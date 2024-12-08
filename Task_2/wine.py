import ast
import pandas as pd

#3. methods to filter out outliers using the IQR method
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

# a function to convert a list in a string representation into an actual python list
def convert_to_list(cell):
    if isinstance(cell, str):
        cell = cell.strip()
        return ast.literal_eval(cell)
    return cell

# 1.1 Get CSV file paths.
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

# 3.1 Remove outliers
# 3.1.2 Remove outliers from Bold column
wine_df = remove_extreme_outliers_iqr(wine_df, 'Bold')
# 3.1.3 Remove outliers from Sweet column
wine_df = remove_extreme_outliers_iqr(wine_df, 'Sweet')
# 3.1.3 Remove outliers from Acidic column
wine_df = remove_extreme_outliers_iqr(wine_df, 'Acidic')

# 4.1 Add a country column
wine_df['Country'] = wine_df['Region'].str.split('/').str[0]
wine_df['Country'] = wine_df['Country'].str.strip()

# 4.2 Add a country_region column
wine_df['Country_region'] = wine_df['Region'].str.split('/').str[1]
wine_df['Country_region'] = wine_df['Country_region'].str.strip()

# 4.3 Separate food pairings to separate columns
wine_df['Food pairings'] = wine_df['Food pairings'].apply(convert_to_list)

# get all food pairings into a set 
all_food_pairings = set()
for food_pairing in wine_df['Food pairings'] : 
  all_food_pairings.update(food_pairing)

# create columns for each food pairing items and set them FALSE defaultly
for food_pairing in all_food_pairings :
  wine_df[food_pairing] = False

# iterte over each row and set available food pairing items TRUE in relavant columns
for index, row in wine_df.iterrows():
  matching_foods = row['Food pairings']
  for food in matching_foods:
    wine_df.at[index, food] = True

# 5. Remove the 'food pairings, Region and Grapes' columns
wine_df.drop(columns=['Food pairings', 'Region', 'Grapes'], inplace=True)
#print(wine_df)
wine_df.to_csv('wine.csv', index=False)