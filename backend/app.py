from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from summarizer import summarize_audio, summarize_partial_audio
from utils import cleanup_temp_folder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension:iecoipjpgmodkkfbacfbmciahlaicdhf","*"],  # In production, restrict this to chrome-extension://<EXT_ID>
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    cleanup_temp_folder()
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        summary, language, pdf_path = summarize_audio(file_path)
        return {
            "summary": summary,
            "language": language,
            "pdf_url": f"/download?path={pdf_path}",
        }
    except Exception as e:
        print("Upload processing failed:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/live")
async def live_partial_summary(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        partial_summary = summarize_partial_audio(file_path)
        return {"partial_summary": partial_summary}
    except Exception as e:
        print("Live summarization failed:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/download")
def download_pdf(path: str = Query(...)):
    if os.path.exists(path):
        return FileResponse(path, media_type="application/pdf", filename="summary.pdf")
    return JSONResponse(status_code=404, content={"error": "File not found"})
