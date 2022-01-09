# first try for a simple UI
import PySimpleGUI as sg

# initialize needed variables
with open('api_key.txt') as f:
    api_key = f.readlines()


# define the layout
layout = [
    [sg.Text('WeEatGood', font=("Calibri", 50), text_color='pink')],
    [sg.Text('Gib deinen SMS-Activate API-Key ein:')],
    [sg.Text('API-Key'), sg.InputText(api_key)],
    [sg.Button('Account erstellen'), sg.Button('Schritte im Warenkorb durchführen')]
]

# create the window
window = sg.Window('WeEatGood', layout, font='Calibri')

while True:
    event, values = window.read()
    if event == 'Account erstellen':
        f = open('api_key.txt','w')
        f.write(api_key)
        f.close()

        os.system('ubereats.py')

