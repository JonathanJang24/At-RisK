import tkinter as tk
from tkinter.constants import FLAT, GROOVE, LEFT, RAISED, RIDGE, SOLID, SUNKEN, UNDERLINE
from tkinter.font import BOLD, ITALIC
from backend import analyze

# Declaring Colors
bgColor, fColor, entryBg, entryFg = '#333333', '#73d0b3', '#595959', '#83dec2'

# Initalize Tkitner Frame
root = tk.Tk()
root.geometry('500x250')
root.configure(background=bgColor)
root.title('At Risk?')
root.resizable(False, False)
text = tk.Text(root)
myFont = 'PierSans-Light'


def query():

    # Declare Widgets
    search_button = tk.Button(text='Analyze', font=(
        myFont, 16, BOLD, UNDERLINE, ITALIC), bg=entryBg, fg=entryFg, activebackground=bgColor, activeforeground=fColor, command=lambda: analyze(addy.get(), zip.get(), sex.get(), age.get()))
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
    age = tk.Entry(root, bg=entryBg, font=(
        myFont, 12), fg=entryFg)
    sex = tk.Entry(root, bg=entryBg, font=(
        myFont, 12), fg=entryFg)

    # Place widgets
    instruction.place(x=12, y=50)
    addy_label.place(x=10, y=80)
    zip_label.place(x=10, y=120)
    sex_label.place(x=10, y=160)
    age_label.place(x=10, y=200)
    addy.place(x=80, y=80, width=300, height=30)
    zip.place(x=80, y=120, width=300, height=30)
    age.place(x=80, y=160, width=300, height=30)
    sex.place(x=80, y=200, width=300, height=30)
    search_button.place(x=395, y=125)


# start button function


def start():
    # Clears Start Screen
    for widgets in root.winfo_children():
        if str(widgets) != '.!label':
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
start_button.place(x=360, y=100)

root.mainloop()
