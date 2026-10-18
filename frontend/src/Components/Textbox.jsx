import React, { useState } from 'react';

export default function Textbox() {
  const [text, setText] = useState('');

  const handleChange = (e) => {
    setText(e.target.value);
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
        onChange={handleChange}
      />
      <p className="preview-text">Live Output: {text}</p>
    </div>
  );
}
