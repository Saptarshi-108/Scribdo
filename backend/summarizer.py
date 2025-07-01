import os
from transformers import pipeline
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils import generate_pdf, detect_language
from dotenv import load_dotenv

load_dotenv()

# Load models
print("Loading ASR model...")
asr_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en", chunk_length_s=30)

print("Initializing LLM with HuggingFaceHub...")
llm = HuggingFaceHub(
    huggingfacehub_api_token=os.environ.get("HUGGINGFACEHUB_API_TOKEN"),
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    model_kwargs={"temperature": 0.2, "max_new_tokens": 500}
)

prompt_template = PromptTemplate(
    input_variables=["context"],
    template="List the key points from this context:\n\n{context}"
)
chain = LLMChain(llm=llm, prompt=prompt_template)

def summarize_audio(audio_path):
    print(f"Transcribing full audio: {audio_path}")
    transcript = asr_pipeline(audio_path)["text"]
    print("Transcript:", transcript[:300])

    lang = detect_language(transcript)
    print("Detected language:", lang)

    summary = chain.run(transcript)
    print("Generated summary.")

    pdf_path = generate_pdf(summary, lang)
    return summary, lang, pdf_path

def summarize_partial_audio(audio_path):
    print(f"Processing partial audio: {audio_path}")
    transcript = asr_pipeline(audio_path)["text"]
    return chain.run(transcript)
