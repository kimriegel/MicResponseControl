
import React, { useState } from 'react';
import Dropdown from './Dropdown';

export default function Textbox({
  signalUnits,
  timeUnits,
  columnType,
}) {
  const [text, setText] = useState('');
  const [columnSettings, setColumnSettings] = useState({
    time: {
      type: 'Time',
      unit: 's',
    },
  });

  const channelCount = Math.max(
    0,
    Math.floor(Number(text) || 0)
  );

  const columns = [
    {
      id: 'time',
      name: 'Time',
      defaultType: 'Time',
    },
    ...Array.from({ length: channelCount }, (_, index) => ({
      id: `signal-${index + 1}`,
      name: `Signal ${index + 1}`,
      defaultType: 'Signal',
    })),
  ];

  const handleTypeChange = (columnId, newType) => {
    setColumnSettings((previous) => {
      const currentSettings = previous[columnId] || {};

      const defaultUnit = newType === 'Time' ? 's' : 'V';

      return {
        ...previous,
        [columnId]: {
          type: newType,
          unit:
            currentSettings.type === newType
              ? currentSettings.unit
              : defaultUnit,
        },
      };
    });
  };

  const handleUnitChange = (columnId, newUnit) => {
    setColumnSettings((previous) => ({
      ...previous,
      [columnId]: {
        ...(previous[columnId] || {}),
        unit: newUnit,
      },
    }));
  };

  return (
    <div className="input-container">
      <label htmlFor="custom-textbox" className="input-label">
        How many channels are you using?
      </label>

      <input
        id="custom-textbox"
        type="text"
        className="text-input"
        placeholder="Type in a number"
        value={text}
        onChange={(event) => setText(event.target.value)}
      />

      <p className="preview-text">
        Total columns: {columns.length}
      </p>

      <details className="column-config">
        <summary>
          Configure columns ({columns.length})
        </summary>

        <div className="column-list">
          {columns.map((column, index) => {
            const settings = columnSettings[column.id] || {};

            const currentType = settings.type ?? column.defaultType;

            const currentUnit =
              settings.unit ?? (currentType === 'Time' ? 's' : 'V');
            const availableUnits =
              currentType === 'Time' ? timeUnits : signalUnits;

            return (
              <div className="column-item" key={column.id}>
                <div className="column-info">
                  <strong>
                    Column {index + 1}: {column.name}
                  </strong>

                  <span>Column identifier: {column.id}</span>
                </div>

                <div className="column-setting">
                  <label>Type</label>

                  <Dropdown
                    title={currentType}
                    items={columnType}
                    onSelect={(newType) =>
                      handleTypeChange(column.id, newType)
                    }
                  />
                </div>

                <div className="column-setting">
                  <label>Units</label>

                  <Dropdown
                    title={currentUnit}
                    items={availableUnits}
                    onSelect={(newUnit) =>
                      handleUnitChange(column.id, newUnit)
                    }
                  />
                </div>
              </div>
            );
          })}
        </div>
      </details>
    </div>
  );
}
