import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_price(string):
    ticker, history = string.split(",")
    history = int(history)
    ##今天
    end_date = datetime.today()
    start_date = end_date - timedelta(days=history)
    
    print(string)
    # 檢查 ticker 是否已經包含後綴，根據這一點來決定市場
    if ticker.endswith(".NS"):  # 假設以 ".NS" 代表印度市場
        suffix = ".NS"
    elif ticker.endswith(".TW"):  # 假設以 ".TW" 代表台灣市場
        suffix = ".TW"
    elif ticker.isalpha() and len(ticker) < 5:  # 假設沒有後綴且長度較短是美股
        suffix = ""  # 默認美國市場股票代碼沒有後綴
    else:
        suffix = ""  # 預設其他市場

    # 確保ticker有正確的後綴
    ticker = ticker + suffix if not ticker.endswith(suffix) else ticker

    # 獲取股票數據
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)


    # 選擇需要的列：關閉（Close）和成交量（Volume）
    df = df[["Close", "Volume"]]

    # 處理索引，將其轉換為日期格式
    df.index = [str(x).split()[0] for x in list(df.index)]  # 格式化索引
    df.index.rename("Date", inplace=True)

    # 返回 DataFrame
    # return df.to_string
    return f"股票 {ticker} 的过去 {history} 天的价格如下：\n{df.to_string}"

# 保存 DataFrame 到 CSV 文件
def save_to_csv(df, filename):
    df.to_csv(filename)
    print(f"Data has been saved to {filename}")



# 保存為 CSV 文件
# save_to_csv(stock_data, "Fstock_data.csv")
