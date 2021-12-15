import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from os import listdir
from statistics import mean
from statsmodels.stats.anova import AnovaRM

dataPath = "data_group/"
fileList = listdir(dataPath)

meanRTs = pd.DataFrame({"participant" : [], "NoOfCircles"
: [], "Aligned" : [], "mean RT" : []}) #table for mean reaction times

counter = 0 

for dataFile in fileList: #loop through each file
    counter+=1 #participant number
    pNum="P-"+str(counter)
    
    rawData=pd.read_csv(dataPath+dataFile) #read the whole file
    #data needed for analysis:
    expData=pd.DataFrame(rawData, columns = ["condition_size", "condition_lined","correct_answer", "key_resp.keys", "key_resp.rt"])
    expData=expData.rename(columns = {"key_resp.rt" : "RT", "key_resp.keys" : "response"})

    expData = expData[expData.RT.notnull()] #remove data without response
    expData = expData[(expData.RT < 3)] #threshold to 3 seconds (remove outliers)
    rtData = expData[(expData.correct_answer == "Yes") & (expData.response == "z")] #filter correct answers
    lowAlignRTs = rtData[(rtData.condition_size == "Low") & (rtData.condition_lined == "Yes")].RT #RTs for trials with low number of aligned circles
    lowUnalignRTs = rtData[(rtData.condition_size == "Low") & (rtData.condition_lined == "No")].RT #trials with low number of unaligned circles
    highAlignRTs = rtData[(rtData.condition_size == "High") & (rtData.condition_lined == "Yes")].RT #trials with high number of aligned circles
    highUnalignRTs = rtData[(rtData.condition_size == "High") & (rtData.condition_lined == "No")].RT #trials with high number of unaligned circles
    
    pNumList = [pNum, pNum, pNum, pNum]
    circleNumList = ["Low", "Low", "High", "High"]
    alignmentList = ["Yes", "No", "Yes", "No"]
    meanRTsList = [mean(lowAlignRTs),mean(lowUnalignRTs),mean(highAlignRTs),mean(highUnalignRTs)]
    newLines = pd.DataFrame({"participant" : pNumList, "NoOfCircles" : circleNumList, "Aligned" : alignmentList, "mean RT" : meanRTsList})
    meanRTs = meanRTs.append(newLines, ignore_index=True)
    

lowAlignMeans=meanRTs[(meanRTs.NoOfCircles == "Low") & (meanRTs.Aligned == "Yes")]["mean RT"]
lowUnalignMeans=meanRTs[(meanRTs.NoOfCircles == "Low") & (meanRTs.Aligned == "No")]["mean RT"]
highAlignMeans=meanRTs[(meanRTs.NoOfCircles == "High") & (meanRTs.Aligned == "Yes")]["mean RT"]
highUnalignMeans=meanRTs[(meanRTs.NoOfCircles == "High") & (meanRTs.Aligned == "No")]["mean RT"]

#scatter plot
def scatter_plt(listofRTs1, listofRTs2, listofRTs3, listofRTs4):

    lowyes= plt.scatter(range(1,len(listofRTs1) + 1), listofRTs1, color = 'pink') #low number of aligned circles
    
    lowno = plt.scatter(range(1,len(listofRTs2) + 1), listofRTs2,  color = 'deeppink') #low number of unaligned circles
    
    highyes = plt.scatter(range(1,len(listofRTs3) + 1), listofRTs3, color = 'blue') #high number of aligned circles
    
    highno = plt.scatter(range(1,len(listofRTs4) + 1), listofRTs4, color = 'deepskyblue') #high number of unaligned circles
    
    plt.ylabel("RT (s)") #y-axis
    plt.xlabel("Trial Number") #x-axis
    plt.title("Reaction Time Sequence") #title
    plt.legend((lowyes,lowno,highyes,highno),("Low:Yes","Low:No","High:Yes","High:No"), scatterpoints=1, loc="upper right",ncol=1,fontsize=10) #legend   
    plt.show()

scatter_plt(lowAlignRTs, lowUnalignRTs, highAlignRTs, highUnalignRTs)

#boxplot
fig, ax = plt.subplots()
box = ax.boxplot([lowAlignMeans, lowUnalignMeans, highAlignMeans, highUnalignMeans])
ax.set_ylabel("RT (s)")
ax.set_xticklabels(["Low:Yes", "Low:No", "High:Yes", "High:No"])

#anova
model = AnovaRM(data = meanRTs, depvar = "mean RT", subject = "participant", within = ["NoOfCircles","Aligned"]).fit()
print(model)