from transformers import pipeline
from tqdm import tqdm
import pandas as pd

cleaned_reviews = 'cleaned_reviews.csv'
df = pd.read_csv(cleaned_reviews)

classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
candidate_labels = ["talks about food combinations", "talks about taste", "talks about value for money", "other"]

tqdm.pandas()

df['talks_about'] = df['cleaned_reviews'].progress_apply(lambda x: classifier(x, candidate_labels)['labels'][0])

df.to_csv('labeled_reviews.csv', index=False)

# if transformer pipeline shows and import error due to numpy version mismatch,
# pip install numpy<2
# pip install --upgrade transformers torch pybind11