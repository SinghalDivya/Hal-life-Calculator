
# coding: utf-8


import csv
import numpy as np
import pandas as pan
from scipy import stats
from operator import itemgetter

def ParseTextIntoTables(table,x,y):
    values = list()
    rows = len(table)
    for index in range(1,rows):
        numList = [float(i) for i in table.loc[index,x:y]]
        updatedVal = HandleNaN(numList)
        values.append(updatedVal)
    return values

def HalfLifeCalculator(values):
    HalfLife = list()
    rows = len(values)
    for index in range(1,rows):
        slope, intercept, r_value, p_value, std_err = stats.linregress(values[0],values[index])
        tempHL = 0.693/slope
        HalfLife.append(tempHL)
    return HalfLife

def HandleNaN(listValues):
    df = pan.DataFrame({
    'Cordinates': pan.Series(
                [listValues[0],
                 listValues[1],
                 listValues[2],
                 listValues[3],
                 listValues[4],
                 listValues[5],
                 listValues[6],
                 listValues[7],
                 listValues[8]])})
    meanList = df.fillna(df.mean(),axis=0)
    return meanList['Cordinates'].values.tolist()

def listToPandaDataFrame(List1):
    pandaDataFrame = pan.DataFrame(List1,columns=['col1','col2'])
    return pandaDataFrame
    

tableValues = pan.read_table('DecayTimecourse.txt',header=None)
table_1 = ParseTextIntoTables(tableValues, 1, 9)
table_2 = ParseTextIntoTables(tableValues, 10, 18)
table_3 = ParseTextIntoTables(tableValues, 19, 27)

HalfLife_1 = HalfLifeCalculator(table_1)
HalfLife_2 = HalfLifeCalculator(table_2)
HalfLife_3 = HalfLifeCalculator(table_3)

HalfLife = list()
GenesList = list()
startIndex = 2
for i in range(0,len(HalfLife_1)):
    sum = HalfLife_1[i] + HalfLife_2[i] + HalfLife_3[i]
    avg = sum/3
    tempHL = [tableValues.loc[startIndex+i,0],avg]
    HalfLife.append(tempHL)

HalfLife_PandaDF = listToPandaDataFrame(HalfLife)
HalfLife_PandaDF = HalfLife_PandaDF.replace([np.inf, -np.inf], np.nan)
HalfLife_PandaDF = HalfLife_PandaDF.dropna(how="any")
SortedHalfLife_PandaDF = HalfLife_PandaDF.sort_values("col2")

numberRows = len(SortedHalfLife_PandaDF)
tenPerNum = int(numberRows*0.10)

topTenValues = SortedHalfLife_PandaDF.tail(tenPerNum)
BottomTenValues = SortedHalfLife_PandaDF.head(tenPerNum)

topTenValues.to_csv("topTenValues.txt",sep='\t',encoding='utf-8')
BottomTenValues.to_csv("bottonTenValues.txt",sep='\t', encoding='utf-8')





