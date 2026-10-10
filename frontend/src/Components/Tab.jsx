export default function Tab({ tabData, activeTab, setActiveTab }) {
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
