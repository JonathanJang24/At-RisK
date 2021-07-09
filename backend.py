import tkinter as tk
import os
from xml.etree import ElementTree

# Testing split and scraping data from text files
file_name = open('data\Address.txt')
for r in file_name:
    r = r.split('\t')
    id = r[1]
    address = ' '.join(r[2:9])
    coords = ' '.join(r[10:12])
    print('id: ' + id)
    print('address: ' + address)
    print('coordinates: ' + coords)
    break


def analyze(address, zipcode, sex, age):
    new = tk.Toplevel()
    new.geometry('400x400')

    print("called")
    print(address)
    print(zipcode)
    print(sex)
    print(age)
