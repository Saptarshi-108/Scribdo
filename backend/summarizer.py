import os
from transformers import pipeline
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils import generate_pdf, detect_language

def summarize_audio(audio_path):
    # 1. Transcribe
    asr = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en", chunk_length_s=30)
    transcript = asr(audio_path)["text"]

    # 2. Detect Language
    lang = detect_language(transcript)

    # 3. Summarize
    llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.1", model_kwargs={"temperature": 0.2, "max_new_tokens": 500})
    prompt = PromptTemplate(input_variables=["context"], template="List the key points from this context:\n\n{context}")
    chain = LLMChain(llm=llm, prompt=prompt)
    summary = chain.run(transcript)

    # 4. Generate PDF
    pdf_path = generate_pdf(summary, lang)

    return summary, lang, pdf_path
