# -*- coding: utf-8 -*-
"""
Google_Play_Reviews_Sentiment_Analysis.py

This script retrieves reviews for a specified Google Play app, performs sentiment analysis on each review,
and saves the results to a CSV file.
"""

import sys
import pandas as pd
import numpy as np
from google_play_scraper import reviews_all, Sort
import plotly.express as px
from transformers import pipeline

print("Starting the script...")

# Check if an app ID argument was provided
if len(sys.argv) < 2:
    print("Please provide the app ID as a command-line argument.")
    sys.exit(1)

# Get the app ID from command-line arguments
app_id = sys.argv[1]
print(f"App ID received: {app_id}")

# Wrap review fetching and analysis in try-except to catch errors
try:
    print("Fetching reviews...")
    skill_cat_app = reviews_all(
        app_id, 
        sleep_milliseconds=0, 
        lang='en', 
        country='us', 
        sort=Sort.NEWEST
    )
    print("Fetched reviews successfully.")
except Exception as e:
    print(f"Error fetching reviews: {e}")
    sys.exit(1)

# Normalize the JSON data to a Pandas DataFrame
try:
    dataframe = pd.json_normalize(skill_cat_app)
    print("Dataframe created successfully.")
    print("Dataframe head:\n", dataframe.head())
    print("\nAverage score:", dataframe['score'].mean())
except Exception as e:
    print(f"Error creating DataFrame: {e}")
    sys.exit(1)

# Initialize the sentiment analysis pipeline
try:
    print("Initializing sentiment analysis pipeline...")
    sentiment_analysis = pipeline("text-classification", model="siebert/sentiment-roberta-large-english")
    print("Sentiment analysis pipeline initialized successfully.")
except Exception as e:
    print(f"Error initializing sentiment analysis pipeline: {e}")
    sys.exit(1)

# Convert the 'content' column to string format if needed
dataframe['content'] = dataframe['content'].astype(str)

# Apply the sentiment analysis to each review's content
try:
    print("\nApplying sentiment analysis...")
    dataframe['result'] = dataframe['content'].apply(lambda x: sentiment_analysis(x))
    print("Sentiment analysis applied successfully.")
except Exception as e:
    print(f"Error during sentiment analysis: {e}")
    sys.exit(1)

# Extract the sentiment label and confidence score from the result
try:
    dataframe['sentiment'] = dataframe['result'].apply(lambda x: x[0]['label'])
    dataframe['confidence'] = dataframe['result'].apply(lambda x: x[0]['score'])

    # Display sentiment analysis results
    print("Sentiment analysis results head:\n", dataframe[['content', 'sentiment', 'confidence']].head())
    print("\nAverage confidence score:", dataframe['confidence'].mean())

    # Display sentiment distribution
    print("\nSentiment distribution:\n", dataframe['sentiment'].value_counts(normalize=True))
except Exception as e:
    print(f"Error processing sentiment results: {e}")
    sys.exit(1)

# Create a histogram of the sentiment results
try:
    figure = px.histogram(
        dataframe,
        x='sentiment',
        color='sentiment',
        text_auto=True,
        title='Sentiment Distribution of Reviews'
    )
    figure.show()
    print("Histogram displayed successfully.")
except Exception as e:
    print(f"Error creating histogram: {e}")

# Save the DataFrame to a CSV file
output_csv = 'skill_cat_reviews_sentiment.csv'
try:
    dataframe.to_csv(output_csv, index=False)
    print(f"Sentiment analysis results saved to {output_csv}")
except Exception as e:
    print(f"Error saving CSV file: {e}")

print("Completed...")