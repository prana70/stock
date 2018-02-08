#coding: utf-8

def InterValue(Growth, EarningsPerShare, DiscountRate, PriceEarningsRatio): #成长股内在价值计算
  #InterValue 内在价值，本函数返回值
  #Growth 增长率
  #EarningsPerShare 每股收益
  #DiscountRate  折现率
  #PriceEarningRatio 基准市盈率
  #V1, V2, V3, V4, V 不同部份增长率现值
  
  #分部增长率现值计算
    if Growth > 2:                                   #增长率高于200%
        V1 = (1 + 0.5) ** 2 / (1 + DiscountRate) ** 2
        V2 = (1 + 0.5) ** 1.5 / (1 + DiscountRate) ** 1.5
        V3 = (1 + 1) / (1 + DiscountRate)
        V4 = (1 + Growth - 2) ** 0.5 / (1 + DiscountRate) ** 0.5
    elif Growth > 1 : #增长率高于100%但小于等于150%
        V1 = (1 + 0.5) ** 2 / (1 + DiscountRate) ** 2
        V2 = (1 + 0.5) ** 1.5 / (1 + DiscountRate) ** 1.5
        V3 = (1 + Growth - 1) / (1 + DiscountRate)
        V4 = 0
    elif Growth > 0.5 :                               #增长率高于50%但小于等于100%
        V1 = (1 + 0.5) ** 2 / (1 + DiscountRate) ** 2
        V2 = (1 + Growth - 0.5) ** 1.5 / (1 + DiscountRate) ** 1.5
        V3 = 0
        V4 = 0
    elif Growth >=0:                                                  #增长率小于等于50%
        V1 = (1 + Growth) ** 2 / (1 + DiscountRate) ** 2
        V2 = 0
        V3 = 0
        V4 = 0
    else:
        V1 = (1 + Growth) / (1 + DiscountRate) ** 2
        V2 = 0
        V3 = 0
        V4 = 0

    V = V1 + V2 + V3 + V4                                 #合计增长率现值计算
    InterValue = EarningsPerShare * V * PriceEarningsRatio #内在价值计算
    return InterValue

if __name__=='__main__':
    Growth=float(input('请输入预测增长率：'))
    EarningsPerShare=float(input('请输入每股收益：'))
    DiscountRate=0.07
    PriceEarningsRatio=15
    print(InterValue(Growth, EarningsPerShare, DiscountRate, PriceEarningsRatio))
 
