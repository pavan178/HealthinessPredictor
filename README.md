# Healthiness Predictor 🥗

## Problem Formulation 🍽️
We are presented with images of various dishes from different cuisines, each with attributes such as Taste, Healthiness, Ingredients, and Likeness. Alongside these images, we have a CSV file containing relevant attributes.

Our goal is to predict the 'Healthiness_rating_int' of each dish based on features like 'Ingredients', 'Diet', 'Home_or_restaurant', and Likeness. The 'Healthiness_rating_int' ranges from 1.0 (lowest) to 5.0 (highest).

## Machine Learning Pipeline 🛠️
We utilize the CSV file as the input for our machine learning pipeline. Using features such as 'Ingredients', 'Diet', 'Home_or_restaurant', 'Healthiness_rating_int', and 'Likeness', we preprocess the data. The categorical features are encoded, and preprocessing techniques like lemmatization are applied to 'Ingredients'. We employ the TF-IDF method to vectorize the ingredients. This results in 1635 columns as input.

## Transformation Stage 🔄

To reduce dimensionality, we employ a random forest classifier, setting the threshold for important features to 0.01. This process helps identify 22 significant columns, streamlining our feature set.

## Methodology 📊
We split the dataset into an 80:20 ratio for training and testing. Various classification models are trained on the training dataset. The model performance is evaluated based on accuracy scores, confusion matrix analysis, precision, recall, etc., on both the training and testing datasets.

## Dataset 📉
Test data is utilized for predictions. We visualize a sample image from the input data and obtain predictions. Additionally, we present the correlation matrix of the extracted features.

## Results 📈
After inputting and visualizing an image from the dataset, our model predicts a healthiness rating of 4.0 for the dish on a scale of 1-5.
 
