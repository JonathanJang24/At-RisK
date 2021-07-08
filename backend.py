import tkinter as tk
import os
from xml.etree import ElementTree

file_name = open('data\Address.txt')
for r in file_name:
    print(r)


def analyze(address, zipcode, sex, age):
    new = tk.Toplevel()
    new.geometry('400x400')

    print("called")
    print(address)
    print(zipcode)
    print(sex)
    print(age)
