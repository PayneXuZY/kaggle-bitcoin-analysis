import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt

zip_file = "bitcoin-historical-data.zip"
data_folder = "data"
image_output = "sample_output.png"

# 下载数据
if not os.path.exists(zip_file):
    os.system("kaggle datasets download -d mczielinski/bitcoin-historical-data")

# 解压数据
if not os.path.exists(data_folder):
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(data_folder)

# 自动查找 CSV 文件
csv_path = None
for root, _, files in os.walk(data_folder):
    for file in files:
        if file.endswith(".csv"):
            csv_path = os.path.join(root, file)
            break
    if csv_path:
        break

if not csv_path:
    raise FileNotFoundError("❌ 没有找到 CSV 文件")

df = pd.read_csv(csv_path)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', errors='coerce')
df.set_index('Timestamp', inplace=True)
df = df[df.index.notnull()]
daily_avg = df['Close'].resample('D').mean()

# 生成图表并保存
plt.figure(figsize=(12, 6))
plt.plot(daily_avg, label='Daily Avg Close Price', color='dodgerblue', alpha=0.7)
plt.title('Bitcoin Daily Average Close Price (Auto-Generated)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(image_output)
