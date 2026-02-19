from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os
import pickle

EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_FILE = os.path.join(BASE_DIR, "embeddings.pkl")

def load_courses():
    csv_path = os.path.join(BASE_DIR, "data", "sample_courses.csv")
    df = pd.read_csv(csv_path)
    df.fillna("", inplace=True)
    return df

def embed_and_store():
    """Create and store embeddings using pickle instead of ChromaDB"""
    if os.path.exists(EMBEDDINGS_FILE):

        print("Loading existing embeddings...")
        with open(EMBEDDINGS_FILE, 'rb') as f:
            return pickle.load(f)
    
    print("Creating embeddings...")
    df = load_courses()
    embeddings_data = {
        'embeddings': [],
        'metadata': [],
        'documents': []
    }
    
    for i, row in df.iterrows():
        text = f"{row['title']} {row['description']} {row['topics']}"
        embedding = EMBEDDING_MODEL.encode(text)
        
        embeddings_data['embeddings'].append(embedding)
        embeddings_data['documents'].append(text)
        embeddings_data['metadata'].append({
            "title": row['title'],
            "description": row['description'],
            "prerequisites": row['prerequisites'],
            "difficulty": row['difficulty'],
            "duration_hours": str(row['duration_hours']),
            "platform": row['platform'],
            "link": row['link']
        })
    
    embeddings_data['embeddings'] = np.array(embeddings_data['embeddings'])
    
    with open(EMBEDDINGS_FILE, 'wb') as f:
        pickle.dump(embeddings_data, f)
    
    print("Embeddings created and stored")
    return embeddings_data

def retrieve_courses(query, k=10):
    """Retrieve courses using cosine similarity"""
    embedding = EMBEDDING_MODEL.encode(query)
    
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, 'rb') as f:
            data = pickle.load(f)
    else:
        data = embed_and_store()
    
    # Calculate cosine similarity
    embeddings = data['embeddings']
    similarities = np.dot(embeddings, embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embedding)
    )
    
    # Get top k indices
    top_indices = np.argsort(similarities)[::-1][:k]
    
    # Format results similar to ChromaDB
    results = {
        'metadatas': [[data['metadata'][i] for i in top_indices]],
        'documents': [[data['documents'][i] for i in top_indices]],
        'distances': [[1 - similarities[i] for i in top_indices]]  # Convert similarity to distance
    }
    
    return results
