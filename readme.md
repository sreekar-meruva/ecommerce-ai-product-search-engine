# AI-Powered Cross-Platform Product Search Engine

This project is an AI-powered semantic product search engine that helps users find relevant products across selected shopping platforms using natural-language search. Instead of relying only on exact keyword matching, the system uses Sentence-BERT embeddings and cosine similarity to understand the meaning of a user's query and return semantically relevant products.

The goal of this project is to simulate a cross-platform shopping search experience where users can choose trusted shopping sources, search with generic text, and filter results by category, price range, rating, and source.

---

## Project Overview

Traditional e-commerce search engines often depend heavily on exact keyword matching. For example, if a user searches for:

```text
comfortable shoes for daily walking
```

a keyword-based system may miss products described as:

```text
lightweight running sneakers with cushioned sole
```

This project solves that problem using semantic search. Product information is converted into vector embeddings using a pre-trained Sentence-BERT model. When a user enters a query, the query is also converted into an embedding, and cosine similarity is used to find the most relevant products.

The system also supports filters such as preferred shopping sources, category, price range, and minimum rating.

---

## Features

- Natural-language product search
- Semantic search using Sentence-BERT
- Cosine similarity-based product ranking
- Cross-platform product source filtering
- Category filtering
- Price range filtering
- Minimum rating filtering
- Top-K result retrieval
- FastAPI backend
- Pydantic request and response validation
- Swagger UI for API testing
- Synthetic cross-platform product dataset

---

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pandas
- NumPy
- scikit-learn
- Sentence-Transformers
- Pydantic

---

## Project Structure

```text
ecommerce-ai-product-search-engine/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── search_engine.py
│
├── data/
│   └── cross_platform_products.csv
│
├── models/
│   ├── processed_prods.csv
│   └── prod_embeddings.npy
│
├── scripts/
│   └── build_embeddings.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Dataset

The project uses a synthetic cross-platform e-commerce product dataset.

The dataset includes the following columns:

```text
product_id
name
category
brand
color
description
price
rating
review_count
source
product_url
image_url
availability
delivery_estimate
tags
```

The `source` column represents the shopping platform or website where the product is listed.

Example sources:

```text
Amazon
Walmart
Best Buy
Target
Nike
eBay
```

---

## How It Works

The system follows this pipeline:

```text
Product dataset
    ↓
Combine product fields into searchable text
    ↓
Generate Sentence-BERT embeddings for products
    ↓
Save product embeddings as a NumPy .npy file
    ↓
User sends search query and filters
    ↓
Apply filters such as source, category, price, and rating
    ↓
Generate embedding for the user query
    ↓
Compare query embedding with product embeddings using cosine similarity
    ↓
Return top matching products
```

---

## Model Used

This project uses the pre-trained Sentence-BERT model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model converts product descriptions and user queries into dense numerical vectors called embeddings.

These embeddings are then compared using cosine similarity.

---

## Why Sentence-BERT?

Sentence-BERT is useful because it captures semantic meaning beyond exact keyword matching.

Example:

```text
User query:
comfortable shoes for walking

Product description:
lightweight running sneakers with cushioned sole
```

Even though the exact words are different, Sentence-BERT can understand that both texts are related to walking shoes and comfort.

---

## What is an Embedding?

An embedding is a numerical representation of text.

For example:

```text
"comfortable walking shoes"
```

is converted into a vector like:

```text
[0.12, -0.04, 0.33, ...]
```

In this project, each product is converted into an embedding. The user query is also converted into an embedding. Products with embeddings closest to the query embedding are considered more relevant.

---

## What is Cosine Similarity?

Cosine similarity measures how similar two vectors are.

In this project, it compares:

```text
User query embedding
        with
