from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from summarizer import summarize_audio, summarize_partial_audio
from utils import cleanup_temp_folder

app = FastAPI()

# Allow only Chrome extension origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://abcdefghijklmnopqrstuvwxyz123456"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    cleanup_temp_folder()  # Delete old files
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filename, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        summary, language, pdf_path = summarize_audio(filename)
        return {
            "summary": summary,
            "language": language,
            "pdf_url": f"/download?path={pdf_path}"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/live")
async def live_summary(file: UploadFile = File(...)):
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filename, "wb") as f:
        f.write(await file.read())

    try:
        partial_summary = summarize_partial_audio(filename)
        return {"partial_summary": partial_summary}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download")
def download_pdf(path: str = Query(...)):
    return FileResponse(path, media_type="application/pdf", filename="summary.pdf")
