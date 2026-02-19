from sentence_transformers import SentenceTransformer
import chromadb
import pandas as pd
import os

EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
CHROMA_PATH = "vector_db"
# Use EphemeralClient for simplicity - data will persist across runs via file storage
CLIENT = chromadb.EphemeralClient()
COLLECTION_NAME = "courses"

def load_courses():
    df = pd.read_csv("data/sample_courses.csv")
    df.fillna("", inplace=True)
    return df

def embed_and_store():
    if os.path.exists(CHROMA_PATH) and COLLECTION_NAME in [c.name for c in CLIENT.list_collections()]:
        print("Vector DB already exists")
        return CLIENT.get_collection(COLLECTION_NAME)
    
    df = load_courses()
    collection = CLIENT.create_collection(COLLECTION_NAME)
    
    for i, row in df.iterrows():
        text = f"{row['title']} {row['description']} {row['topics']}"
        embedding = EMBEDDING_MODEL.encode(text).tolist()
        metadata = {
            "title": row['title'],
            "description": row['description'],
            "prerequisites": row['prerequisites'],
            "difficulty": row['difficulty'],
            "duration_hours": str(row['duration_hours']),
            "platform": row['platform'],
            "link": row['link']
        }
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[text]
        )
    print("Embeddings created and stored")
    return collection

def retrieve_courses(query, k=10):
    embedding = EMBEDDING_MODEL.encode(query).tolist()
    collection = CLIENT.get_collection(COLLECTION_NAME)
    results = collection.query(query_embeddings=[embedding], n_results=k)
    return results