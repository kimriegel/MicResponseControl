
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Dropdown from '../Components/Dropdown';

const API_URL = 'http://localhost:8000';

const typeOptions = [
  { label: 'Signal' },
  { label: 'Time' },
];

const signalUnits = [
  { label: 'V' },
  { label: 'mV' },
  { label: 'Pa' },
  { label: 'mPa' },
  { label: 'kPa' },
];

const timeUnits = [
  { label: 's' },
  { label: 'ms' },
  { label: 'µs' },
];

export default function FrequencyResponse() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [columns, setColumns] = useState([]);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const updateColumn = (index, property, value) => {
    setColumns((previous) =>
      previous.map((column, i) => {
        if (i !== index) return column;

        const updated = { ...column, [property]: value };

        if (property === 'type') {
          updated.unit = value === 'Time' ? 's' : 'V';
        }

        return updated;
      })
    );
  };

  const handleFileChange = (event) => {
    setFile(event.target.files?.[0] ?? null);
    setColumns([]);
    setStatus('');
  };

  async function handleDetect() {
    if (!file) {
      setStatus('Please select a CSV file first.');
      return;
    }

    setLoading(true);
    setStatus('Detecting columns...');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_URL}/api/detect`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const result = await response.json();

      setColumns(
        result.columns.map((column) => ({
          ...column,
          type: column.suggestedType ?? 'Signal',
          unit: column.suggestedUnit ?? 'V',
        }))
      );

      setStatus('Detection complete. Review the mapping below.');
    } catch (error) {
      setStatus(`Detection failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit() {
    if (!file || columns.length === 0) {
      setStatus('Select a CSV and detect its columns first.');
      return;
    }

    setLoading(true);
    setStatus('Calculating frequency response...');

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('mapping', JSON.stringify(columns));

      const response = await fetch(
        `${API_URL}/api/frequency-response`,
        {
          method: 'POST',
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const results = await response.json();

      navigate('/frequency-results', {
        state: results,
      });
    } catch (error) {
      setStatus(`Processing failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="frequency-page">
      <h2>Frequency Response</h2>
      <p>
        Upload your measurement CSV, map the columns, and calculate
        the frequency response.
      </p>

      <div className="action-row">
        <label className="file-picker">
          Select CSV
          <input
            type="file"
            accept=".csv,text/csv"
            onChange={handleFileChange}
          />
        </label>

        <span className="file-name">
          {file ? file.name : 'No file selected'}
        </span>

        <button
          className="action-button secondary"
          onClick={handleDetect}
          disabled={loading || !file}
        >
          {loading ? 'Working...' : 'Detect'}
        </button>
      </div>

      {columns.length > 0 && (
        <>
          <h3>Column Mapping</h3>
          <p>
            Choose which source column represents time and which
            columns contain signal measurements.
          </p>

          <div className="mapping-list">
            {columns.map((column, index) => {
              const units =
                column.type === 'Time' ? timeUnits : signalUnits;

              return (
                <div className="mapping-row" key={column.index}>
                  <div className="mapping-source">
                    <strong>{column.name}</strong>
                    <span>
                      Source column: {column.index}
                    </span>
                  </div>

                  <div className="mapping-setting">
                    <label>Type</label>
                    <Dropdown
                      title={column.type}
                      items={typeOptions}
                      onSelect={(value) =>
                        updateColumn(index, 'type', value)
                      }
                    />
                  </div>

                  <div className="mapping-setting">
                    <label>Units</label>
                    <Dropdown
                      title={column.unit}
                      items={units}
                      onSelect={(value) =>
                        updateColumn(index, 'unit', value)
                      }
                    />
                  </div>
                </div>
              );
            })}
          </div>

          <button
            className="action-button primary"
            onClick={handleSubmit}
            disabled={loading}
          >
            Confirm &amp; Submit
          </button>
        </>
      )}

      {status && <p className="status-message">{status}</p>}
    </div>
  );
}
