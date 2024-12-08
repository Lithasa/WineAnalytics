import pandas as pd

cleaned_reviews = 'cleaned_reviews.csv'
df = pd.read_csv(cleaned_reviews)
print(df.head(10))