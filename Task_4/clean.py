import pandas as pd

wine_reviews = 'wine_reviews.csv'
df = pd.read_csv(wine_reviews)

print(df.head())