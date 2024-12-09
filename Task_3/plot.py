import matplotlib.pyplot as plt
import pandas as pd

labeled_reviews = 'labeled_reviews.csv'
df = pd.read_csv(labeled_reviews)

grouped_df = df.groupby('talks_about').size().reset_index(name='frequency')
print(grouped_df)