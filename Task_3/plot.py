import matplotlib.pyplot as plt
import pandas as pd

labeled_reviews = 'labeled_reviews.csv'
df = pd.read_csv(labeled_reviews)

grouped_df = df.groupby('talks_about').size().reset_index(name='frequency')
print(grouped_df)

fig, ax = plt.subplots()
ax.pie(grouped_df['frequency'], labels=grouped_df['talks_about'], autopct='%1.2f%%')

plt.title('Distribution of Review Categories')
plt.show()