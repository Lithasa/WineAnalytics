import pandas as pd

# 1.1 Get CVS file paths.
file_paths = [
  'Wine_Stats/Australia_Wine_Stats.csv',
  'Wine_Stats/Chile_Wine_Stats.csv', 
  'Wine_Stats/France_Wine_Stats.csv',
  'Wine_Stats/Italy_Wine_Stats.csv',
  'Wine_Stats/New Zealand_Wine_Stats.csv',
  'Wine_Stats/Portugal_Wine_Stats.csv',
  'Wine_Stats/Spain_Wine_Stats.csv',
  'Wine_Stats/USA_Wine_Stats.csv'
]

# 1.2 Load all CSV file paths and set each column's data type. 
df_list = [pd.read_csv(
  file, 
  sep=',', 
  header=0, 
  index_col=0, 
  dtype={
    'Name': str,
    'Rating': float,
    'Number of ratings': int,
    'Price': float,
    'Region': str,
    'Winery': str,
    'Wine style': str,
    'Alcohol content': float,
    'Grapes': str,
    'Food pairings': str,
    'Bold': float,
    'Tanin': float,
    'Sweet': float,
    'Acidic': float
  }) for file in file_paths]

# 1.3 Concatenate all files into a one 'wine_df' DataFrame
wine_df = pd.concat(df_list, ignore_index=True)

# 2.1 Remove duplicate records - consider all columns
wine_df = wine_df.drop_duplicates()

# 2.2 remove records with null names
wine_df = wine_df[wine_df['Name'].notnull()]

# 4.1 Add a country column
wine_df['Country'] = wine_df['Region'].str.split('/').str[0]

# 4.2 Add a country_region column
wine_df['Country_region'] = wine_df['Region'].str.split('/').str[1]

print(wine_df)