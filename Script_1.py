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
    X = filedialog.askopenfilename(filetypes=[("Image files", "*.csv; *.json; *.json-stat")])
    print(X)
    file_path = X
    file_pathlabel = Label(app, text=file_path) # creates label
    file_pathlabel.pack() # adds the label to the window
    return file_path

label = Label(app, text="Testing testing one, two, three") # creates label
label.pack() # adds the label to the window
button = tk.Button(app, text="Select a .csv, .json or .json-text file.", width = 50, command = lambda: file_path == selectFile())
button.pack()


app.mainloop() # this must go at the end of your window code

print(file_path)
csv=".csv"
json = ".json"
json_stat = ".json-stat"



#if file_path!="": 
 #   if file_path.find(csv)!=-1:
  #      df= df = pd.read_csv(file_path)

#print(df)