# At-RisK

## Description
At RisK? is a program designed to help families and individuals identify and assess the risk level that they are at from Sexual Offenders.
Based on the User's Address, Sex, and Age, it determines if the individual is more at risk compared to nearby offender's previous offenses.
It uses a publically available database and public information to compute calculations and assessments.
Due to the API used to retrieve coordinate data from addresses, some addresses use older street names or different nearby zipcodes.

## Instructions
* Install dependencies:
  * Assuming Python and Pip are properly installed, in a new command window type:
    * `pip install geopy`
    * `pip install bs4`
    * `pip install urllib3`

* In a command window with the directory in this folder, type:
  * `python main.py`

* Fill in the input fields according to their label

## Technologies
* Tkinter
* Geopy
* Urllib3
* BeautifulSoup
* API Requests

## Restrictions
* The program currently only contains information regarding Texas Sex Offenders, as other states' databases are private
