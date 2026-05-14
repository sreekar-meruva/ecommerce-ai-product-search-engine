from  pydantic import BaseModel, Field, model_validator
from typing import List, Optional

class SearchRequest(BaseModel):
    query: Optional[str] = Field(default=None, example="comfortable shoes for walking")
    category: Optional[str] = Field(default=None, example="footwear")
    sources: List[str] = Field(..., min_length=1, example=["amazon", "walmart", "nike"])
    min_price: Optional[float] = Field(default=None, ge=0, example=20)
    max_price: Optional[float] = Field(default=None, ge=0, example=100)
    min_rating: Optional[float] = Field(default=None, ge=0, le=5.0, example=4.1)
    top_k: int = Field(default=5, ge=1, le=20)

    @model_validator(mode="after")
    def query_or_category_empty(self):
        query_empty = not self.query or self.query.strip() == None
        category_empty = not self.category or self.category.strip() == None

        if(query_empty and category_empty):
            raise ValueError("Either query or category must be provided.")
        
        if(self.min_price is not None and self.max_price is not None):
            if(self.min_price > self.max_price):
                raise ValueError("Minimum price cannot be greater than maximum price.")
        
        return self

class ProductResult(BaseModel):
    product_id: int
    name: str
    category: str
    brand: str
    description: str
    price: float
    rating: float
    review_count: int
    source: str
    product_url: str
    image_url: Optional[str] = None
    availability: Optional[str] = None
    delivery_estimate: Optional[str] = None
    similarity_score: Optional[float] = None

class SearchResponse(BaseModel):
    query: str
    total_results: int
    result: List[ProductResult]