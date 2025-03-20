"""
아래 코드를 생성하기 위한 프롬프트:
1. 1분마다 값이 생성되는 1시간짜리 시계열 데이터를 생성하고, 그 안에 이상 현상이 두번은 있어야돼. openai api 를 사용해서 이상현상을 탐지할 수 있는 파이선 코드를 생성해줘
2. 데이터 생성은 잘했어. 이 데이터를 openai 에 넣고 데이터를 분석할 수 있는 프롬프트와 코드를 파이선으로 새성해줘

한번에 동작하는 코드는 잘 안나옴. 디버깅 필수!
"""


!pip install statsmodels
import pandas as pd
import numpy as np
from openai import OpenAI
import matplotlib.pyplot as plt
import datetime
import json

# 1시간짜리 시계열 데이터 생성
index = pd.date_range('2022-01-01 00:00:00', periods=60, freq='1min')
data = np.random.normal(0, 1, 60)  # 평균 0, 표준편차 1의 정규분포 데이터
df = pd.DataFrame(data, index=index, columns=['value'])

# 이상 현상 추가 (두번)
df.loc['2022-01-01 00:15:00', 'value'] = 5  # 첫 번째 이상 현상
df.loc['2022-01-01 00:45:00', 'value'] = 10  # 두 번째 이상 현상

# OpenAI API를 사용하여 이상 현상 탐지
client = OpenAI(
    # This is the default and can be omitted
    api_key='...'  # 본인의 OpenAI API 키를 입력하세요.
)

def analyze_data(df):
    prompt = "Analyze the following time series data, detect anomalies, and explain it.(Answer in Korean):\n\n" + df.to_csv(index=False)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content": "You are a helpful data analyst."},
            {"role":"user", "content": prompt}
        ]
    )
   
    return response.choices[0].message.content
    

data = analyze_data(df)
print("Anomaly Detection Result:")
print(data)

# 이상 현상 탐지 결과를 기반으로 시각화
import matplotlib.pyplot as plt

# 이상 현상 탐지 (OpenAI API를 사용하지 않고)
from statsmodels.stats.outliers_influence import summary_table
import matplotlib.pyplot as plt

# 이상 현상 탐지
df['z_score'] = (df['value'] - df['value'].mean()) / df['value'].std()
anomaly = df[(df['z_score'] > 2) | (df['z_score'] < -2)]

# 결과 출력
print(df.to_markdown())
print("\nAnomaly Detection Result:")
print(anomaly.to_markdown())

# 시각화
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['value'], label='Original')
plt.plot(anomaly.index, anomaly['value'], label='Anomaly')
plt.legend()
plt.show()