Product embedding
```

A higher cosine similarity score means the product is more semantically related to the user query.

Example:

```text
0.90 = very strong match
0.70 = good match
0.40 = weak match
```

---

## Search Logic

The search engine supports the following cases:

| Query    | Category | Sources  | Behavior                                                      |
| -------- | -------- | -------- | ------------------------------------------------------------- |
| Provided | Optional | Required | Semantic search within selected sources                       |
| Empty    | Provided | Required | Returns filtered products from selected category and sources  |
| Provided | Provided | Required | Semantic search inside selected category and selected sources |
| Empty    | Empty    | Required | Invalid request                                               |

The `sources` field is required because the goal is to search only within the user's preferred or trusted shopping platforms.

---

## API Request Fields

The `/search` endpoint accepts the following fields:

| Field      | Type            | Required | Description                   |
| ---------- | --------------- | -------- | ----------------------------- |
| query      | string          | No       | Natural-language search query |
| category   | string          | No       | Product category filter       |
| sources    | list of strings | Yes      | Preferred shopping platforms  |
| min_price  | float           | No       | Minimum product price         |
| max_price  | float           | No       | Maximum product price         |
| min_rating | float           | No       | Minimum product rating        |
| top_k      | integer         | No       | Number of products to return  |

At least one of `query` or `category` should be provided.

---

## Run Steps

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/sreekar-meruva/ecommerce-ai-product-search-engine.git
```

Move into the project folder:

```bash
cd ecommerce-ai-product-search-engine
```

---

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Make Sure the Dataset Exists

The dataset should be present at:

```text
data/cross_platform_products.csv
```

This CSV file is used to generate product embeddings.

---

### 5. Build Product Embeddings

Before running the API, generate product embeddings:

```bash
python scripts/build_embeddings.py
```

This creates the following files:

```text
models/processed_prods.csv
models/prod_embeddings.npy
```

The `.npy` file stores the numerical product embeddings generated by Sentence-BERT.

> Note: The embedding file `models/prod_embeddings.npy` is generated locally and may not be committed to GitHub if it is listed in `.gitignore`. Run `python scripts/build_embeddings.py` before starting the API.

---

### 6. Start the FastAPI Server

Run:

```bash
python -m uvicorn app.main:app --reload
```

If `uvicorn` is not recognized on Windows, use the same command above instead of running `uvicorn` directly.

Correct:

```bash
python -m uvicorn app.main:app --reload
```

Avoid:

```bash
uvicorn app.main:app --reload
```

---

### 7. Open Swagger UI

Open this URL in your browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to test the API directly from the browser.

---

### 8. Test the Search API

Use the `POST /search` endpoint with this sample request:

```json
{
  "query": "comfortable shoes for daily walking",
  "category": "footwear",
  "sources": ["Amazon", "Walmart", "Nike"],
  "min_price": 30,
  "max_price": 100,
  "min_rating": 4.0,
  "top_k": 10
}
```

---

### 9. Stop the Server

In the terminal where Uvicorn is running, press:

```text
Ctrl + C
```

---

## API Endpoints

### Home Endpoint

```http
GET /
```

Example response:

```json
{
  "message": "AI Cross-Platform Product Search API is running",
  "docs": "/docs"
}
```

---

### Search Endpoint

```http
POST /search
```

Example request:

```json
{
  "query": "comfortable shoes for daily walking",
  "category": "footwear",
  "sources": ["Amazon", "Walmart", "Nike"],
  "min_price": 30,
  "max_price": 100,
  "min_rating": 4.0,
  "top_k": 10
}
```

Example response:

```json
{
  "query": "comfortable shoes for daily walking",
  "total_results": 10,
  "results": [
    {
      "product_id": 1,
      "name": "Nike Revolution Running Shoes",
      "category": "footwear",
      "brand": "Nike",
      "description": "Lightweight running shoes with soft cushioning for walking and daily use",
      "price": 64.99,
      "rating": 4.5,
      "review_count": 1280,
      "source": "Nike",
      "product_url": "https://example.com/product",
      "image_url": "https://example.com/image.jpg",
      "availability": "In Stock",
      "delivery_estimate": "3-5 days",
      "similarity_score": 0.8421
    }
  ]
}
```

---

## Example Search Requests

### 1. Query with Preferred Sources

```json
{
  "query": "laptop for data science student",
  "sources": ["Amazon", "Best Buy", "Walmart"],
  "top_k": 5
}
```

---

### 2. Category-Only Search

```json
{
  "query": "",
  "category": "footwear",
  "sources": ["Amazon", "Nike"],
  "top_k": 5
}
```

---

### 3. Full Filtered Search

```json
{
  "query": "wireless headphones with noise cancellation",
  "category": "electronics",
  "sources": ["Amazon", "Best Buy"],
  "min_price": 50,
  "max_price": 200,
  "min_rating": 4.2,
  "top_k": 10
}
```

