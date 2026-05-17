from search_engine import ProductSearchEngine
import pandas as pd

def main():
    # search_engine = ProductSearchEngine()
    # query = "comfortable shoes for walking"
    # results = search_engine.search(query=query,top_k=5)
    
    products = pd.read_csv("data\cross_platform_products.csv")
    products_list = products['category'].unique().tolist()
    print(products_list)


if __name__== "__main__":
    main()