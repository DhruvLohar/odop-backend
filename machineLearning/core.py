import numpy as np
import pandas as pd
import io
import re
import nltk
import base64
from PIL import Image
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pandas.tseries.offsets import DateOffset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords


def adfuller_test(sales):
    result = adfuller(sales)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

def fit_sarimax_model(sales_data):
    model = sm.tsa.statespace.SARIMAX(sales_data, order=(1, 1, 1), seasonal_order=(1,1,1,12))
    results = model.fit()
    return results

def forecast_sales(results, last_date, steps=24):
    future_dates = [last_date + DateOffset(months=x) for x in range(1, steps + 1)]
    forecast_values = results.get_forecast(steps=steps).predicted_mean
    return future_dates, forecast_values

def generate_forecast_plot(df, future_dates, forecast_values):
    future_df = pd.DataFrame(index=future_dates, columns=df.columns)
    future_df['forecast'] = forecast_values
    combined_df = pd.concat([df, future_df])

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Sales'], label='Historical Sales')
    plt.plot(combined_df.index, combined_df['forecast'], color='red', label='Forecast')
    plt.title('Pottery Sales Forecast')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return plot_data

def clean_text(text, stemmer, stopword):
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = [word for word in text.split() if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split()]
    return " ".join(text)

