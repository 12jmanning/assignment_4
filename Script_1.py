# testing testing

#https://www.youtube.com/watch?v=H71ts4XxWYU

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.csv; *.json; *.json-stat")])

print(file_path)

input('Press any key to exit')

