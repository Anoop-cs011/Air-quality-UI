import tkinter as tk
from tkinter import ttk
import csv
import serial
import pandas as pd
import functools

def getData(ser, rows):
    result = []
    for _ in range(rows):
        dataline = ser.readline().decode().strip()
        gas_data = list(map(int, dataline.split(',')))
        result.append(gas_data)
    return pd.DataFrame(result, columns=["NO2", "C2H5OH", "VOC", "CO"])

def readData(filename):
    data = pd.read_csv(filename, skiprows= 3, header= None, nrows= 8)
    data.columns= ["NO2","C2H5OH","VOC","CO"]
    return data

def readTestData(filename, i):
    data = pd.read_csv(filename, skiprows=i, header=None, nrows=1)
    data.columns = ["NO2", "C2H5OH", "VOC", "CO"]
    return data

def acceptableRange(gasName, data):
    rangeData = pd.read_csv("range.csv", index_col=0)
    thresholds = ["hazardous", "very unhealthy", "unhealthy", "usg", "moderate"]
    colors = ["#7E0023", "#8F3F97", "#FF0000", "#FF7E00", "#FFFF00", "#00E400"]
    for i, level in enumerate(thresholds):
        if rangeData.loc[gasName, level] < data:
            return colors[i]
    return colors[-1]

def getPrec(gasName):
    with open(f"precautions/{gasName}.txt", "r") as f1, open(f"sources/{gasName}.txt", "r") as f2, open(f"effects/{gasName}.txt", "r") as f3:
        return {
            "effects": f3.readlines(),
            "precautions": f1.readlines(),
            "sources": f2.readlines()
        }

def dispPrec(gasname):
    gas = getPrec(gasname)
    top = tk.Toplevel()
    top.title(f"Precautions for {gasname}")
    top.geometry("400x300")
    
    frame = ttk.Frame(top, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient= tk.VERTICAL, command= canvas.yview)
    scrollbar.pack(side= tk.RIGHT, fill= tk.Y)

    canvas.configure(yscrollcommand= scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))
    scroll_frame = ttk.Frame(canvas)
    
    ttk.Label(scroll_frame, text="Sources:", font=("Arial", 14, "bold")).pack(anchor='w')
    for line in gas["sources"]:
        ttk.Label(scroll_frame, text=line.strip(), wraplength=380).pack(anchor='w')
    
    ttk.Label(scroll_frame, text="Effects:", font=("Arial", 14, "bold")).pack(anchor='w')
    for line in gas["effects"]:
        ttk.Label(scroll_frame, text=line.strip(), wraplength=380).pack(anchor='w')
    
    ttk.Label(scroll_frame, text="Precautions:", font=("Arial", 14, "bold")).pack(anchor='w')
    for line in gas["precautions"]:
        ttk.Label(scroll_frame, text=line.strip(), wraplength=380).pack(anchor='w')
    
    frame.grid_columnconfigure(0, weight=1)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

def Quit():
    root.destroy()

def dispData():
    ser1 = serial.Serial("COM3", 9600)
    data = getData(ser1, 5)
    ser1.close()
    
    data = data.mean(axis= 0)
    for widget in frame.winfo_children():
        widget.destroy()

    for i, (index, value) in enumerate(data.items()):
        color = acceptableRange(index, value)
        ttk.Label(frame, text=f"{index}:", font=("Arial", 14)).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(frame, text=f"{value:.2f}", font=("Arial", 14), background=color, padding=5).grid(row=i, column=1, padx=10, pady=5, sticky='w')
        if color != "#00E400":
            ttk.Button(frame, text="?", command=lambda gas=index: dispPrec(gas)).grid(row=i, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Refresh", command=dispData).grid(row=len(data), column=0, pady=10)
    ttk.Button(frame, text="Quit", command=Quit).grid(row=len(data), column=1, pady=10)

def dispTestData(testCase):
    data = readTestData("testcases.csv", testCase).mean(axis=0)
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    for i, (index, value) in enumerate(data.items()):
        color = acceptableRange(index, value)
        ttk.Label(frame, text=f"{index}:", font=("Arial", 14)).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(frame, text=f"{value:.2f}", font=("Arial", 14), background=color, padding=5).grid(row=i, column=1, padx=10, pady=5, sticky='w')
        if color != "#00E400":
            ttk.Button(frame, text="?", command=lambda gas=index: dispPrec(gas)).grid(row=i, column=2, padx=10, pady=5)
    partialFunc = functools.partial(dispTestData, (testCase+1)%12)
    ttk.Button(frame, text="Refresh", command=partialFunc).grid(row=len(data), column=0, pady=10)
    ttk.Button(frame, text="Quit", command=Quit).grid(row=len(data), column=1, pady=10)

root = tk.Tk()
root.geometry("500x400")
root.title("Air Monitoring System")
root.resizable(False, False)
frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)
# dispData()
dispTestData(0)
root.mainloop()
