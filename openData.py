import re

addy_file, name_file, offense_file, indv_file, off_code_file = open('data\Address.txt'), open(
    'data\\NAME.txt'), open('data\\Offense.txt'), open('data\\INDV.txt'), open('data\\OFF_CODE_SOR.txt')
addy_dict, name_dict, offense_dict, indv_dict, off_code_dict = {}, {}, {}, {}, {}

for x in addy_file:
    temp = x.split('\t')
    id = temp[1]
    temp_list = []
    for y in temp[2:9]:
        if(y == ''):
            continue
        else:
            temp_list.append(y)
    addy = ' '.join(temp_list)
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
    indv_dict[temp[0]] = sid

for x in off_code_file:
    temp = x.split('\t')
    if(temp[2] == 'TX'):
        try:
            key = temp[3]
            offense = temp[5]
            off_code_dict[key] = offense
        except:
            pass
    else:
        continue
