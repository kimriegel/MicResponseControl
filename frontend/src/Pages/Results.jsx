
import { useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import {
  Chart as ChartJS,
  LinearScale,
  LogarithmicScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';

import { Scatter } from 'react-chartjs-2';

ChartJS.register(
  LinearScale,
  LogarithmicScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

export default function Results() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const chartRef = useRef(null);

  if (!state?.channels) {
    return (
      <div className="results-page">
        <h2>No results available</h2>
        <p>Submit a CSV from the Frequency Response page first.</p>
        <button
          className="action-button secondary"
          onClick={() => navigate('/')}
        >
          Back to Frequency Response
        </button>
      </div>
    );
  }

  const colors = [
    '#5289AD',
    '#D97757',
    '#419873',
    '#9370DB',
    '#C49A28',
    '#D45B83',
  ];

  const datasets = state.channels.map((channel, index) => ({
    label: channel.name,
    data: channel.frequency
      .map((frequency, pointIndex) => ({
        x: frequency,
        y: channel.decibels[pointIndex],
      }))
      .filter(
        (point) =>
          Number.isFinite(point.x) &&
          point.x > 0 &&
          Number.isFinite(point.y)
      ),
    borderColor: colors[index % colors.length],
    backgroundColor: colors[index % colors.length],
    borderWidth: 1.5,
    pointRadius: 0,
    showLine: true,
    tension: 0,
  }));

  const chartData = { datasets };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'nearest',
      intersect: false,
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      tooltip: {
        callbacks: {
          label: (context) =>
            `${context.dataset.label}: ` +
            `${context.parsed.y.toFixed(2)} dB at ` +
            `${context.parsed.x.toPrecision(4)} Hz`,
        },
      },
    },
    scales: {
      x: {
        type: 'logarithmic',
        title: {
          display: true,
          text: 'Frequency (Hz)',
        },
      },
      y: {
        type: 'linear',
        title: {
          display: true,
          text: 'Magnitude (dB)',
        },
      },
    },
  };


const saveGraph = () => {
  const chart = chartRef.current;

  if (!chart) return;

  const sourceCanvas = chart.canvas;
  const exportCanvas = document.createElement("canvas");

  exportCanvas.width = sourceCanvas.width;
  exportCanvas.height = sourceCanvas.height;

  const context = exportCanvas.getContext("2d");

  // Paint the background white before drawing the chart.
  context.fillStyle = "#ffffff";
  context.fillRect(0, 0, exportCanvas.width, exportCanvas.height);

  context.drawImage(sourceCanvas, 0, 0);

  const link = document.createElement("a");
  link.download = "frequency-response.png";
  link.href = exportCanvas.toDataURL("image/png");
  link.click();
};


  async function saveCSV() {
    if (!state.csvDownloadUrl) {
      alert('The backend did not provide a CSV download URL.');
      return;
    }

    try {
      const response = await fetch(state.csvDownloadUrl);

      if (!response.ok) {
        throw new Error('Unable to download the CSV.');
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');

      link.href = url;
      link.download = 'frequency_response_revised.csv';
      link.click();

      URL.revokeObjectURL(url);
    } catch (error) {
      alert(error.message);
    }
  }

  return (
    <div className="results-page">
      <h2>Frequency Response Results</h2>

      <div className="chart-container">
        <Scatter
          ref={chartRef}
          data={chartData}
          options={chartOptions}
        />
      </div>

      <div className="action-row result-actions">
        <button
          className="action-button primary"
          onClick={saveGraph}
        >
          Save Graph as PNG
        </button>

        <button
          className="action-button primary"
          onClick={saveCSV}
        >
          Download Revised CSV
        </button>

        <button
          className="action-button secondary"
          onClick={() => navigate('/')}
        >
          Back
        </button>
      </div>
    </div>
  );
}
