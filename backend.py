import tkinter as tk
import os
import re
import urllib.parse
import requests
import geopy.distance
import math

# Initialize and assign dictionaries
addy_file = open('data\Address.txt')
addy_dict = {}
for x in addy_file:
    temp = x.split('\t')
    id = temp[1]
    addy = ' '.join(temp[2:9])
    zipcode = temp[8]
    lat = temp[10]
    lon = re.sub(r'\n', '', temp[11])
    coord = (lat, lon)
    addy_dict[id] = [addy, coord, zipcode]

name_dict = {}
name_file = open('data\\NAME.txt')
for x in name_file:
    temp = x.split('\t')
    id = temp[1]
    first_name = re.sub(r'\n', '', temp[5])
    last_name = temp[4]
    name_dict[id] = [first_name, last_name]

offense_dict = {}
offense_file = open('data\\Offense.txt')
for x in offense_file:
    temp = x.split('\t')
    id = temp[0]
    offense_code = temp[5]
    victim_age = temp[12]
    victim_sex = temp[13]
    offense_dict[id] = [offense_code, victim_age, victim_sex]

indv_dict = {}
indv_file = open('data\\INDV.txt')
for x in indv_file:
    temp = x.split('\t')
    sid = re.sub(r'\n', '', temp[1])
    indv_dict[sid] = temp[0]

off_code_dict = {}
off_code_file = open('data\\OFF_CODE_SOR.txt')
for x in off_code_file:
    temp = x.split('\t')
    try:
        key = temp[3]
        offense = temp[5]
        off_code_dict[key] = offense
    except:
        pass

# print('Address: ' + addy_dict['13347593'][0] +
#       '\nOffense: ' + offense_dict['13347593'][1] + " " + offense_dict['13347593'][2] + '\nMore Offense: ' + off_code_dict[offense_dict['13347593'][0]])


def analyze(address, zipcode, sex, age):
    new = tk.Toplevel()
    new.geometry('400x400')

    try:
        url = 'https://nominatim.openstreetmap.org/search/' + \
            urllib.parse.quote(address+" " + zipcode) + '?format=json'
        print(url)
        response = requests.get(url).json()
        lat = response[0]['lat']
        lon = response[0]['lon']
        user_coords = (lat, lon)

        print(user_coords)
        print(addy_dict['13347593'][1])
        distance = geopy.distance.distance(
            addy_dict['13347593'][1], user_coords).miles
        print(distance)

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
        print(close_dict)
    except Exception as e:
        print("Invalid Address")
        print(e)
        new.destroy()
