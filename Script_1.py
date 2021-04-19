#https://www.youtube.com/watch?v=H71ts4XxWYU


import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter import *
import pandas as pd
import os



app = tk.Tk() # the application itself
app.title("Test") # title of window



def selectFile():
    
    X = filedialog.askopenfilename(filetypes=[("Image files", "*.csv; *.json; *.json-stat")])
    #print(X)
    file_path = X
    label_1 = Label(app, text="The file's location that you have selected is as follows:") # other option
    label_1.pack()
    file_pathlabel = Label(app, text=file_path) # creates label
    file_pathlabel.pack() # adds the label to the window
    label_s = Label(app, text="") # other option
    label_s.pack()
    #print(file_path)
    data = data_finder(file_path)

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
        z = pd.read_json(fp)
        data=z
    #data.head()
    #print(list(data.columns.values.tolist()))
    #label_3 = Label(app, text=str(data.head())) # other option
    #label_3.pack()
    label_2 = Label(app, text="The first 5 rows of the dataset are as follows:") # other option
    label_2.pack() 
    label_3 = Label(app, text=str(data.iloc[:6,:data.shape[1]])) # other option
    label_3.pack()
    dataSetInfo(data)
    return data

def dataSetInfo(data):
    label_s = Label(app, text="") # other option
    label_s.pack()
    label_t = Label(app, text="The number of rows in the dataset is:") # other option
    label_t.pack()
    label_1 = Label(app, text=str(data.shape[0])) # other option
    label_1.pack()

    label_s2 = Label(app, text="") # other option
    label_s2.pack()
    label_t2 = Label(app, text="The number of columns in the dataset is:") # other option
    label_t2.pack()
    label_2 = Label(app, text=str(data.shape[1])) # other option
    label_2.pack()

    x = list(data.columns.values.tolist())
    string_1 = ""
    for i in x:
        string_1= string_1 + "\n" + i

    label_s3 = Label(app, text="") # other option
    label_s3.pack()
    label_t3 = Label(app, text="The columns of the dataset are:") # other option
    label_t3.pack()
    label_3 = Label(app, text=string_1) # other option
    label_3.pack()

    label_s4 = Label(app, text="") # other option
    label_s4.pack()
    label_t4 = Label(app, text="Please click the button below to export to an excel file:") # other option
    label_t4.pack()
    button_2 = tk.Button(app, text="Export Data",  command = lambda: convertToExcel(data))
    button_2.pack()


def convertToExcel(data):
    wd = os.getcwd()
    print(wd)
    with pd.ExcelWriter('output.xlsx') as writer:  
        data.to_excel(writer, sheet_name='Sheet_name_1')
    #data.to_excel(wd)


file_path = StringVar()
label = Label(app, text="Please click the button below to select a data file:") # creates label
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