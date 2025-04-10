import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt

# === 参数设置 ===
zip_file = "bitcoin-historical-data.zip"
data_folder = "data"

# === Step 1: 下载 ZIP 文件 ===
if not os.path.exists(zip_file):
    print("📥 正在从 Kaggle 下载数据集...")
    result = os.system("kaggle datasets download -d mczielinski/bitcoin-historical-data")
    if result != 0:
        raise Exception("❌ Kaggle 下载失败，请检查 kaggle.json 配置")

# === Step 2: 解压 ZIP 文件 ===
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# 检查是否已经解压完成
extracted_files = os.listdir(data_folder)
if not extracted_files:
    print("📦 正在解压数据集...")
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(data_folder)
else:
    print("📂 已发现解压后的文件，跳过解压步骤")

# === Step 3: 自动查找 CSV 文件（递归搜索）===
csv_path = None
for root, dirs, files in os.walk(data_folder):
    for file in files:
        if file.endswith(".csv"):
            csv_path = os.path.join(root, file)
            break
    if csv_path:
        break

if not csv_path:
    raise FileNotFoundError("❌ 没有找到 CSV 文件，请手动检查 data/ 解压结果。")

print(f"✅ 找到数据文件：{csv_path}")

# === Step 4: 读取 CSV 数据 ===
df = pd.read_csv(csv_path)

# 检查是否包含 Timestamp 和 Close 字段
if 'Timestamp' not in df.columns or 'Close' not in df.columns:
    raise ValueError("❌ CSV 文件中不包含 Timestamp 或 Close 字段")

# === Step 5: 处理时间戳 ===
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', errors='coerce')
df.set_index('Timestamp', inplace=True)

# 删除缺失时间数据
df = df[df.index.notnull()]

# === Step 6: 每日平均收盘价 ===
daily_avg = df['Close'].resample('D').mean()

# === Step 7: 可视化 ===
plt.figure(figsize=(12, 6))
plt.plot(daily_avg, label='Daily Avg Close Price', color='dodgerblue')
plt.title('Bitcoin Daily Average Close Price (2012–2021)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
