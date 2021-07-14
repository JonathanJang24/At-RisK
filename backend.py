import tkinter as tk
import os
import re
from tkinter.constants import CENTER, LEFT, UNDERLINE
from tkinter.font import BOLD
import urllib.parse
import requests
import geopy.distance
import math
from custom_errors import InvalidSexError, ImpossibleAgeError
from openData import addy_dict, name_dict, offense_dict, indv_dict, off_code_dict

bgColor, fColor, entryBg, entryFg = '#333333', '#73d0b3', '#595959', '#83dec2'
risk0_color, risk1_color, risk2_color, risk3_color = '#97e8c1', '#f7ff66', '#ffba66', '#f55d5d'
myFont = 'PierSans-Light'


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
                    print(x)
                    closest_distance = distance
                    closest_offender = x

    offender_label.config(text="The closest offender is %f miles away. They live at %s" % (
        closest_distance, re.sub(r'\t', '', addy_dict[closest_offender][0])))
    return close_dict, closest_distance, closest_offender


def analyze(address, zipcode, sex, age):
    global risk_label, sex_label, age_label, quantity_label, offender_label
    new_window = tk.Tk()
    new_window.geometry('400x400')
    new_window.resizable(False, False)
    new_window.configure(background=bgColor)

    risk_label = tk.Label(new_window,
                          text="", font=(myFont, 20, BOLD, UNDERLINE), bg=bgColor)
    quantity_label = tk.Label(new_window, text="test", font=(
        myFont, 12), bg=bgColor, wraplength=380, justify=LEFT)
    age_label = tk.Label(new_window, text="", font=(
        myFont, 12), bg=bgColor, wraplength=380, justify=LEFT)
    sex_label = tk.Label(new_window, text="", font=(
        myFont, 12), bg=bgColor, wraplength=380, justify=LEFT)
    offender_label = tk.Label(new_window, text="", fg=fColor, bg=bgColor, font=(
        myFont, 12), justify=LEFT, wraplength=380)

    risk_label.place(x=200, y=20, anchor="center")
    quantity_label.place(x=10, y=70, anchor='w')
    sex_label.place(x=10, y=120, anchor='w')
    age_label.place(x=10, y=170, anchor='w')
    offender_label.place(x=10, y=220, anchor='w')

    try:
        if(sex.upper() != 'M' and sex.upper() != 'F'):
            raise InvalidSexError

        if(int(age) < 0 or int(age) > 122):
            raise ImpossibleAgeError

        url = 'https://nominatim.openstreetmap.org/search/' + \
            urllib.parse.quote(address+" " + zipcode) + '?format=json'
        response = requests.get(url).json()
        lat = response[0]['lat']
        lon = response[0]['lon']
        user_coords = (lat, lon)

        close_offenders, closest_distance, closest_offender = narrow(
            user_coords, zipcode)

        risk_1 = quantity_risk(close_offenders)
        sex_risk, age_risk = specific_level(close_offenders, sex, age)
        general_risk(risk_1, sex_risk, age_risk)

    except IndexError:
        print("Invalid Address")
        new_window.destroy()
    except ValueError:
        print('Invalid Zipcode')
        new_window.destroy()
    except InvalidSexError:
        print('Invalid Sex')
        new_window.destroy()
    except ImpossibleAgeError:
        print('Impossible Age')
        new_window.destroy()
    except Exception as e:
        print(e)
    new_window.mainloop()


def quantity_risk(dict):
    if(len(dict) == 0):
        quantity_label.config(
            text='There are no convicted offenders in a 2 mile radius', fg=risk0_color)
    elif(len(dict) > 0 and len(dict) < 6):
        quantity_label.config(
            text='There is a small quantity of convicted offenders in a 2 mile radius', fg=risk1_color)
    elif(len(dict) > 5 and len(dict) < 11):
        quantity_label.config(
            text='There is a moderate presence of convicted offenders in a 2 mile radius', fg=risk2_color)
    elif(len(dict) > 10):
        quantity_label.config(
            text='There is a relativley large amount of convicted offenders in a 2 mile radius', fg=risk3_color)


def specific_level(dict, user_sex, user_age):
    global sex_label, age_label

    sex_match = 0
    age_match = 0
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
    elif(sex_match > 4 and sex_match < 8):
        sex_label.config(
            text="Within the area, this sex is at risk based on previous records.", fg=risk2_color)
    elif(sex_match > 8):
        sex_label.config(
            text="Within the area, this sex is at high risk based on previous records.", fg=risk3_color)

    if(age_match == 0):
        age_label.config(
            text="Within the area, similar ages have not previously been targeted.", fg=risk0_color)
    elif(age_match > 0 and age_match < 4):
        age_label.config(
            text='Within the area, similar ages are at slight risk based on previous records.', fg=risk1_color)
    elif(age_match > 4 and age_match < 8):
        age_label.config(
            text='Within the area, similar ages are at risk based on previous records.', fg=risk2_color)
    elif(age_match > 8):
        age_label.config(
            text='Within the area, similar ages are at high risk based on previous records.', fg=risk3_color)

    return sex_match, age_match


def general_risk(q, s, a):

    risk_label.config(text="You are at no risk", fg=risk0_color)
