import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ProductSearchEngine:
    def __init__(self,
                 product_path = "models/processed_prods.csv",
                 embeddings_path = "models/prod_embeddings.npy",
                 category_embedding_path = "models/category_embeddings.npy",
                 categories_path = "models/processed_categories.csv",
                 model_name = "sentence-transformers/all-MiniLM-L6-v2"):
        self.products = pd.read_csv(product_path)
        self.categories = pd.read_csv(categories_path)
        self.prod_embeddings = np.load(embeddings_path)
        self.category_embeddings = np.load(category_embedding_path)
        self.model = SentenceTransformer(model_name)

    def search(self, 
               query: str, 
               top_k: int = 5, 
               category: str = None,
               sources: list = None,
               min_price: float = None,
               max_price: float = None,
               min_rating: float = None):
        query_empty = not query or query.strip()==""
        category_empty = not category or category.strip()==""

        candidates = list(range(len(self.products)))

        if not category_empty:
            query_cat_embeddings = self.model.encode(
                [category],
                convert_to_numpy=True,
                normalize_embeddings=True  
            )
            cat_embeddings = self.category_embeddings
            cat_sim_score = cosine_similarity(query_cat_embeddings,cat_embeddings)[0]
            sort_cat_sim_score = cat_sim_score.argsort()[::-1]
            relevant_category = self.categories.iloc[sort_cat_sim_score[0]]["category"]
            candidates = [
                indx for indx in candidates
                if self.products.iloc[indx]["category"].lower() == relevant_category.lower()
            ]


        if sources:
            sources_lower = [source.lower() for source in sources]
            candidates = [
                indx for indx in candidates
                if self.products.iloc[indx]["source"].lower() in sources_lower
            ]
        
        if min_price:
            candidates = [
                indx for indx in candidates
                if float(self.products.iloc[indx]["price"]) >= min_price
            ]
        
        if max_price:
            candidates = [
                indx for indx in candidates
                if float(self.products.iloc[indx]["price"] <= max_price)
            ]
        
        if min_rating:
            candidates = [
                indx for indx in candidates
                if float(self.products.iloc[indx]["rating"] >= min_rating)
            ]

        if not candidates:
            return []
        
        if query_empty:
            return self.build_results(candidates[:top_k], None, None)
        
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        candidate_embeddings = self.prod_embeddings[candidates]
        similarity_scores = cosine_similarity(query_embedding, candidate_embeddings)[0]
        sort_similarity_scores = similarity_scores.argsort()[::-1]
        top_candidate_positions = sort_similarity_scores[:top_k]
        top_candidates = [candidates[position] for position in top_candidate_positions]
        

        return(self.build_results(top_candidates, similarity_scores,candidates))
    
    def build_results(self,top_k_products: list, similarity_scores = None, candidates=None):
        results = []
        for indx in top_k_products:
            product = self.products.iloc[indx]
            if similarity_scores is not None:
                position = candidates.index(indx)
                score = round(float(similarity_scores[position]),4)
            else:
                score = None
            results.append({
                "product_id": int(product["product_id"]),
                "name": str(product["name"]),
                "category": str(product["category"]),
                "brand": str(product["brand"]),
                "description": str(product["description"]),
                "price": float(product["price"]),
                "rating": float(product["rating"]),
                "review_count": int(product["review_count"]),
                "source": str(product["source"]),
                "product_url": str(product["product_url"]),
                "image_url": str(product["image_url"]) if "image_url" in product else None,
                "availability": str(product["availability"]) if "availability" in product else None,
                "delivery_estimate": str(product["delivery_estimate"]) if "delivery_estimate" in product else None,
                "similarity_score": score
            })
        return(results)