import pandas as pd
import yfinance as yf
from datetime import datetime, time, timedelta
import math

#get this tickers option chain
#count puts / calls that are over the money for each expiration, 

def putCallRatios(ticker) -> list:
    t = yf.Ticker(ticker)
    #print(ticker.options)
    dates = t.options
    #print(dates)

    ratio = []
    for date in dates:
        callOTM = 0
        putOTM = 0
        opt = t.option_chain(date)
        for index, row in opt.calls.iterrows():
            if row['inTheMoney'] == False:
                if math.isnan(row['volume']) and math.isnan(row['openInterest']):
                    break
                elif math.isnan(row['volume']):
                    callOTM += row['openInterest']
                elif math.isnan(row['openInterest']):
                    callOTM += row['volume']
                else:
                    callOTM += row['openInterest'] + row['volume']
        for index, row, in opt.puts.iterrows():
            #print(opt.puts)
            if row['inTheMoney'] == False:
                if math.isnan(row['volume']) and math.isnan(row['openInterest']):
                    break
                elif math.isnan(row['volume']):
                    putOTM += row['openInterest']
                elif math.isnan(row['openInterest']):
                    putOTM += row['volume']
                else:
                    putOTM += row['openInterest'] + row['volume']
                #print(putOTM)
        
        ratio.append(callOTM / putOTM)
            
        #print(opt.calls)
    return ratio

#each ratio is linearly weighted i.e. each expiration date matters 
def linSentiment(ratio) -> str:
    avg = sum(ratio) / len(ratio)
    
    #weird distribution here bc its modeled after a/b
    if avg > 1 and avg <= 2:
        return 'weak positive sentiment'
    elif avg > 2:
        return 'strong positive sentiment'
    elif avg <= 1 and avg > .5:
        return 'weak negative sentiment'
    elif avg <= .5:
        return 'strong negative sentiment'

#each ratio is exponentially weighted i.e. each further expieration date matters more
#therefore if the ratio is significant it will be changed to a larger degree by the weighting
def expSentiment(ratio) -> str:
    decay = 1.03
    weighted_ratio = [ratio[0]]
    for x in range(1, len(ratio)):
        weighted_ratio.append((decay ** x) * ratio[x])
    
    exp_avg = sum(weighted_ratio) / len(ratio)

    #weird distribution here bc its modeled after a/b
    if exp_avg > 1 and exp_avg <= 2:
        return 'weak positive sentiment'
    elif exp_avg > 2:
        return 'strong positive sentiment'
    elif exp_avg <= 1 and exp_avg > .5:
        return 'weak negative sentiment'
    elif exp_avg <= .5:
        return 'strong negative sentiment'
    
    
