import pandas as pd
import re

wine_reviews = 'wine_reviews.csv'
df = pd.read_csv(wine_reviews)

# drop missing values
df = df.dropna(subset=['review'])

# remove punctuation, emojis, and other symbols
def remove_special_characters(text):
  return re.sub(r'[^a-zA-Z0-9\s]', '', text)

# convert all texts to lowercase
def to_lowercase(text):
  return text.lower()

# remove whitespaces
def remove_extra_whitespace(text):
  return re.sub(r'\s+', ' ', text).strip()

def clean_reviews(text) :
  text = to_lowercase(text)
  text = remove_special_characters(text)
  text = remove_extra_whitespace(text)
  return text

df['cleaned_reviews'] = df['review'].apply(clean_reviews)
print(df.head())