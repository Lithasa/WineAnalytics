import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))

lemmatizer = WordNetLemmatizer()

# no use of stemmer
stemmer = PorterStemmer()

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

# remove stop words (e.g., "and", "the", "is")
def remove_stop_words(words):
  return [word for word in words if word not in stop_words]

# Lemmatization
def lemmatize_text(words):
  return [lemmatizer.lemmatize(word) for word in words]

# stemming - not used
def stem_text(words):
  return [stemmer.stem(word) for word in words]

# tokenize
def tokenize_text(text):
  return word_tokenize(text)

def clean_reviews(text) :
  text = to_lowercase(text)
  text = remove_special_characters(text)
  text = remove_extra_whitespace(text)
  tokens = tokenize_text(text)
  tokens = remove_stop_words(tokens)
  tokens = lemmatize_text(tokens)
  return tokens

# apply the cleaning method
df['cleaned_reviews'] = df['review'].apply(clean_reviews)

# remove review column
df = df.drop('review', axis=1)
print(df.hea)
# save the cleaned reviews to a CSV file
df.to_csv('cleaned_reviews.csv', index=False)