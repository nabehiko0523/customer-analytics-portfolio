import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Loading sales history data
df = pd.read_csv('data/sales_history.csv')
df['date'] = pd.to_datetime(df['date'])

# Summary monthly sales
monthly_sales = df.groupby(df['date'].dt.to_period('M'))['sales_amount'].sum().reset_index()
monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()

# Feature engineering
monthly_sales['month_num'] = range(len(monthly_sales))
monthly_sales['month'] = monthly_sales['date'].dt.month
monthly_sales['quarter'] = monthly_sales['date'].dt.quarter

# Train/Test split (last 6 months for testing)
train = monthly_sales[:-6]
test = monthly_sales[-6:]

# Training the model
features = ['month_num', 'month', 'quarter']
X_train = train[features]
y_train = train['sales_amount']
X_test = test[features]
y_test = test['sales_amount']

model = LinearRegression()
model.fit(X_train, y_train)

# Forecasting
train['predicted'] = model.predict(X_train)
test['predicted'] = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, test['predicted'])
rmse = np.sqrt(mean_squared_error(y_test, test['predicted']))
mape = np.mean(np.abs((y_test - test['predicted']) / y_test)) * 100

print("=" * 60)
print("SALES FORECAST MODEL RESULTS")
print("=" * 60)
print(f"\nModel: Linear Regression")
print(f"Training Period: {train['date'].min().strftime('%Y-%m')} to {train['date'].max().strftime('%Y-%m')}")
print(f"Test Period: {test['date'].min().strftime('%Y-%m')} to {test['date'].max().strftime('%Y-%m')}")
print(f"\nMetrics:")
print(f"  MAE:  ¥{mae:,.0f}")
print(f"  RMSE: ¥{rmse:,.0f}")
print(f"  MAPE: {mape:.2f}%")

# Visulaization
plt.figure(figsize=(14, 6))
plt.plot(train['date'], train['sales_amount'], 'b-', label='Actual (Train)', linewidth=2)
plt.plot(test['date'], test['sales_amount'], 'g-', label='Actual (Test)', linewidth=2)
plt.plot(train['date'], train['predicted'], 'b--', label='Predicted (Train)', alpha=0.7)
plt.plot(test['date'], test['predicted'], 'r--', label='Predicted (Test)', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Sales Amount (¥)')
plt.title('Sales Forecast: Actual vs Predicted')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/screenshots/sales_forecast.png', dpi=150)
print("\n✓ Chart saved: docs/screenshots/sales_forecast.png")

# Store results
forecast_results = pd.concat([train, test])
forecast_results.to_csv('data/sales_forecast_results.csv', index=False)
print("✓ Results saved: data/sales_forecast_results.csv")