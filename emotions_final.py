# -*- coding: utf-8 -*-
"""Emotions - Final

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DMa_dnFzoa_Lw8jB8zYNGD-i61RaaZma
"""

!pip install nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

## reading emotions off of Tweets from Twitter because Twitter is always a hub of emotion

from google.colab import drive
drive.mount('/content/drive')
data = pd.read_csv('/content/drive/MyDrive/text.csv')
# df = df.dropna()
# df.head()

data = data.dropna()
data.dtypes

data.head()

x, y = data.text, data.label

"""graph of how many tweets are in each emotion category"""

# Value count of 'label'
count = data['label'].value_counts()

# Set the background color and theme
background_color = '#dddddd'
sns.set_theme(style="whitegrid", rc={"axes.facecolor": background_color, 'figure.facecolor': background_color})

# Create a figure with two subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 6), facecolor=background_color)

# Plot pie chart on the first subplot
palette = sns.color_palette("bright", len(count))
sns.set_palette(palette)
axs[0].pie(count, labels=count.index, autopct='%1.1f%%', startangle=140)
axs[0].set_title('Distribution of Categories', fontsize=15, fontweight='bold')

# Plot bar chart on the second subplot
sns.barplot(x=count.index, y=count.values, ax=axs[1], palette=palette)
axs[1].set_title('Count of Categories', fontsize=15, fontweight='bold')

# Adjust layout
plt.tight_layout()
plt.xlabel('relevant emotions')
plt.ylabel('amount of tweets')

# Show the plot
plt.show()

"""tokenization/pre-processing"""

x = x.str.lower()

tokens = x.apply(nltk.word_tokenize)

stop_words = set(stopwords.words("english"))
filtered_tokens = tokens.apply(lambda tokens: [word for word in tokens if word not in stop_words])

# stemmer = PorterStemmer()
# stemmed_tokens = filtered_tokens.apply(lambda filtered_tokens: [stemmer.stem(token) for token in filtered_tokens])

lemmatizer = WordNetLemmatizer()
lemmings = filtered_tokens.apply(lambda filtered_tokens: [lemmatizer.lemmatize(word) for word in filtered_tokens])

print(filtered_tokens)
# print(stemmed_tokens)
print(lemmings)

"""train/test split"""

x_train, x_test, y_train, y_test = train_test_split(data.text, data.label, test_size=0.2, random_state=127)

"""naive bayes - 86% accuracy"""

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
x_train_v = vectorizer.fit_transform(x_train)
x_test_v = vectorizer.transform(x_test)

thing = MultinomialNB()

thing.fit(x_train_v, y_train)

y_pred = thing.predict(x_test_v)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

