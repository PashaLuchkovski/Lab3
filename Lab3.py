import urllib2
import os
import pandas as pd
import re
import random

path = "/Users/pashaluchkovski/Documents/Study/Coding/Python/Lab3/"

def readDataToFrame(path):
    os.chdir(path)
    df = pd.read_csv('data.txt', header = 0, sep = ";", low_memory=False)
    return df

def cleanData(frame):
    frame = frame.loc[(frame['Voltage'] != "?")]
    return frame

def moreThan5kWt(frame):
    frame = frame.loc[(frame['Global_active_power'] >= "5")]
    return frame

def moreThan235Voltage(frame):
    frame = frame.loc[(frame['Voltage'] >= "235")]
    return frame

def intensityBetween19_20andSub2moreThanSub3(frame):
    frame = frame.loc[ (frame['Global_intensity'].astype(float) > 19) ]
    frame = frame.loc[ (frame['Global_intensity'].astype(float) < 20) ]
    frame = frame.loc[ frame['Sub_metering_2'].astype(float) > frame['Sub_metering_3'] ]
    return frame

def chooseHouses(frame, amount):
    if amount < frame.size/9:
        randVar = []
        for i in range(amount):
            randVar.append(random.choice(frame.index.values))
        frame = frame.ix[randVar]
        return frame
    else:
        return 0

def appendWithAverage(frame):
    averageMass = []
    for i in range(len(frame.index.values)):
        averageVal = float(frame['Sub_metering_1'].values[i]) + float(frame['Sub_metering_2'].values[i]) + float(frame['Sub_metering_3'].values[i])
        averageMass.append(averageVal)
    toAppend = pd.Series(averageMass, index=frame.index.values, name = 'Average')
    appended = pd.concat([frame, toAppend], axis=1, join_axes=[frame.index])
    appended = appended.sort_index()
    return appended

def eveningFrameF(frame):
    eveningIndexes = []
    eveningHours = ['18','19','20','21','22','23']
    for i in range(len(frame.index.values)):
        test = frame['Time'].values[i]
        test = test[0:2] #Choose 2 first symbols, it`s Hour
        if test in eveningHours:
            eveningIndexes.append(i)
    frame = frame.ix[eveningIndexes] # fault in pandas ix[] 
    frame = frame.loc[frame['Global_active_power'].astype(float) > 6] # choose more than 6 kWt
    frame = frame.loc[ frame['Sub_metering_2'].astype(float) > frame['Sub_metering_1'].astype(float) ]
    frame = frame.loc[ frame['Sub_metering_2'].astype(float) > frame['Sub_metering_3'].astype(float) ]
    return frame

def sliceFrame(frame):
    half = frame.size/(9*2)
    print frame.shape
    print half
    frame1 = frame[0:(frame.size/(9*2))]
    frame2 = frame[half:(frame.size/9)]
    frame1 = frame1[0:(frame1.size/9):3]
    frame2 = frame2[0:(frame2.size/9):4]

def main_f():    
    df = readDataToFrame(path) #Read to frame
    df = cleanData(df) # Clean data (delete rows with "?")
    more5kWt = moreThan5kWt(df) # 1 task
    more235V = moreThan235Voltage(df) # 2 task
    intensity19and20 = intensityBetween19_20andSub2moreThanSub3(df) # 3 task
    appended = appendWithAverage(chooseHouses(df, 50000)) # 4 task
    eveningFrame = eveningFrameF(df) # 5 task 
    sliceFrame(eveningFrame) # 5 task continue

main_f()
# ________TEST__________ #
#intensity19and20.to_csv("/Users/pashaluchkovski/Downloads/3task.csv") #WRITE TO CSV
#print list(df.columns.values) # columns names
#print float(frame['Sub_metering_2'].values[3]) #choose 3 value
#frame_columns[i] = re.sub('[^A-Za-z0-9]+', '', frame_columns[i]) #regular expression
#print frame.shape # size of frame
