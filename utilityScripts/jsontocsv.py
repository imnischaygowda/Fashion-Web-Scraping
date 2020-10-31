import pandas as pd
df = pd.read_json (r'jsonFiles\prepdata_BOYNER.json')
df.to_csv(r'final_products_csv\product_BOYNER.csv')


# df.to_csv (r'Path where the new CSV file will be stored\New File Name.csv', index = None)