---

### 4. Budget-Based Search

```json
{
  "query": "backpack for college and travel",
  "category": "bags",
  "sources": ["Amazon", "Walmart", "Target"],
  "max_price": 80,
  "min_rating": 4.0,
  "top_k": 10
}
```

---

## Main Components

### 1. `build_embeddings.py`

This script reads the product dataset, combines important product fields into one searchable text field, generates Sentence-BERT embeddings, and saves the processed data.

Main tasks:

```text
Read product CSV
Create search_text column
Load Sentence-BERT model
Generate product embeddings
Save processed products
Save embeddings as .npy file
```

---

### 2. `search_engine.py`

This file contains the `ProductSearchEngine` class.

Main responsibilities:

```text
Load processed product data
Load saved product embeddings
Load Sentence-BERT model
Apply filters
Generate query embedding
Calculate cosine similarity
Rank products
Return formatted results
```

---

### 3. `schemas.py`

This file defines API request and response schemas using Pydantic.

Main schemas:

```text
SearchRequest
ProductResult
SearchResponse
```

The schemas validate user input and ensure that API responses follow a consistent structure.

---

### 4. `main.py`

This file creates the FastAPI application and exposes the API endpoints.

Main endpoints:

```text
GET /
POST /search
```

---

## Validation Rules

The API validates the request before running the search.

Important validation rules:

```text
sources is required
sources cannot be empty
top_k must be between 1 and 50
min_rating must be between 0 and 5
min_price cannot be greater than max_price
at least query or category should be provided
```

Example validation logic:

```python
@model_validator(mode="after")
def validate_search_request(self):
    query_empty = not self.query or self.query.strip() == ""
    category_empty = not self.category or self.category.strip() == ""

    if query_empty and category_empty:
        raise ValueError("Provide either query or category.")

    if self.min_price is not None and self.max_price is not None:
        if self.min_price > self.max_price:
            raise ValueError("min_price cannot be greater than max_price.")

    return self
```

---

## Current Ranking Approach

The current version ranks products mainly by semantic similarity.

When a query is provided:

```text
Sentence-BERT query embedding
        ↓
Cosine similarity with product embeddings
        ↓
Products ranked by highest similarity score
```

When no query is provided and only filters are used, products can be sorted by rating and review count.

---

## Future Ranking Improvements

A stronger ranking formula can combine multiple signals:

```text
final_score =
semantic similarity
+ product rating
+ review count
+ price competitiveness
+ availability
+ source trust score
```

Example:

```text
final_score =
0.60 * similarity_score
+ 0.20 * rating_score
+ 0.10 * review_score
+ 0.10 * price_score
```

This would make the search engine more realistic because the best product should not depend only on text similarity.

---

## Future Improvements

Possible future enhancements include:

- React frontend for user-friendly search
- PostgreSQL database instead of CSV files
- FAISS for faster vector search
- Real product data from official APIs or affiliate feeds
- Product deduplication across shopping platforms
- Hybrid ranking using similarity, rating, reviews, price, and source trust
- User preference-based personalization
- LLM-based query understanding for automatic filter extraction
- Docker deployment
- Cloud deployment on AWS, GCP, Render, or Railway
- Scheduled product data refresh
- Product comparison page
- User search history and saved preferences

---

## Limitations

This is currently an MVP project and uses synthetic product data.

Current limitations:

```text
The dataset is synthetic
Prices and availability are not real-time
Product URLs are sample URLs
No frontend is included yet
No live shopping APIs are connected yet
No product deduplication is implemented yet
No user personalization is implemented yet
```

The system is designed so that the CSV dataset can later be replaced with official product APIs, affiliate feeds, or a real database.

---

## Resume Summary

This project can be described on a resume as:

```text
Built an AI-powered cross-platform product search engine using Sentence-BERT embeddings and cosine similarity to retrieve relevant products from user-selected shopping platforms, with support for category, source, price, and rating filters through a FastAPI backend.
```

Another version:

```text
Developed a FastAPI-based semantic product discovery system that unified product catalogs from multiple shopping platforms, generated Sentence-BERT embeddings for product descriptions, and ranked results using cosine similarity with filters for source, category, price, and customer rating.
```

---

## Author

Sreekar Meruva
