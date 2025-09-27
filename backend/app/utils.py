import os
from sqlalchemy import create_engine
from langchain_community.utilities import  SQLDatabase
from langchain_community.llms import HuggingFaceHub
from huggingface_hub import InferenceClient
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from app.config import DATABASE_URL


def get_sql_database():
    engine = create_engine(DATABASE_URL)
    db = SQLDatabase(engine)
    return db


def get_llm():
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # Build a Transformers pipeline (text generation)
    generator = pipeline(
        "text-generation",
        model="meta-llama/Llama-3.2-3B-Instruct",   # Or 1B if 3B is too heavy
        token=hf_token,
        max_new_tokens=256,
        temperature=0.1,
    )

    # Wrap into LangChain-compatible LLM
    llm = HuggingFacePipeline(pipeline=generator)
    return llm


