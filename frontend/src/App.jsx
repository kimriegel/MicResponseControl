
import { useState } from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';

import './App.css';

import Tab from './Components/Tab';
import FrequencyResponse from './Pages/FrequencyResponse';
import Directivity from './Pages/Directivity';
import Results from './Pages/Results';

function Home() {
  const [activeTab, setActiveTab] = useState('tab1');

  const tabData = [
    {
      id: 'tab1',
      label: 'Frequency Response',
      content: <FrequencyResponse />,
    },
    {
      id: 'tab2',
      label: 'Directivity',
      content: <Directivity />,
    },
  ];

  return (
    <div className="app-container">
      <Tab
        tabData={tabData}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/frequency-results"
          element={<Results />}
        />
      </Routes>
    </BrowserRouter>
  );
}
