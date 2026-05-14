from search_engine import ProductSearchEngine

def main():
    search_engine = ProductSearchEngine()
    query = "comfortable shoes for walking"
    results = search_engine.search(query=query,top_k=5)
    print(results)


if __name__== "__main__":
    main()