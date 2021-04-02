#https://www.youtube.com/watch?v=H71ts4XxWYU


import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter import *
import pandas as pd



app = tk.Tk() # the application itself
app.title("Test") # title of window



def selectFile():
    
    X = filedialog.askopenfilename(filetypes=[("Image files", "*.csv; *.json; *.json-stat")])
    #print(X)
    file_path = X
    file_pathlabel = Label(app, text=file_path) # creates label
    file_pathlabel.pack() # adds the label to the window
    #print(file_path)
    return file_path

def data_finder(fp):
    data=-1
    if fp.lower().endswith(".json"):
        x = pd.read_json(fp)
        data = pd.DataFrame(data=x)
    elif fp.lower().endswith(".csv"):
        y = pd.read_csv(fp)
        data = pd.DataFrame(data=y)
    elif fp.lower().endswith(".json-stat"):
        x=-1
        data=x
    return data

file_path = StringVar()
label = Label(app, text="Testing testing one, two, three") # creates label
label.pack() # adds the label to the window
button = tk.Button(app, text="Select a .csv, .json or .json-text file.", width = 50, command = lambda: file_path == selectFile())
button.pack()
#data_path=file_path
print(file_path)
#data = data_finder(file_path)
#print(data)

app.mainloop() # this must go at the end of your window code




#if file_path!="": 
 #   if file_path.find(csv)!=-1:
  #      df= df = pd.read_csv(file_path)

#print(df)