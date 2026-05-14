import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_PATH = "data\cross_platform_products.csv"
MODEL_DIR = "models"
embeddings_path = os.path.join(MODEL_DIR,"prod_embeddings.npy")
processed_products_path = os.path.join(MODEL_DIR,"processed_prods.csv")

def product_info(row):
    return(f"{row['name']} {row['category']} {row['brand']} {row['color']} {row['description']} {row['source']} {row['tags']}")

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    products = pd.read_csv(DATA_PATH)
    products["search_text"] = products.apply(product_info, axis=1)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    embeddings = model.encode(
        products["search_text"].to_list(),
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    np.save(embeddings_path, embeddings)
    products.to_csv(processed_products_path, index=False)

if __name__ == "__main__":
    main()