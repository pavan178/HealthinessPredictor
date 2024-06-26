# -*- coding: utf-8 -*-
"""Advanced_ML_230049961.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MYkWAGuQ7_glyUVUtU0q93xc4bonhbcq

#1 Author
Student Name: Pavan Kumar Gondabal Ramakrishna

Student ID: 230049961

## 2 Problem formulation

We have The images of various dishes from different cusines, having attributes such as Taste, healthiness, ingredients, likliness etc and a Csv file containing the attributes

Based on the features such as 'Ingredients','Diet','Home_or_restaurant', Likeness, we will be prediting the 'Healthiness_rating_int'of the Dish.

I have selected these featrues as they are importent features based on how each attribute plays a major role for the healthiness of a dish when compared to other attributes in general

1.0 being the lowest and 5.0 being the heighest Healthiness_rating_int

We can also consider the images but the attributes have all the relevant data on the images which can be used as features, we can directly use the CSV file to build our model. Image processing takes huge amount of comutation time and features of the images might sometimes wont be enough to build a classification model such as food classification for healthiness rating
"""

#Install the mlend library
!pip install mlend

"""#3 Machine Learning pipeline

The Csv file from ML end library is being used as an input for our pipe line ,use ['Ingredients','Diet','Home_or_restaurant','Healthiness_rating_int','Likeness'] as input features, encode the catagorical features into numbers, Ingredients have been cleaned and lemmatization is used for preprocessing and TF-IDF method is being implimented to find the importand ingredients and vectorize the ingredient features, after pre processing of input features, we have 1635 columns as input

We will mount the google colab to drive in order to acces the dataset
"""

from google.colab import drive

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spkit as sp

from skimage import exposure
from skimage.color import rgb2hsv, rgb2gray
import skimage as ski

import mlend
from mlend import download_yummy_small, yummy_small_load

import os, sys, re, pickle, glob
import urllib.request
import zipfile

import IPython.display as ipd
from tqdm import tqdm
import librosa

drive.mount('/content/drive')

#We will use The csv file which has the attributes

df = pd.read_csv('/content/drive/MyDrive/Data/MLEnd/yummy/MLEndYD_image_attributes_benchmark.csv').set_index('filename')

df

df_sample= df[['Ingredients','Diet','Home_or_restaurant','Healthiness_rating_int','Likeness']]
#df_sample= df[['Ingredients','Home_or_restaurant','Healthiness_rating_int']]
#drop nan values
df_sample.dropna(inplace=True)

df_sample

import pandas as pd


# Check if the string contains 'home' and update accordingly
df_sample['Home_or_restaurant'] = df_sample['Home_or_restaurant'].apply(lambda x: 'home' if 'home' in x else 'restaurant')

# Display the updated DataFrame
print(df_sample)

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score



# Combine categorical features and ingredients
X_text = df_sample['Ingredients'].str.replace(',', ' ')
X_cat = pd.get_dummies(df_sample[['Diet', 'Home_or_restaurant','Likeness']], drop_first=True)
#X_cat = pd.get_dummies(df_sample[[ 'Home_or_restaurant']], drop_first=True)

X = pd.concat([X_text, X_cat], axis=1)
#X['Likeness_int'] = df_sample['Likeness_int']
y = df_sample['Healthiness_rating_int']

X

def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)

# Define a function to remove stop words


# Apply the functions to the 'Ingredients' column
X['Ingredients'] = X['Ingredients'].str.replace(r'\d+', '')  # Remove digits
 # Remove special characters

#X['Ingredients'] = X['Ingredients'].str.replace(r'\d+', '')  # Remove numbers
X['Ingredients'] = X['Ingredients'].str.replace('_', ' ')  # Replace underscores with spaces
X['Ingredients'] = X['Ingredients'].apply(remove_special_characters)
# Remove common words and exclude non-food ingredients
non_food_words = ['cups','cup','glass','water','cook','glasses','all','allpurpose', 'spoon','teaspoon','add','adjust','boil','heat','about','tablespoon','tablespoons','acid',  'acidity', 'agent','powder','paste','chopped','finely']  # Add more non-food words as needed

X['Ingredients']

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Function to lemmatize a sentence
def lemmatize_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Lemmatize each word, excluding stop words
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words if word.lower() not in stop_words]

    # Join the lemmatized words back into a sentence
    lemmatized_sentence = ' '.join(lemmatized_words)

    return lemmatized_sentence

# Apply lemmatization to the entire column
X['Ingredients'] = X['Ingredients'].apply(lemmatize_sentence)

# Display the DataFrame
print(X)

X['Ingredients'] = X['Ingredients'].apply(lambda x: ' '.join(word for word in x.split() if word not in non_food_words))

# Split words and tokenize
X['Ingredients'] = X['Ingredients'].apply(lambda x: ' '.join(x.split()))

for i in X['Ingredients']:
  print(i)

vectorizer = TfidfVectorizer()

ingredients_encoded = vectorizer.fit_transform(X['Ingredients'])

# Convert the encoded features to a DataFrame

ingredients_encoded

df_encoded = pd.DataFrame(ingredients_encoded.toarray(), columns=vectorizer.get_feature_names_out())




