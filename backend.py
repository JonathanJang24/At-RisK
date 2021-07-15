import tkinter as tk
import re
from tkinter.constants import CENTER, LEFT, UNDERLINE
from tkinter.font import BOLD
import urllib.parse
import requests
import geopy.distance
import math
from custom_errors import InvalidSexError, ImpossibleAgeError
from openData import addy_dict, name_dict, offense_dict, indv_dict, off_code_dict
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import io

bgColor, fColor, entryBg, entryFg = '#333333', '#73d0b3', '#595959', '#83dec2'
risk0_color, risk1_color, risk2_color, risk3_color = '#97e8c1', '#f7ff66', '#ffba66', '#f55d5d'
myFont = 'PierSans-Light'


def destroy():
    new_window.destroy()


def narrow(user_coords, zipcode):
    close_dict = {}
    closest_distance = 1000
    closest_offender = ''
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
                if(distance < closest_distance):
                    closest_distance = distance
                    closest_offender = x

    offender_label.config(text="The closest offender is %.3f miles away. He/She lives at %s" % (
        round(closest_distance, 3), re.sub(r' ', ' ', addy_dict[closest_offender][0])))
    return close_dict, closest_distance, closest_offender


def analyze(address, zipcode, sex, age):
    global new_window, risk_label, sex_label, age_label, quantity_label, offender_label, error_msg, nearby_label
    new_window = tk.Toplevel()
    new_window.geometry('400x400')
    new_window.resizable(False, False)
    new_window.configure(background=bgColor)

    # Initalizing most of the labels
    risk_label = tk.Label(new_window,
                          text="", font=(myFont, 20, BOLD, UNDERLINE), bg=bgColor)
    quantity_label = tk.Label(new_window, text="", font=(
        myFont, 12), bg=bgColor, fg=fColor, wraplength=380, justify=LEFT)
    age_label = tk.Label(new_window, text="", font=(
        myFont, 12), bg=bgColor, wraplength=380, justify=LEFT)
    sex_label = tk.Label(new_window, text="", font=(
        myFont, 12), bg=bgColor, wraplength=380, justify=LEFT)
    offender_label = tk.Label(new_window, text="", fg=fColor, bg=bgColor, font=(
        myFont, 12, UNDERLINE), justify=LEFT, wraplength=225)
    nearby_label = tk.Label(new_window, text="", bg=bgColor, fg=fColor, font=(
        myFont, 12, UNDERLINE), wraplength=380)

    # Placing all labels
    risk_label.place(x=200, y=20, anchor="center")
    quantity_label.place(x=10, y=70, anchor='w')
    sex_label.place(x=10, y=120, anchor='w')
    age_label.place(x=10, y=170, anchor='w')
    offender_label.place(x=10, y=280, anchor='w')

    if(sex.upper() != 'M' and sex.upper() != 'F'):
        raise InvalidSexError

    if(int(age) < 0 or int(age) > 122):
        raise ImpossibleAgeError

    # Getting user coordinates
    url = 'https://nominatim.openstreetmap.org/search/' + \
        urllib.parse.quote(address+" " + zipcode) + '?format=json'
    response = requests.get(url).json()
    lat = response[0]['lat']
    lon = response[0]['lon']
    user_coords = (lat, lon)

    # Calling of all functions
    close_offenders, closest_distance, closest_offender = narrow(
        user_coords, zipcode)
    risk_1 = quantity_risk(close_offenders)
    sex_risk, age_risk = specific_level(close_offenders, sex, age)
    total = risk_1 + sex_risk + age_risk
    general_risk(risk_1, sex_risk, age_risk)

    # How many are nearby
    nearby_label.config(
        text="There are %d offenders in a 2 mile radius." % len(close_offenders))
    nearby_label.place(x=10, y=215, anchor='w')

    # Code for picture of closest offender
    source = requests.get(
        'https://publicsite.dps.texas.gov/SexOffenderRegistry/Search/Rapsheet/CurrentPhoto?Sid='+indv_dict[closest_offender]).content

    img = ImageTk.PhotoImage(Image.open(io.BytesIO(source)))
    img_label = tk.Label(new_window, image=img,
                         bg=bgColor, height=120, width=120)
    img_label.place(x=240, y=245, anchor='nw')

    new_window.mainloop()


