import React, { useState } from 'react';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('tab1');

  const tabData = [
    { id: 'tab1', label: 'Frequency Response'},
    { id: 'tab2', label: 'Directivity'},
  ];

  return (
    <div className="tabs-container">
      <div className="tabs-list" role="tablist">
        {tabData.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            aria-selected={activeTab === tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="tab-panel" role="tabpanel">
        {tabData.find((tab) => tab.id === activeTab)?.content}
      </div>
    </div>
  );
}