# Concatenate the original DataFrame with the encoded features
X1 = pd.concat([X.reset_index(drop=True), df_encoded], axis=1)
X1.set_index(X.index, inplace=True)
# Display the updated DataFrame
print(X1)

new_dataframe = X1.iloc[:, 2:].copy()

new_dataframe

"""# 4 Transformation stage

 we will use random forest classfier to reduce the dimentions of the features by keeping the improtent feature threshold to 0.01, which will eliminate the remaining features from 1633 columns, we will identify 22 columns
"""

# Assuming X is your DataFrame
from sklearn.ensemble import RandomForestClassifier

# Fit a RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(new_dataframe, y)  # Replace 'y' with your target variable

# Get feature importances
feature_importances = rf.feature_importances_

# Select top features based on importance scores
threshold = 0.01
selected_features = new_dataframe.columns[feature_importances > threshold]

# Apply the selection to the DataFrame
X_selected = new_dataframe[selected_features]

X_selected

"""#5 Modelling

We will be using ensabling technique and grid search to find best parameters and models among, random forest, SVC and logistic regression, as all these models are well known for classification problem.

#6 Methodology

We will be using 80:20 split on the entire datset for train and test data, the models will be trained on the train dataset using various classification models below
Based on the Accuracy score on train and test dataset, the model will also be assed on Confusion matrix ,Precision, recall etc.
"""

from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# Define the model (Random Forest Classifier in this example)
model = RandomForestClassifier()

# Define the parameter grid for grid search
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Define the stratified k-fold cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Use GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(model, param_grid, cv=cv, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get the best model from the grid search
best_model = grid_search.best_estimator_

# Make predictions on the test set
y_pred = best_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Display classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Display the best hyperparameters
print("Best Hyperparameters:", grid_search.best_params_)

from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

# Print classification report
#print("Classification Report:\n", classification_report(y_test, y_pred))

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
            xticklabels=np.unique(y), yticklabels=np.unique(y))
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# Define the model (Logistic Regression in this example)
model = LogisticRegression()

# Define the parameter grid for grid search
param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],  # Regularization parameter
    'penalty': ['l1', 'l2'],  # Regularization type
    'solver': ['liblinear'],  # Solver for optimization problem
}

# Define the stratified k-fold cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Use GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(model, param_grid, cv=cv, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get the best model from the grid search
best_model = grid_search.best_estimator_

# Make predictions on the test set
y_pred = best_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Display classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Display the best hyperparameters
print("Best Hyperparameters:", grid_search.best_params_)

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# Define the model (Support Vector Machine - SVM in this example)
model = SVC()

# Define the parameter grid for grid search
param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],  # Regularization parameter
    'kernel': ['linear', 'rbf', 'poly'],  # Kernel type
    'degree': [2, 3, 4],  # Degree of the polynomial kernel (if 'poly' is chosen)
}

# Define the stratified k-fold cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Use GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(model, param_grid, cv=cv, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get the best model from the grid search
best_model = grid_search.best_estimator_

# Make predictions on the test set
y_pred = best_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Display classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Display the best hyperparameters
print("Best Hyperparameters:", grid_search.best_params_)

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
            xticklabels=np.unique(y), yticklabels=np.unique(y))
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

"""#7 Dataset
Test data is used to make the predictions, we will use one of the sample data to make our predictions, below is the corelation matrix of the extracted featrues
"""

X_selected_matrix = X_selected.corr()

# Create the heatmap using the `heatmap` function of Seaborn
plt.figure(figsize=(15, 10))

# Create the heatmap
sns.heatmap(X_selected_matrix, cmap='coolwarm', annot=True)

# Show the plot
plt.show()

first_row = X_test.head(1)

# Display the first row
print("First Row of DataFrame:")
first_row

"""#8 Results
we will input and visualize the one of the image from input data and get the predictions for the same, our model rates the dish as 4.0 on healthiness scale from 1-5
"""

import cv2
from matplotlib import pyplot as plt

# Replace 'path/to/your/image.jpg' with the actual path to your image file
image_path = '/content/drive/MyDrive/Data/MLEnd/yummy/MLEndYD_images/002591.jpg'

# Read the image using OpenCV
image = cv2.imread(image_path)

# Display the image using matplotlib
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Optional: Turn off axis labels
plt.show()

"""The Above image referes to the 1st row of model input which is classifed below using the model we built"""

y_pred = best_model.predict(first_row)

#healthiness of the input image 002591.jpg
#predicted score
y_pred

#healthiness of the input image 002591.jpg

#actual score
y_test[0]

"""#9 Conclusions

We have created a feature extaraction and feature reduction transformation and built the model using various classification models, however, the accuracy of the model and confuion matrix says this can be improvised. The scope for improvement in the model, after trying to extract the features from the images such as textre , colour, the model didn't improve by huge number however, the attributes alone from csv file were able to prove better results, so I have only used the csv file in the classification model submission.

The classification results can be improved by extrating more usefulfeatures from images and complex CNN models which directly take images as input and provide classification results better than random forest or linear SVC, however the complexity of CNN architecture needs better understanding of the deep learning modelling
"""