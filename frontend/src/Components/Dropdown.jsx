
import React, { useState, useEffect, useRef } from 'react';

export default function Dropdown({ title, items, onSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(title);
  const dropdownRef = useRef(null);

  useEffect(() => {
    setSelectedItem(title);
  }, [title]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="dropdown-container" ref={dropdownRef}>
      <button
        type="button"
        className="dropdown-trigger"
        onClick={() => setIsOpen((previous) => !previous)}
        aria-haspopup="true"
        aria-expanded={isOpen}
      >
        {selectedItem}
        <span className={`dropdown-arrow ${isOpen ? 'open' : ''}`}>
          ▼
        </span>
      </button>

      {isOpen && (
        <ul className="dropdown-menu" role="menu">
          {items.map((item) => (
            <li key={item.label} className="dropdown-item" role="none">
              <button
                type="button"
                role="menuitem"
                onClick={() => {
                  setSelectedItem(item.label);
                  onSelect?.(item.label);
                  item.onClick?.();
                  setIsOpen(false);
                }}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
