let mediaRecorder;
let recordedChunks = [];

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "startRecording") {
    chrome.tabCapture.capture({ audio: true, video: false }, (stream) => {
      mediaRecorder = new MediaRecorder(stream);
      recordedChunks = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) recordedChunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(recordedChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("file", blob, "meet_audio.webm");

        try {
          const res = await fetch("http://localhost:7860/upload", {
            method: "POST",
            body: formData,
          });
          const data = await res.json();
          sendResponse({
            summary: data.summary,
            language: data.language,
            pdfUrl: "http://localhost:7860" + data.pdf_url,
          });
        } catch (err) {
          sendResponse({ error: err.message });
        }
      };

      mediaRecorder.start();
    });
    return true;
  }

  if (msg.action === "stopRecording") {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
    }
    return true; // indicates async response
  }
});