def quantity_risk(dict):
    if(len(dict) == 0):
        quantity_label.config(
            text='There are no convicted offenders in a 2 mile radius', fg=risk0_color)
        nearby_label.config(fg=risk0_color)
        return 0
    elif(len(dict) > 0 and len(dict) < 6):
        quantity_label.config(
            text='There is a small quantity of convicted offenders in a 2 mile radius', fg=risk1_color)
        nearby_label.config(fg=risk1_color)
        return 1
    elif(len(dict) > 5 and len(dict) < 11):
        quantity_label.config(
            text='There is a moderate presence of convicted offenders in a 2 mile radius', fg=risk2_color)
        nearby_label.config(fg=risk2_color)
        return 2
    elif(len(dict) > 10):
        quantity_label.config(
            text='There is a relatively large amount of convicted offenders in a 2 mile radius', fg=risk3_color)
        nearby_label.config(fg=risk3_color)
        return 3


def specific_level(dict, user_sex, user_age):
    global sex_label, age_label

    sex_match = 0
    age_match = 0
    sex_risk = 0
    age_risk = 0

    for x in dict:
        if offense_dict[x][2] == user_sex.upper():
            sex_match += 1
        # If offender's previous victim's age is +- 3 of individual's age
        if(int(offense_dict[x][1]) >= 60 and int(user_age) >= 60):
            age_match += 1
        elif(int(user_age) > 21 and user_age < 60 and int(offense_dict[x][1]) > 21 and int(offense_dict[x][1]) < 60):
            age_match += 1
        else:
            if(int(offense_dict[x][1])-3 <= int(user_age) and int(offense_dict[x][1])+3 >= int(user_age)):
                age_match += 1

    if(sex_match == 0):
        sex_label.config(
            text="Within the area, this sex has not previously been targeted.", fg=risk0_color)
    elif(sex_match > 0 and sex_match < 4):
        sex_label.config(
            text="Within the area, this sex is at slight risk based on previous records.", fg=risk1_color)
        sex_risk = 1
    elif(sex_match > 3 and sex_match < 8):
        sex_label.config(
            text="Within the area, this sex is at risk based on previous records.", fg=risk2_color)
        sex_risk = 2
    elif(sex_match > 7):
        sex_label.config(
            text="Within the area, this sex is at high risk based on previous records.", fg=risk3_color)
        sex_risk = 3

    if(age_match == 0):
        age_label.config(
            text="Within the area, similar ages have not previously been targeted.", fg=risk0_color)
    elif(age_match > 0 and age_match < 4):
        age_label.config(
            text='Within the area, similar ages are at slight risk based on previous records.', fg=risk1_color)
        age_risk = 1
    elif(age_match > 3 and age_match < 8):
        age_label.config(
            text='Within the area, similar ages are at risk based on previous records.', fg=risk2_color)
        age_risk = 2
    elif(age_match > 7):
        age_label.config(
            text='Within the area, similar ages are at high risk based on previous records.', fg=risk3_color)
        age_risk = 3

    return sex_risk, age_risk


def general_risk(q, s, a):
    if (not q and not s and not a):
        risk_label.config(text="You are at no risk", fg=risk0_color)
    elif (q <= 1 and s <= 1 and a <= 1):
        risk_label.config(text="You should be cautious", fg=risk1_color)
    elif (q <= 2 and s <= 2 and a <= 2):
        risk_label.config(text="You may be at risk ", fg=risk2_color)
    elif(q <= 3 and s <= 3 and a <= 3):
        risk_label.config(text="You are not safe", fg=risk3_color)
