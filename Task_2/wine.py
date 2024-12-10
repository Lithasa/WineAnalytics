import ast
import pandas as pd

def remove_mild_outliers_iqr(df, column) :
  Q1 = df[column].quantile(0.25)
  Q3 = df[column].quantile(0.75)
  IQR = Q3 - Q1
  lower_bound = Q1 - 1.5 * IQR
  upper_bound = Q3 + 1.5 * IQR
  outlier_removed_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
  return outlier_removed_df

def remove_extreme_outliers_iqr(df, column) :
  Q1 = df[column].quantile(0.25)
  Q3 = df[column].quantile(0.75)
  IQR = Q3 - Q1
  lower_bound = Q1 - 3 * IQR
  upper_bound = Q3 + 3 * IQR
  outlier_removed_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
  return outlier_removed_df

def convert_to_list(cell):
  if isinstance(cell, str):
    cell = cell.strip()
    return ast.literal_eval(cell)
  return cell

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

wine_df = pd.concat(df_list, ignore_index=True)

wine_df = wine_df.drop_duplicates()

wine_df = wine_df[wine_df['Name'].notnull()]

wine_df = remove_extreme_outliers_iqr(wine_df, 'Bold')

wine_df = remove_extreme_outliers_iqr(wine_df, 'Sweet')

wine_df = remove_extreme_outliers_iqr(wine_df, 'Acidic')

wine_df['Country'] = wine_df['Region'].str.split('/').str[0]
wine_df['Country'] = wine_df['Country'].str.strip()

wine_df['Country_region'] = wine_df['Region'].str.split('/').str[1]
wine_df['Country_region'] = wine_df['Country_region'].str.strip()

wine_df['Food pairings'] = wine_df['Food pairings'].apply(convert_to_list)

all_food_pairings = set()
for food_pairing in wine_df['Food pairings'] : 
  all_food_pairings.update(food_pairing)

for food_pairing in all_food_pairings :
  wine_df[food_pairing] = False

for index, row in wine_df.iterrows():
  matching_foods = row['Food pairings']
  for food in matching_foods:
    wine_df.at[index, food] = True

wine_df.drop(columns=['Food pairings', 'Region', 'Grapes'], inplace=True)

wine_df['Year'] = wine_df['Name'].str.extract(r'(\b\d{4}\b)')
wine_df['Year'] = wine_df['Year'].str.strip()
wine_df['Year'] = wine_df['Year'].fillna('n.v.')

wine_df.to_csv('wine.csv', index=False)