import tkinter as tk
import os
import re
import urllib.parse
import requests
import geopy.distance
import math
from custom_errors import InvalidSexError, ImpossibleAgeError
from openData import addy_dict, name_dict, offense_dict, indv_dict, off_code_dict

bgColor, fColor, entryBg, entryFg = '#333333', '#73d0b3', '#595959', '#83dec2'
risk0_color, risk1_color, risk2_color, risk3_color = '#32a852', '#f7ff66', '#ffba66', '#f55d5d'
myFont = 'PierSans-Light'


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


def general_level(dict):
    if len(dict) == 0:
        return 0
    elif len(dict) > 0 and len(dict) < 4:
        return 1
    elif len(dict) > 3 and len(dict) < 9:
        return 2
    else:
        return 3


def specific_level(dict, user_sex, user_age):
    sex_match = 0
    age_match = 0
    for x in dict:
        if offense_dict[x][2] == user_sex.upper():
            sex_match += 1
        # If offender's previous victim's age is +- 3 of individual's age
        if(int(offense_dict[x][1])-3 <= int(user_age) and int(offense_dict[x][1])+3 >= int(user_age)):
            age_match += 1
    return sex_match, age_match


def analyze(address, zipcode, sex, age):
    new = tk.Toplevel()
    new.geometry('400x400')
    new.resizable(False, False)
    new.configure(background=bgColor)

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

        close_offenders = narrow(user_coords, zipcode)

        risk_1 = general_level(close_offenders)
        sex_risk, age_risk = specific_level(close_offenders, sex, age)

    except IndexError:
        print("Invalid Address")
        new.destroy()
    except ValueError:
        print('Invalid Zipcode')
        new.destroy()
    except InvalidSexError:
        print('Invalid Sex')
        new.destroy()
    except ImpossibleAgeError:
        print('Impossible Age')
        new.destroy()
    except Exception as e:
        print(e)

    risk_label = tk.Label(font=myFont)
