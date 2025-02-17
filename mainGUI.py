import tkinter as tk
from tkinter import ttk
import functools
import csv
import serial
import numpy as np
import pandas as pd

def getData(ser,rows):
    result = []
    for i in range(rows):
        dataline = ser.readline()
        dataline = dataline.decode().strip()

        gas_data = dataline.split(sep= ",")

        for j in range(len(gas_data)):
            gas_data[j] = int(gas_data[j])

        result.append(gas_data)

        #wait 1s
    return pd.DataFrame(result, columns= ["NO2","C2H5OH","VOC","CO"])


def readData(filename):
    data = pd.read_csv(filename, skiprows= 3, header= None, nrows= 8)
    data.columns= ["NO2","C2H5OH","VOC","CO"]
    return data

def readTestData(filename,i):
    data = pd.read_csv(filename, skiprows= i, header= None, nrows= 1)
    data.columns= ["NO2","C2H5OH","VOC","CO"]
    return data

def acceptableRange(gasName, data):
    rangeData = pd.read_csv("range.csv", index_col= 0)
    # CHECK IF THE dispData IS IN ACCEPTABLE RANGE
    if rangeData.loc[gasName, "hazardous"] < data:
        return "#7E0023"
    elif rangeData.loc[gasName, "very unhealthy"] < data:
        return "#8F3F97"
    elif rangeData.loc[gasName, "unhealthy"] < data:
        return "#FF0000"
    elif rangeData.loc[gasName, "usg"] < data:
        return "#FF7E00"
    elif rangeData.loc[gasName, "moderate"] < data:
        return "#FFFF00"
    else:
        return "#00E400"

class precaution:
    def __init__(self,gasName,effects,precautions,sources):
        self.gasName = gasName
        self.effects = effects
        self.precautions = precautions
        self.sources = sources


def getPrec(gasName):
    file1 = open("precautions\\" + gasName + ".txt","r")
    file2 = open("sources\\" + gasName + ".txt","r")
    file3 = open("effects\\" + gasName + ".txt","r")

    result = precaution(gasName, file3.readlines(), file1.readlines(), file2.readlines())

    file1.close()
    file2.close()
    file3.close()

    return result

def dispPrec(gasname):
    gas = getPrec(gasName= gasname)

    top = tk.Toplevel()
    top.title("Gas- " + gasname)
    rowcount = 0

    main_frame = tk.Frame(top)
    main_frame.pack(fill= tk.BOTH, expand= 1)

    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side= tk.LEFT, fill= tk.BOTH, expand= 1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient= tk.VERTICAL, command= my_canvas.yview)
    my_scrollbar.pack(side= tk.RIGHT, fill= tk.Y)

    my_canvas.configure(yscrollcommand= my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))

    second_frame = tk.Frame(my_canvas)
    
    my_canvas.create_window((0,0), window= second_frame, anchor= "nw")

    label1 = tk.Label(second_frame, text= "Sources:", anchor= 'nw', font= ('Ariel', 18))
    label1.grid(row= rowcount, column= 0, sticky = tk.W)
    rowcount += 1

    for i in gas.sources:
        label2 = tk.Label(second_frame, anchor= 'nw', text= i)
        label2.grid(row= rowcount, column= 0, sticky = tk.W)
        rowcount += 1

    label1 = tk.Label(second_frame, text= "Effects:", anchor= 'nw', font= ('Ariel', 18))
    label1.grid(row= rowcount, column= 0, sticky = tk.W)
    rowcount += 1

    for i in gas.effects:
        label2 = tk.Label(second_frame, anchor= 'nw', text= i)
        label2.grid(row= rowcount, column= 0, sticky = tk.W)
        rowcount += 1
    
    label1 = tk.Label(second_frame, text= "Precautions:", anchor= 'nw', font= ('Ariel', 18))
    label1.grid(row= rowcount, column= 0, sticky = tk.W)
    rowcount += 1

    for i in gas.precautions:
        label2 = tk.Label(second_frame, anchor= 'nw', text= i)
        label2.grid(row= rowcount, column= 0, sticky = tk.W)
        rowcount += 1

def Quit():
    root.destroy()

root = tk.Tk()
root.geometry("400x300")
root.title("Air Monitoring system")
root.resizable(0,0)

def dispData():
    ser1 = serial.Serial("COM3", 9600)
    data = getData(ser1, 5)
    ser1.close()

    # data = readData("coca_cola_1.csv")

    meanData = data.mean(axis= 0)
    rowCount = 0

    for index, value in meanData.items():
        label = tk.Label(root, text = index +": ", font = ('Ariel', 18))
        label.grid(row= rowCount, column= 0, sticky = tk.W + tk.E)

        color = acceptableRange(index, value)
        label1 = tk.Label(root, text= str(value), font= ('Ariel', 18), background= color)
        label1.grid(row= rowCount, column= 1, sticky= tk.W + tk.E)
        if color != "#00E400":
            button = tk.Button(root, text= "?", font= ('Ariel', 12), command= lambda index=index: dispPrec(index))
            button.grid(row= rowCount, column= 2, sticky= tk.W + tk.E)
        rowCount += 1

    mybutton = tk.Button(root, text= "Refresh", command= dispData)
    mybutton.grid(row= rowCount, column= 1)

    mybutton = tk.Button(root, text= "Quit", command= Quit)
    mybutton.grid(row= rowCount, column= 2)
    rowCount += 1

def testDispData(i):
    data = readTestData("testcases.csv",i)

    meanData = data.mean(axis= 0)
    rowCount = 0

    for index, value in meanData.items():
        label = tk.Label(root, text = index +": ", font = ('Ariel', 18))
        label.grid(row= rowCount, column= 0, sticky = tk.W + tk.E)

        color = acceptableRange(index, value)
        label1 = tk.Label(root, text= str(value), font= ('Ariel', 18), background= color)
        label1.grid(row= rowCount, column= 1, sticky= tk.W + tk.E)
        if color != "#00E400":
            button = tk.Button(root, text= "?", font= ('Ariel', 12), command= lambda index= index: dispPrec(index))
            button.grid(row= rowCount, column= 2, sticky= tk.W + tk.E)
        rowCount += 1

    mybutton = tk.Button(root, text= "Quit", command= Quit)
    mybutton.grid(row= rowCount, column= 2)
    rowCount += 1

# dispData()
testDispData(4)
root.mainloop()  



    

    
        

