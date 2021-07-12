import tkinter as tk
import os
import re
import urllib.parse
import requests
import geopy.distance
import math

bgColor, fColor, entryBg, entryFg = '#333333', '#73d0b3', '#595959', '#83dec2'

# Initialize and assign dictionaries
addy_file, name_file, offense_file, indv_file, off_code_file = open('data\Address.txt'), open(
    'data\\NAME.txt'), open('data\\Offense.txt'), open('data\\INDV.txt'), open('data\\OFF_CODE_SOR.txt')
addy_dict, name_dict, offense_dict, indv_dict, off_code_dict = {}, {}, {}, {}, {}

for x in addy_file:
    temp = x.split('\t')
    id = temp[1]
    addy = ' '.join(temp[2:9])
    zipcode = temp[8]
    lat = temp[10]
    lon = re.sub(r'\n', '', temp[11])
    coord = (lat, lon)
    addy_dict[id] = [addy, coord, zipcode]

for x in name_file:
    temp = x.split('\t')
    id = temp[1]
    first_name = re.sub(r'\n', '', temp[5])
    last_name = temp[4]
    name_dict[id] = [first_name, last_name]

for x in offense_file:
    temp = x.split('\t')
    id = temp[0]
    offense_code = temp[5]
    victim_age = temp[12]
    victim_sex = temp[13]
    offense_dict[id] = [offense_code, victim_age, victim_sex]

for x in indv_file:
    temp = x.split('\t')
    sid = re.sub(r'\n', '', temp[1])
    indv_dict[sid] = temp[0]

for x in off_code_file:
    temp = x.split('\t')
    try:
        key = temp[3]
        offense = temp[5]
        off_code_dict[key] = offense
    except:
        pass


def narrow(user_coords, zipcode):
    close_dict = {}
    for x in addy_dict:
        if addy_dict[x][2] == '':
            continue
        else:
            temp_zip = int(addy_dict[x][2])
            checker = math.floor(int(zipcode)/1000)
            # Creating dictionary of all offenders with same first two digits
            if math.floor(temp_zip/1000) == checker:
                distance = geopy.distance.distance(
                    addy_dict[x][1], user_coords).miles
                # If place is within 2 miles of user location
                if distance <= 2:
                    close_dict[x] = addy_dict[x]
    return close_dict


def analyze(address, zipcode, sex, age):
    new = tk.Toplevel()
    new.geometry('400x400')
    new.resizable(False, False)
    new.configure(background=bgColor)

    try:
        url = 'https://nominatim.openstreetmap.org/search/' + \
            urllib.parse.quote(address+" " + zipcode) + '?format=json'
        print(url)
        response = requests.get(url).json()
        lat = response[0]['lat']
        lon = response[0]['lon']
        user_coords = (lat, lon)

        close_offenders = narrow(user_coords, zipcode)
    except Exception as e:
        print("Invalid Address")
        print(e)
        new.destroy()
