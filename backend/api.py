import json
import tempfile
import uuid
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from frequency_response.data.detector import (
    detect_data_start,
    detect_time_column,
)
from frequency_response.data.loader import read_data
from frequency_response.data.converter import convert_time, convert_signal
from frequency_response.data.exporter import save_results_csv
from frequency_response.models.channel import Channel
from frequency_response.processing.frequency_response import (
    calculate_frequency_response,
)


app = FastAPI(title="Frequency Response API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = Path(tempfile.gettempdir()) / "frequency_response_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

saved_results = {}


def load_uploaded_csv(file_path):
    data_start = detect_data_start(file_path)

    if data_start is None:
        raise ValueError("Could not detect the start of CSV data.")

    data = read_data(file_path, data_start)

    if data.empty or len(data.columns) < 2:
        raise ValueError(
            "The CSV must contain at least two data columns."
        )

    return data


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/detect")
async def detect(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file.",
        )

    input_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".csv",
            delete=False,
        ) as temporary:
            temporary.write(await file.read())
            input_path = Path(temporary.name)

        data = load_uploaded_csv(input_path)
        suggested_time = detect_time_column(data)

        columns = []

        for index in data.columns:
            is_time = index == suggested_time

            columns.append({
                "index": int(index),
                "name": f"Column {index + 1}",
                "suggestedType": "Time" if is_time else "Signal",
                "suggestedUnit": "s" if is_time else "V",
            })

        return {"columns": columns}

    except HTTPException:
        raise

    except (ValueError, pd.errors.ParserError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    finally:
        if input_path is not None:
            input_path.unlink(missing_ok=True)


@app.post("/api/frequency-response")
async def process(
    file: UploadFile = File(...),
    mapping: str = Form(...),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file.",
        )

    try:
        column_mapping = json.loads(mapping)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid column mapping JSON.",
        )

    input_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".csv",
            delete=False,
        ) as temporary:
            temporary.write(await file.read())
            input_path = Path(temporary.name)

        data = load_uploaded_csv(input_path)

        time_columns = [
            column
            for column in column_mapping
            if column.get("type") == "Time"
        ]

        signal_columns = [
            column
            for column in column_mapping
            if column.get("type") == "Signal"
        ]

        if len(time_columns) != 1:
            raise HTTPException(
                status_code=400,
                detail="Select exactly one time column.",
            )

        if not signal_columns:
            raise HTTPException(
                status_code=400,
                detail="Select at least one signal column.",
            )

        time_config = time_columns[0]
        time_index = int(time_config["index"])

        if time_index not in data.columns:
            raise HTTPException(
                status_code=400,
                detail="Invalid time column index.",
            )

        time_data = convert_time(
            data[time_index].to_numpy(),
            time_config["unit"],
        )

        channels = []

        for config in signal_columns:
            index = int(config["index"])

            if index not in data.columns:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid signal column index.",
                )

            unit = config["unit"]

            signal_data = convert_signal(
                data[index].to_numpy(),
                input_unit=unit,
                output_unit=unit,
            )

            channel = Channel(
                name=config.get(
                    "name",
                    f"Channel {len(channels) + 1}",
                ),
                time=time_data,
                raw_data=signal_data,
            )

            channel.frequency, channel.decibels = (
                calculate_frequency_response(channel)
            )

            channels.append(channel)

        result_id = uuid.uuid4().hex
        csv_path = OUTPUT_DIR / f"{result_id}_revised.csv"

        save_results_csv(channels, csv_path)

        saved_results[result_id] = csv_path

        return {
            "resultId": result_id,
            "channels": [
                {
                    "name": channel.name,
                    "frequency": channel.frequency.tolist(),
                    "decibels": channel.decibels.tolist(),
                }
                for channel in channels
            ],
            "csvDownloadUrl": (
                f"http://localhost:8000/api/results/{result_id}/csv"
            ),
        }

    except HTTPException:
        raise

    except (
        ValueError,
        KeyError,
        TypeError,
        IndexError,
        pd.errors.ParserError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    finally:
        if input_path is not None:
            input_path.unlink(missing_ok=True)


@app.get("/api/results/{result_id}/csv")
def download_csv(result_id: str):
    csv_path = saved_results.get(result_id)

    if csv_path is None or not csv_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Result CSV not found.",
        )

    return FileResponse(
        path=csv_path,
        media_type="text/csv",
        filename="frequency_response_revised.csv",
    )