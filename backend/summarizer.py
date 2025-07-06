import os
from transformers import pipeline
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils import generate_pdf, detect_language

asr = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en", chunk_length_s=30)
llm = HuggingFaceHub(
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    model_kwargs={"temperature": 0.2, "max_new_tokens": 500}
)
prompt = PromptTemplate(input_variables=["context"], template="List the key points from this audio transcript in bullet points :\n\n{context}")
chain = LLMChain(llm=llm, prompt=prompt)

def summarize_audio(audio_path):
    transcript = asr(audio_path)["text"].strip()
    if not transcript:
        raise ValueError("No speech detected for summarization.")
    lang = detect_language(transcript)
    summary = chain.run(transcript)
    pdf_path = generate_pdf(summary, lang)
    return summary, lang, pdf_path

def summarize_partial_audio(audio_path):
    # Not used anymore
    return None
