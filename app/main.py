from app.schemas import SearchRequest, SearchResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.search_engine import ProductSearchEngine

app = FastAPI(
    title="AI Product Search API",
    description="Semantic product search using Sentence-BERT embeddings and cosine similarity",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

search_engine = ProductSearchEngine()

@app.get("/")
def home():
    return{
        "message": "AI Product Search API is running",
        "docs": "/docs"
    }

@app.post("/search",response_model = SearchResponse)
def search_products(request: SearchRequest):
    try:
        results = search_engine.search(
            query = request.query,
            top_k = request.top_k,
            category = request.category,
            sources = request.sources,
            min_price = request.min_price,
            max_price = request.max_price,
            min_rating = request.min_rating
        )

        return({
            "query": request.query,
            "total_results": len(results),
            "results": results
        })
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))