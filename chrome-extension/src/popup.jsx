import React, { useState } from "react";
import "./popup.css";

const Popup = () => {
  const [recording, setRecording] = useState(false);
  const [enabled, setEnabled] = useState(false);
  const [summary, setSummary] = useState("");
  const [pdfUrl, setPdfUrl] = useState(null);

  const handleToggle = () => {
    setEnabled(!enabled);
    if (!enabled) {
      chrome.runtime.sendMessage({ action: "START_RECORDING" });
    } else {
      chrome.runtime.sendMessage({ action: "STOP_RECORDING" });
    }
  };

  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.action === "SUMMARY_READY") {
      setSummary(msg.data.summary);
      setPdfUrl(msg.data.pdf_url);
    }
  });

  return (
    <div className="popup-container">
      <h3>GMeet Summarizer</h3>
      <label className="switch">
        <input type="checkbox" checked={enabled} onChange={handleToggle} />
        <span className="slider round"></span>
      </label>
      <p>{enabled ? "Summarization ON" : "Summarization OFF"}</p>

      {summary && (
        <>
          <h4>Summary:</h4>
          <pre>{summary}</pre>
          {pdfUrl && (
            <a href={pdfUrl} target="_blank">
              Download PDF
            </a>
          )}
        </>
      )}
    </div>
  );
};

export default Popup;
