# testing testing

#https://www.youtube.com/watch?v=H71ts4XxWYU

import tkinter as tk
#import pandas as pd
from tkinter import *
from tkinter import filedialog

#file_path = ""

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.csv; *.json; *.json-stat")])

#fileOpen()
#button = Button(text="Select a .csv, .json or .json-text file.", width = 50, command= fileOpen).pack()
#a.mainloop()

csv=".csv"
json = ".json"
json_stat = ".json-stat"

input('Press any key to exit')

if file_path!="": 
    if file_path.find(csv)!=-1:
        df= df = file_path # pd.read_csv(file_path)

print(df)
