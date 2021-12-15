#This script is adapted form the analysis scripts provided in psychophysics class

import pandas as pd
from scipy.stats import norm

from os import listdir



dataPath = "data_group/"
fileList = listdir(dataPath)

dataList = pd.DataFrame({"NoOfCircles":["Low","Low","High","High"],"Aligned":["Yes","No","Yes","No"],"hits":[0,0,0,0],"misses":[0,0,0,0],"FAs":[0,0,0,0],"CRs":[0,0,0,0]})

counter=0

for dataFile in fileList: #loop through the files
    counter+=1
    pNum="P-"+str(counter) #participant number
    
    rawData = pd.read_csv(dataPath + dataFile) #read the file
    expData = pd.DataFrame(rawData, columns = ["condition_size", "condition_lined","correct_answer", "key_resp.keys"]) #columns needed for analysis
    expData = expData.rename(columns = {"key_resp.keys" : "response"})
    
    expData = expData[expData.response.notnull()]#remove empty data (practice data)
    for index, row in expData.iterrows():
        if row["condition_size"] == "Low" and row["condition_lined"] == "Yes": #low number of aligned circles
            rowInd = 0 #first row
            if row["correct_answer"] == "Yes" and row["response"] == "z":#hit
                dataList.loc[rowInd,"hits"]+=1
            elif row["correct_answer"] == "Yes" and row["response"] == "m":#miss
                dataList.loc[rowInd,"misses"]+=1
            elif row["correct_answer"] == "No" and row["response"] == "z": #False alarm
                dataList.loc[rowInd,"FAs"]+=1
            elif row["correct_answer"]=="No" and row["response"] == "m": #correct rejection
                dataList.loc[rowInd,"CRs"]+=1
        elif row["condition_size"] == "Low" and row["condition_lined"] == "No": #low number of unaligned circles
            rowInd = 1 #second row
            if row["correct_answer"] == "Yes" and row["response"] == "z":#hit
                dataList.loc[rowInd,"hits"]+=1
            elif row["correct_answer"] == "Yes" and row["response"] == "m":#miss
                dataList.loc[rowInd,"misses"]+=1
            elif row["correct_answer"] == "No" and row["response"] == "z": #False alarm
                dataList.loc[rowInd,"FAs"]+=1
            elif row["correct_answer"]=="No" and row["response"] == "m": #correct rejection
                dataList.loc[rowInd,"CRs"]+=1
        elif row ["condition_size"] == "High" and row["condition_lined"] == "Yes": #high number of aligned circles
            rowInd = 2 #third row
            if row["correct_answer"] == "Yes" and row["response"] == "z":#hit
                dataList.loc[rowInd,"hits"]+=1
            elif row["correct_answer"] == "Yes" and row["response"] == "m":#miss
                dataList.loc[rowInd,"misses"]+=1
            elif row["correct_answer"] == "No" and row["response"] == "z": #False alarm
                dataList.loc[rowInd,"FAs"]+=1
            elif row["correct_answer"]=="No" and row["response"] == "m": #correct rejection
                dataList.loc[rowInd,"CRs"]+=1
        elif row ["condition_size"] == "High" and row["condition_lined"] == "No": #high number of unaligned cirlces
            rowInd = 3 #fourth row
            if row["correct_answer"] == "Yes" and row["response"] == "z":#hit
                dataList.loc[rowInd,"hits"]+=1
            elif row["correct_answer"] == "Yes" and row["response"] == "m":#miss
                dataList.loc[rowInd,"misses"]+=1
            elif row["correct_answer"] == "No" and row["response"] == "z": #False alarm
                dataList.loc[rowInd,"FAs"]+=1
            elif row["correct_answer"]=="No" and row["response"] == "m": #correct rejection
                dataList.loc[rowInd,"CRs"]+=1

def dPrime (hitRate,FArate): #calculating dprime
    stat = norm.ppf(hitRate)-norm.ppf(FArate)
    return stat

def criterion (hitRate, FArate): #calculating criterion
    stat=-.5*(norm.ppf(hitRate)+norm.ppf(FArate))
    return stat


#hit rates for each condition    
hitRateLowYes = dataList.loc[0,"hits"]/40 
hitRateLowNo = dataList.loc[1,"hits"]/40 
hitRateHighYes = dataList.loc[2,"hits"]/40 
hitRateHighNo = dataList.loc[3,"hits"]/40 

#False alarm rates for each condition
FArateLowYes = dataList.loc[0,"FAs"]/40 
FArateLowNo = dataList.loc[1,"FAs"]/40 
FArateHighYes = dataList.loc[2,"FAs"]/40 
FArateHighNo = dataList.loc[3,"FAs"]/40

print(dPrime(hitRateHighNo, FArateHighNo))  