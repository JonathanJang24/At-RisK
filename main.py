from re import X
import tkinter as tk
from tkinter.constants import CENTER, FLAT, GROOVE, LEFT, RAISED, RIDGE, SOLID, SUNKEN, UNDERLINE
from tkinter.font import BOLD, ITALIC
from backend import analyze, destroy
from custom_errors import InvalidSexError, ImpossibleAgeError

# Declaring Colors
bgColor, fColor, entryBg, entryFg, errorColor = '#333333', '#73d0b3', '#595959', '#83dec2', '#fa594d'

# Initalize Tkitner Frame
root = tk.Tk()
root.geometry('500x260')
root.configure(background=bgColor)
root.title('At Risk?')
root.resizable(False, False)
myFont = 'PierSans-Light'


def update():
    try:
        error_label.config(text="")
        analyze(addy.get(), zip.get(), sex.get(), age.get())
    except IndexError:
        error_label.config(text="Invalid Address")
        destroy()
    except ValueError:
        error_label.config(text='Invalid Zipcode')
        destroy()
    except InvalidSexError:
        error_label.config(text='Invalid Sex')
        destroy()
    except ImpossibleAgeError:
        error_label.config(text='Impossible Age')
        destroy()
    except:
        error_label.config(text='Error')
        destroy()


def query():
    global error_label, addy, zip, sex, age
    # Declare Widgets
    search_button = tk.Button(text='Analyze', font=(
        myFont, 16, BOLD, UNDERLINE, ITALIC), bg=entryBg, fg=entryFg, activebackground=bgColor, activeforeground=fColor, command=update)
    instruction = tk.Label(text='Enter the information prompted to find out your risk level.', font=(
        myFont, 13, BOLD), bg=bgColor, fg=fColor)
    addy_label = tk.Label(text='Address', font=(
        myFont, 12), bg=bgColor, fg=fColor)
    zip_label = tk.Label(text='Zipcode', font=(
        myFont, 12), bg=bgColor, fg=fColor)
    sex_label = tk.Label(text='Sex', font=(
        myFont, 12), bg=bgColor, fg=fColor)
    age_label = tk.Label(text='Age', font=(
        myFont, 12), bg=bgColor, fg=fColor)
    addy = tk.Entry(root, bg=entryBg, font=(
        myFont, 12), fg=entryFg)
    zip = tk.Entry(root, bg=entryBg, font=(
        myFont, 12), fg=entryFg)
    sex = tk.Entry(root, bg=entryBg, font=(
        myFont, 12), fg=entryFg)
    age = tk.Entry(root, bg=entryBg, font=(
        myFont, 12), fg=entryFg)

    error_label = tk.Label(root, text='', bg=bgColor,
                           fg=errorColor, font=myFont)

    # Place widgets
    instruction.place(x=12, y=50)
    addy_label.place(x=10, y=80)
    zip_label.place(x=10, y=120)
    sex_label.place(x=10, y=160)
    age_label.place(x=10, y=200)
    addy.place(x=80, y=80, width=300, height=30)
    zip.place(x=80, y=120, width=300, height=30)
    age.place(x=80, y=200, width=300, height=30)
    sex.place(x=80, y=160, width=300, height=30)
    search_button.place(x=395, y=125)
    error_label.place(x=250, y=245, anchor='center')

# start button function


def start():
    # Clears Start Screen
    for widgets in root.winfo_children():
        if str(widgets) != '.!label' and str(widgets) != '.!label8':
            widgets.destroy()
    # Calls second window
    query()


# Starting Screen Widgets
title_label = tk.Label(text="At RisK?", font=(
    myFont, 24, 'underline', 'bold'), background=bgColor, fg=fColor)
title_label.place(x=200, y=10)

desc_label = tk.Label(
    text="At RisK? Is a tool designed to help\nfamilies/individuals recognize if\nloved ones are at a higher level of\nrisk in their community from\npredators and offenders.", font=(myFont, 15, BOLD), justify=LEFT, background=bgColor, fg=fColor)
desc_label.place(x=10, y=80)

start_button = tk.Button(text='Get\nStarted', command=start,
                         font=(myFont, 22, ITALIC, BOLD, UNDERLINE), background=entryBg, fg=entryFg, activebackground=bgColor, activeforeground=fColor)
start_button.place(x=365, y=100)

root.mainloop()
