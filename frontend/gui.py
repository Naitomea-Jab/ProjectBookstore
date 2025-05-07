# gui.py
from tkinter import *  # standard Python interface to the Tcl/Tk GUI toolkit
import requests  # package allows you to send HTTP requests
from PIL import Image, ImageTk

import bookstore.customer_Manager
from bookstore import customer_Manager


def start_gui():
    window = Tk()
    window.title("GUI")
    window.geometry("1280x720")

    Label(window, text="Logo").grid(row=1, column=1)

    text_result = Label(window, text="Wynik: 0")
    text_result.grid(row=2, column=0, columnspan=4)

    def get_customers():
        result = customer_Manager.get_customers(None)
        text_result.config(text=result)

    Button(window, text="Enter", command=get_customers, fg="red").grid(row=4, column=1)

    window.mainloop()


    print("hello Cirno")