import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset
import io
import base64
from PIL import Image
from core import *

def forecast_pottery_sales(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df.columns = ["Month", "Sales"]
    df = df.dropna()
    df['Month'] = pd.to_datetime(df['Month'])
    df.set_index('Month', inplace=True)

    adfuller_test(df['Sales'])

    results = fit_sarimax_model(df['Sales'])

    future_dates, forecast_values = forecast_sales(results, df.index[-1], steps=24)
    plot_data = generate_forecast_plot(df, future_dates, forecast_values)

    next_month = future_dates[6]
    next_month_forecast = forecast_values[6]

    forecast_data = {
        'next_month': next_month.strftime('%B %Y'),
        'forecast': round(next_month_forecast, 2),
        'plot': plot_data
    }

    return forecast_data

# Example usage:
result = forecast_pottery_sales('./csv/pottery-sales.csv')
print(f"Forecast for {result['next_month']}: {result['forecast']}")
img = Image.open(io.BytesIO(base64.b64decode(result['plot'])))
plt.imshow(img)
plt.axis('off')
plt.show()
