import pyupbit
import time
import datetime
from pandas import Series
import pandas as pd
import numpy as np

def get_target_ticker():
    df = pd.DataFrame(columns=['st','price_per','volume_per'])

    for i in range(len(ticker_num)):
        try:
            ohlcv=pyupbit.get_ohlcv(ticker_num[i][1],interval="minute1", count=cnt)
            data=[{'st':ticker_num[i][1],
                   'price_per':(pyupbit.get_current_price(ticker_num[i][1])-ohlcv['close'].mean())/ohlcv['close'].mean(),
                   'volume_per':(ohlcv['volume'].iloc[-1]-ohlcv['volume'].mean())/ohlcv['volume'].mean()}]
            df=df.append(data,ignore_index=True)
        except:
            time.sleep(0.05)

    pp_idx = df['price_per'].idxmax()
    target_ticker=df['st'].iloc[pp_idx]

    pp_max = df['price_per'].max()
    tt_vp = df['volume_per'].iloc[pp_idx]
    
    # print('pp_max:',pp_max)
    # print('tt_vp:',tt_vp)
    # print('tt:',target_ticker)
    # print(df)
    
    return target_ticker,pp_max,tt_vp
  

def get_start_time(st):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(st, interval="minute1", count=1)
    start_time = df.index[0]
    return start_time

access = "zK6Yre0yX54zwLMGsUrxLt8nR6XdLCBgu1IkbAEH"
secret = "8sn3aeh88ts20LWeDSotmerbFyKnueJlxAyV2Oio"
upbit = pyupbit.Upbit(access, secret)

print("autotrade start")
i=0

cnt=20
ticker_num=[[0,"KRW-POLY"],
            [1,"KRW-CVC"],
            [2,"KRW-ARDR"],
            [3,"KRW-STMX"],
            [4,"KRW-HIVE"],
            [5,"KRW-AXS"],
            [6,"KRW-POWR"],
            [7,"KRW-IOST"],
            [8,"KRW-ELF"],
            [9,"KRW-BCHA"],
            [10,"KRW-BTC"],
            [11,"KRW-ETC"],
            [12,"KRW-BTT"],
            [13,"KRW-ETH"],
            [14,"KRW-GLM"],
            [15,"KRW-SAND"],
            [16,"KRW-FCT2"],
            [17,"KRW-MOC"],
            [18,"KRW-TON"],
            [19,"KRW-HUNT"],
            [20,"KRW-AERGO"],
            [21,"KRW-MVL"],
            [22,"KRW-MTL"],
            [23,"KRW-ORBS"],
            [24,"KRW-HUM"],
            [25,"KRW-LOOM"],
            [26,"KRW-CRE"],
            [27,"KRW-AHT"],
            [28,"KRW-TT"],
            [29,"KRW-UPP"],
            [30,"KRW-DOT"],
            [31,"KRW-QKC"],
            [32,"KRW-LTC"],
            [33,"KRW-MFT"],
            [34,"KRW-AQT"],
            [35,"KRW-RFR"],
            [36,"KRW-MBL"],
            [37,"KRW-ARK"],
            [38,"KRW-MLK"],
            [39,"KRW-STRAX"],
            [40,"KRW-CBK"],
            [41,"KRW-IQ"],
            [42,"KRW-SC"],
            [43,"KRW-GRS"]]

def get_balance(st):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == st:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0



# 자동매매 시작
while True:
    i=i+1
    gtt=get_target_ticker()
    st=gtt[0]
    pp_max=gtt[1]
    st_vp=gtt[2]

    krw = get_balance('KRW')
    print('                           KRW:',krw)
    
    if(pp_max>0.01)and(st_vp>0.5):
        print("                        try:",i,", get affoldable coin:",st,':',upbit.get_balance(st))

        
        try:
            # now = datetime.datetime.now()
            # start_time = get_start_time(st)
            # end_time = start_time + datetime.timedelta(seconds=5)
            # print("time check!")
            # if start_time < now < end_time:
            if krw > 5000:
                upbit.buy_market_order(st, krw*0.9995)
                print("                                   buy coin!")
                print("                                  :",upbit.get_avg_buy_price(st))
            
            if((upbit.get_avg_buy_price(st)) and (pyupbit.get_current_price(st)>=upbit.get_avg_buy_price(st) * 1.0025)) or pyupbit.get_current_price(st)<= upbit.get_avg_buy_price(st) * 0.985 :
                coin = upbit.get_balance(st)
                if coin > 0.00008:
                    upbit.sell_market_order(st, coin*0.9995)
                    print("                                   sell coin!")
        except:
            time.sleep(0.05)
    else:
        print("                      try:",i,", no affoldable coin")
