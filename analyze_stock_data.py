# pip install openai
# pip install matplotlib

from openai import OpenAI
import matplotlib.pyplot as plt
import datetime
import json

# OpenAI API 키 설정
client = OpenAI(
    # This is the default and can be omitted
    api_key='...'  # 본인의 OpenAI API 키를 입력하세요.
)

# 주식 데이터 (stock_data) 직접 입력 (가짜 데이터)
stock_data = {
    "Company_A": [
        {"Date": "2025-03-07", "Open": 150.25, "Close": 152.35},
        {"Date": "2025-03-08", "Open": 152.50, "Close": 151.75},
        {"Date": "2025-03-09", "Open": 151.60, "Close": 154.20},
        {"Date": "2025-03-10", "Open": 154.00, "Close": 155.10},
        {"Date": "2025-03-11", "Open": 155.20, "Close": 157.30},
        {"Date": "2025-03-12", "Open": 157.00, "Close": 158.10},
        {"Date": "2025-03-13", "Open": 158.30, "Close": 160.00}
    ],
    "Company_B": [
        {"Date": "2025-03-07", "Open": 210.50, "Close": 212.40},
        {"Date": "2025-03-08", "Open": 212.60, "Close": 213.70},
        {"Date": "2025-03-09", "Open": 213.80, "Close": 215.90},
        {"Date": "2025-03-10", "Open": 216.00, "Close": 217.50},
        {"Date": "2025-03-11", "Open": 217.60, "Close": 219.10},
        {"Date": "2025-03-12", "Open": 218.80, "Close": 220.50},
        {"Date": "2025-03-13", "Open": 220.80, "Close": 222.30}
    ]
}

# 데이터 출력 (가짜 데이터 확인용)
print("Company_A Data:")
print(json.dumps(stock_data["Company_A"], indent=2))

print("Company_B Data:")
print(json.dumps(stock_data["Company_B"], indent=2))

# 주식 가격 그래프 그리기
dates_A = [entry["Date"] for entry in stock_data["Company_A"]]
prices_A = [entry["Close"] for entry in stock_data["Company_A"]]

dates_B = [entry["Date"] for entry in stock_data["Company_B"]]
prices_B = [entry["Close"] for entry in stock_data["Company_B"]]

plt.figure(figsize=(10, 6))

# A 회사 주식 가격
plt.plot(dates_A, prices_A, label='Company_A Close Price', color='blue')

# B 회사 주식 가격
plt.plot(dates_B, prices_B, label='Company_B Close Price', color='green')

plt.title('Company_A vs Company_B Stock Prices (Last Week)')
plt.xlabel('Date')
plt.ylabel('Close Price (USD)')
plt.legend(loc='best')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# 그래프 출력
plt.show()

# 주식 분석 요청 (OpenAI API 사용)
def analyze_stock(ticker, data):
    prompt = f"Please analyze the stock price data for {ticker} for the last week. The data is as follows:\n{json.dumps(data, indent=2)}\n\nProvide an analysis of the stock performance. Answer in Korean."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content": "You are a helpful financial analyst."},
            {"role":"user", "content": prompt}
        ]
    )
   
    return response.choices[0].message.content

# A 회사와 B 회사 주식 분석
analysis_A = analyze_stock("Company_A", stock_data["Company_A"])
analysis_B = analyze_stock("Company_B", stock_data["Company_B"])

# 분석 결과 출력
print(f"\nCompany_A Stock Analysis:")
print(analysis_A)

print(f"\nCompany_B Stock Analysis:")
print(analysis_B)
