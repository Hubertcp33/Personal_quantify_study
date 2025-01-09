
#初始化
def initialize(context):
    g.security = "000006.XSHE" #股票代码 000006是深振业A
    g.short_count = 5
    g.long_count = 10
    g.unit = "1d"              #时间间隔1d=1天
    run_daily(market_open ,time="every_bar")


def market_open(context):
    #定义5日线
    short_ma = get_ma(g.security, g.short_count ,g.unit)
    #定义10日线
    long_ma = get_ma(g.security, g.long_count, g.unit)
    #金叉买入
    if get_golden_signal(short_ma, long_ma):
        print(f"金叉买入,MA{g.short_count}={short_ma},MA{g.long_count}={long_ma}")
        order_target(g.security ,100)
    #死叉卖出
    elif get_death_signal(short_ma, long_ma):
        print(f"死叉卖出,MA{g.short_count}={short_ma},MA{g.long_count}={long_ma}")
        order_target(g.security ,0)

#计算
def get_ma(security :str ,count :int ,unit :str )- >list:
    df = attribute_history(security, coun t +1, unit ,["close"])

    now_ma = df[1:coun t +1]["close"].rolling(count).mean()[-1]
    pre_ma = df[:count]["close"].rolling(count).mean()[-1]

    return [pre_ma ,now_ma]
#金叉判断
def get_golden_signal(
        short_ma :list,
        long_ma :list )- >bool:
    return (short_ma[0] < long_ma[0] and short_ma[1] >= long_ma[1])
#死叉判断
def get_death_signal(
        short_ma :list,
        long_ma :list )- >bool:
    return (short_ma[0] <= long_ma[0] and short_ma[1] > long_ma[1])



