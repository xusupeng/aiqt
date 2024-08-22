import ccxt
import datetime
import pandas as pd

# 创建 Binance 交易所对象
binance = ccxt.binance({
    'enableRateLimit': True,  # 启用交易所的频率限制
})

# 定义 ETH-USD 交易对和时间框架
symbol = 'ETHUSD_PERP'
time_frame = '1d'  # 1 天的时间框架

# 获取最近100天的数据
days_count = 100
end_time = int(datetime.datetime.now().timestamp())
start_time = end_time - days_count * 24 * 60 * 60

# 从 Binance 获取数据
since = None # 从最早的数据开始
ohlcvs = []
# 循环直到获取所有需要的数据
while True:
    # 如果这是第一个请求，since 应为 None
    if since is None:
        since = start_time * 1000  # Binance API 需要时间戳以毫秒为单位
    # 准备请求参数
    params = {
        'symbol': symbol,
        'interval': time_frame,
        'limit': 1500,  # Binance API 允许的最大 limit 值
        'startTime': since,
    }

    # 如果设置了 end_time，添加到请求参数中
    if end_time is not None:
        params['endTime'] = end_time * 1000

    # 从 Binance 获取数据
    response = binance.fetch_ohlcv(symbol, time_frame, since=since, params=params)

    # 将获取的数据添加到列表
    ohlcvs.extend(response)

    # 如果获取的数据少于 limit，则认为已经获取完数据
    if len(response) < 1500:
        break

    # 更新 since 为最后一条数据的时间戳 + 1 毫秒，避免重复
    since = response[-1][0] + 1

# 转换数据为 DataFrame
# 假设返回的数据包括交易量作为第 6 列
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
df = pd.DataFrame(ohlcvs, columns=columns)

# 如果只需要 5 列数据，可以删除第 6 列（交易量）
# df = df.drop(columns=['volume'])

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# 保存数据到 CSV 文件
csv_filename = 'binance_eth_usd_ohlcv.csv'
df.to_csv(csv_filename, index=False)

# 打印数据保存的文件名
print(f'Data saved to {csv_filename}')