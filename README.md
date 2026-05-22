# Grape to Glass: Wine Analytics Dashboard

## Overview

**Grape to Glass** is a wine analytics project developed to analyze wine data from eight countries and customer reviews to identify trends, patterns, and actionable business insights.

The project includes data cleaning, feature extraction, customer review preprocessing, review classification, and an interactive analytics dashboard. The dashboard helps users understand relationships between wine price, rating, alcohol content, region, customer reviews, and other important wine-related factors.

This project was completed as part of a data analytics case study focused on transforming raw wine datasets into meaningful visual and strategic insights.

---

## Key Objectives

The main objectives of this project are to:

- Merge wine datasets from eight countries into a single structured dataset.
- Clean and prepare raw wine data for analysis.
- Remove duplicates, null values, irrelevant columns, and outliers.
- Extract useful features such as food pairings, country, region, and manufactured year.
- Preprocess customer reviews for text analysis.
- Classify customer reviews using machine learning and NLP techniques.
- Build an interactive dashboard using Python and Plotly Dash.
- Provide strategic insights based on wine pricing, ratings, alcohol content, and customer feedback.

---

## Features

### Data Preparation

The data preparation process included:

- Merging eight CSV files into one dataset.
- Removing duplicate records.
- Handling missing values.
- Removing unnecessary columns.
- Handling outliers.
- Extracting food pairing details.
- Extracting country and regional information.
- Extracting manufactured year from available data.

### Review Preprocessing

Customer reviews were cleaned and prepared before classification.

The preprocessing steps included:

- Removing null values.
- Removing special characters.
- Converting text to lowercase.
- Removing stop words.
- Applying lemmatization.
- Tokenizing customer reviews.

Some preprocessing techniques, such as stemming, were skipped where they were not suitable for the analysis.

### Sentiment Analysis and Review Classification

The sentiment analysis and review classification process was organized into separate scripts for better code management.

| Script | Purpose |
|---|---|
| `clean.py` | Cleans the dataset and produces the cleaned output |
| `label.py` | Uses a machine learning model to classify reviews into categories |
| `plot.py` | Generates visualizations using the labelled review data |

The project uses transformer-based models for review classification. Since the classification process can take a long time, the `tqdm` library is used to show progress while processing reviews.

### Interactive Dashboard

The dashboard was developed using **Plotly Dash**, **Pandas**, and **NumPy**.

The dashboard includes:

- Interactive visualizations.
- Price vs rating analysis.
- Rating vs alcohol content analysis.
- Customer review-based insights.
- Descriptions below charts for better interpretation.
- Separate CSS styling for cleaner code structure and better maintainability.

---

## Technologies Used

### Programming Language

- Python

### Libraries and Frameworks

- Pandas
- NumPy
- NLTK
- Transformers
- tqdm
- Matplotlib
- Plotly
- Dash

### Tools

- Jupyter Notebook
- Python scripts
- CSV datasets
- CSS
- Git and GitHub

---

## Suggested Project Structure

```text
grape-to-glass-wine-analytics/
│
├── data/
│   ├── raw/
│   │   ├── country_1.csv
│   │   ├── country_2.csv
│   │   └── ...
│   │
│   └── processed/
│       ├── cleaned_wine_data.csv
│       └── labelled_reviews.csv
│
├── notebooks/
│   ├── data_preparation.ipynb
│   ├── review_preprocessing.ipynb
│   └── analysis.ipynb
│
├── scripts/
│   ├── clean.py
│   ├── label.py
│   └── plot.py
│
├── dashboard/
│   ├── app.py
│   └── assets/
│       └── style.css
│
├── extra/
│   └── model_training_experiments/
│
├── requirements.txt
├── README.md
└── .gitignore
```

> Note: The folder names and file names can be changed depending on your actual project structure.

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/grape-to-glass-wine-analytics.git
```

```bash
cd grape-to-glass-wine-analytics
```

Replace `your-username` with your GitHub username.

---

### 2. Create a Virtual Environment

#### For Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

#### For macOS / Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

### 3. Install Required Dependencies

If the project has a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt` file, install the main libraries manually:

```bash
pip install pandas numpy nltk transformers tqdm matplotlib plotly dash
```

---

### 4. Download NLTK Resources

Run Python:

```bash
python
```

Then run:

```python
import nltk
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")
```

Exit Python:

```python
exit()
```

---

## How to Run the Project

### Option 1: Run Jupyter Notebooks

If the project uses notebooks, start Jupyter Notebook:

```bash
jupyter notebook
```

Then open the notebooks inside the `notebooks/` folder and run them step by step.

Example notebooks:

```text
data_preparation.ipynb
review_preprocessing.ipynb
analysis.ipynb
```

---

### Option 2: Run Python Scripts

#### Step 1: Clean the Dataset

```bash
python scripts/clean.py
```

This script cleans the raw dataset and saves the cleaned output.

#### Step 2: Classify Customer Reviews

```bash
python scripts/label.py
```

This script classifies customer reviews using the selected machine learning or transformer-based model.

> Note: This step may take a long time depending on the dataset size and computer performance.

#### Step 3: Generate Charts

```bash
python scripts/plot.py
```

This script creates visualizations based on the labelled and cleaned data.

---

### Option 3: Run the Dashboard

Move to the dashboard folder:

```bash
cd dashboard
```

Run the Dash application:

```bash
python app.py
```

After running the command, open the local server URL shown in the terminal.

Usually, it will look like this:

```text
http://127.0.0.1:8050/
```

Open this link in your browser to view the dashboard.

---

## Example Requirements File

If you do not already have a `requirements.txt` file, you can create one with the following content:

```text
pandas
numpy
nltk
transformers
tqdm
matplotlib
plotly
dash
jupyter
```

You can generate a requirements file automatically using:

```bash
pip freeze > requirements.txt
```

---

## Key Insights

The analysis produced the following key insights:

- The average price vs rating chart shows a moderate positive linear relationship.
- In general, wines with higher prices tend to receive higher ratings.
- Alcohol content does not directly influence wine ratings.
- Customer reviews provide useful information for understanding wine quality, customer preferences, and product perception.
- Combining structured wine data with review analysis can support better business decision-making.

---

## Future Improvements

Future improvements for this project include:

- Fine-tuning the review classification model using supervised multi-label learning.
- Selecting a sample of customer reviews and manually labelling them.
- Training a custom transformer-based model using labelled review data.
- Improving the accuracy of review classification.
- Adding more dashboard filters such as country, region, price range, rating range, and wine type.
- Deploying the dashboard online using a cloud platform.
- Adding automated data processing pipelines.
- Improving UI/UX design of the dashboard.

---

## Learning Outcomes

Through this project, we gained practical experience in:

- Data cleaning and preprocessing.
- Working with multiple CSV datasets.
- Natural Language Processing.
- Review classification using machine learning models.
- Python-based data analysis.
- Dashboard development using Plotly Dash.
- Data visualization and insight generation.
- Code organization and separation of concerns.
- Converting raw data into business insights.

---



## License

This project is for academic and educational purposes.

---

## Conclusion

**Grape to Glass** demonstrates how data analytics, natural language processing, and interactive dashboards can be used to understand wine-related data and customer reviews. By combining structured wine data with review-based insights, this project provides a useful foundation for business analysis, customer preference identification, and strategic decision-making in the wine industry.
