import pandas as pd
import requests


pd.set_option('expand_frame_repr', False)
def get_single_kline_data(symbol):
    kline_type = '1D'
    size = 10
    ticker = 'https://www.okx.com/api/v5/market/candles?instId={}&bar={}&limit={}'.format(symbol, kline_type, size)
    try:
        res_obj = requests.get(ticker, timeout=15)
    except Exception as e:
        print('错误！', e)
        return None

    kline_df = None

    if res_obj.status_code == 200:
        json_obj = res_obj.json()
        data_1 = json_obj.get('data', [])
        if 'error_code' in json_obj:
            print('错误码：{}'.format(json_obj['error_code']))
        else:
            raw_df = pd.DataFrame(data_1)
            if not raw_df.empty: 
                kline_df = raw_df.copy()
                kline_df.columns = ['datetime', '开盘价格', '最高价格', '最低价格', '收盘价格', '交易量', '计价货币的数量', '计价货币为单位', 'K线状态']
                kline_df['datetime'] = pd.to_datetime(kline_df['datetime'], unit='ms')
                kline_df['symbol'] = symbol.replace('_', '/').upper()
            else:
                print(f'获取的 {symbol} 数据为空')


    else:
        print('状态码：{}'.format(res_obj.status_code))
    return (kline_df)

def get_single_klines_data(symbols):
    '''klines_df = pd.DataFrame()
    for symbol in symbols:
        klines_df = get_single_kline_data(symbol)
        if klines_df is None:
            continue
        klines_df = pd.concat(klines_df,klines_df)
    return klines_df'''

    klines_df_list = []
    for symbol in symbols:
        kline_df = get_single_kline_data(symbol)
        if kline_df is not None:
            klines_df_list.append(kline_df)
    if klines_df_list:
        klines_df = pd.concat(klines_df_list, ignore_index=True)
    else:
        klines_df = pd.DataFrame()
    return klines_df


def main():
    #symbol = 'BTC-USD'
    #kline_df = get_single_kline_data(symbol)
    #print(kline_df)
    symbols = ['BTC-USD', 'ETH-USD', 'XRP-USD']
    klines_df = get_single_klines_data(symbols)
    klines_df.to_csv('./crptocoin_sample.csv', index=False)
if __name__ == '__main__':
    main()