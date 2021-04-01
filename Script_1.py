#https://www.youtube.com/watch?v=H71ts4XxWYU

import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter import *

global file_path
file_path = -1 

app = tk.Tk() # the application itself
app.title("Test") # title of window

def selectFile():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.csv; *.json; *.json-stat")])
    if file_path != "":
        return file_path
    elif file_path == "":
        file_path=-1
        return file_path

label = Label(app, text="Testing testing one, two, three") # creates label
label.pack() # adds the label to the window
button = tk.Button(app, text="Select a .csv, .json or .json-text file.", width = 50, command = lambda: file_path == selectFile())
button.pack()
if file_path != -1:
    print(file_path)
    #file_pathlabel = Label(app, text=file_path) # creates label
    #file_pathlabel.pack() # adds the label to the window

app.mainloop() # this must go at the end of your window code

print(file_path)
csv=".csv"
json = ".json"
json_stat = ".json-stat"



#if file_path!="": 
 #   if file_path.find(csv)!=-1:
  #      df= df = pd.read_csv(file_path)

#print(df)