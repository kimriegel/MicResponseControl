import React, { useState } from 'react';
import './App.css';
import Tab from './Components/Tab';
import Dropdown from './Components/DropDown';

export default function App() {
  const [activeTab, setActiveTab] = useState('tab1');

  const tabData = [
    { id: 'tab1', label: 'Frequency Response', content: 'Frequency Response Content' },
    { id: 'tab2', label: 'Directivity', content: 'Directivity Content' },
  ];

  const signalUnits = [
    { label: 'V', onClick: () => console.log('Volts clicked') },
    { label: 'mV', onClick: () => console.log('Milivolts clicked') },
    { label: 'Pa', onClick: () => console.log('Pascals clicked') },
    { label: 'mPa', onClick: () => console.log('Milipascals clicked') },
  ];


  const timeUnits = [
    { label: 's', onClick: () => console.log('Seconds clicked') },
    { label: 'ms', onClick: () => console.log('Miliseconds clicked') },
    { label: 'µs', onClick: () => console.log('Microseconds clicked') },
  ];

  return (
    <div style={{ padding: '40px' }}>
      <Tab
        tabData={tabData}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <Dropdown title="Units" items={signalUnits} />
      <Dropdown title="Units" items={timeUnits} />

    </div>
  );
}
