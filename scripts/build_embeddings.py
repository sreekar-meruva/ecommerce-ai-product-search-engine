import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_PATH = "data\cross_platform_products.csv"
MODEL_DIR = "models"
embeddings_path = os.path.join(MODEL_DIR,"prod_embeddings.npy")
category_embedding_path = os.path.join(MODEL_DIR, "category_embeddings.npy")
processed_products_path = os.path.join(MODEL_DIR,"processed_prods.csv")
processed_category_path = os.path.join(MODEL_DIR,"processed_categories.csv")

def product_info(row):
    return(f"{row['name']} {row['category']} {row['brand']} {row['color']} {row['description']} {row['source']} {row['tags']}")

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    products = pd.read_csv(DATA_PATH)
    products["search_text"] = products.apply(product_info, axis=1)
    category_list = products["category"].unique().tolist()

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    prod_embeddings = model.encode(
        products["search_text"].to_list(),
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    category_embeddings = model.encode(
        category_list,
        normalize_embeddings=True
    )
    categories = pd.DataFrame(category_list,columns=['category'])

    np.save(embeddings_path, prod_embeddings)
    np.save(category_embedding_path,category_embeddings)
    products.to_csv(processed_products_path, index=False)
    categories.to_csv(processed_category_path,index=False)

if __name__ == "__main__":
    main()