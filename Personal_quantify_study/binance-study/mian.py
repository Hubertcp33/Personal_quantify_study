import ccxt
import time
import pandas as pd

pd.set_option('display.max_columns', None)

binance_exchange = ccxt.binance({
    'timeout': 30000,  # 设置为30秒
})

def main():

    binance_exchange = ccxt.binance({
        'timeout': 60000,
        'enableRateLimit': True,
    })

    markets = binance_exchange.load_markets()

    market_a = 'BTC'
    market_b = 'ETH'

    symbol = list(markets.keys())

    symbols_df = pd.DataFrame(data=symbol, columns=['symbol'])

    base_quote_df = symbols_df['symbol'].str.split(pat='/', expand=True)
    base_quote_df.columns = ['base', 'quote']

    base_a_list = base_quote_df[base_quote_df['base'] == market_a]['base'].values.tolist()
    base_b_list = base_quote_df[base_quote_df['base'] == market_b]['base'].values.tolist()

    common_base_list = list(set(base_a_list).intersection(set(base_b_list)))
    print('{}和{}共有{}个相同的计价货币'.format(market_a, market_b, len(common_base_list)))



    columns = ['Market A',
               'Market B',
               'Market C',
               'P1',
               'P2',
               'P3',
               'Profit(%)']
    results_df = pd.DataFrame(columns=columns)

    last_min = binance_exchange.milliseconds() - 60 * 1000

    for base_coin in common_base_list:
        market_c = base_coin
        market_a2b_symbol = '{}/{}'.format(market_b, market_a)
        market_b2c_symbol = '{}/{}'.format(market_c, market_b)
        market_a2c_symbol = '{}/{}'.format(market_c, market_c)

        market_a2b_kline = binance_exchange.fetch_ohlcv(market_a2b_symbol, since=last_min, limit=1 ,timeframe='1m')
        market_b2c_kline = binance_exchange.fetch_ohlcv(market_b2c_symbol, since=last_min, limit=1 ,timeframe='1m')
        market_a2c_kline = binance_exchange.fetch_ohlcv(market_a2c_symbol, since=last_min, limit=1 ,timeframe='1m')

        if len(market_a2b_kline) == 0 or len(market_b2c_kline) == 0 or len(market_a2c_kline) == 0:
            continue

        p1 = market_a2b_kline[0][4]
        p2 = market_b2c_kline[0][4]
        p3 = market_a2c_kline[0][4]

        profit = (p3 / (p1 * p2) - 1) * 1000

        results_df = results_df.append({
            'Market A': market_a,
            'Market B': market_b,
            'Market C': market_c,
            'P1': p1,
            'P2': p2,
            'P3': p3,
            'Profit(%)': profit,
        }, ignore_index=True)

        print(results_df.tail(1))
        time.sleep(binance_exchange.rateLimit / 1000)


    results_df.to_csv('./tri_arbitrage_results.csv', index=None)

if __name__ == '__main__':
    main()
