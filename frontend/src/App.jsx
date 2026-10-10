import React, { useState } from 'react';
import './App.css';

import Tab from './Components/Tab';

import FrequencyResponse from './Pages/FrequencyResponse';
import Directivity from './Pages/Directivity';

export default function App() {
  const [activeTab, setActiveTab] = useState('tab1');

  const tabData = [
    { id: 'tab1', label: 'Frequency Response', content:  <FrequencyResponse /> },
    { id: 'tab2', label: 'Directivity', content: <Directivity /> },
  ];

  return (
    <div style={{ padding: '40px' }}>
      <Tab
        tabData={tabData}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />
    </div>
  );
}
