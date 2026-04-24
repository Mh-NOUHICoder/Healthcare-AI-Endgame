from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

try:
    print("Testing models/text-embedding-004")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    res = embeddings.embed_query("hello")
    print("SUCCESS text-embedding-004, length:", len(res))
except Exception as e:
    print("FAILED:", e)

try:
    print("Testing models/embedding-001")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    res = embeddings.embed_query("hello")
    print("SUCCESS embedding-001, length:", len(res))
except Exception as e:
    print("FAILED:", e)
    
try:
    print("Testing embedding-001")
    embeddings = GoogleGenerativeAIEmbeddings(model="embedding-001")
    res = embeddings.embed_query("hello")
    print("SUCCESS embedding-001 (no prefix), length:", len(res))
except Exception as e:
    print("FAILED:", e)
