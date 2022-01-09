# first try for a simple UI
import PySimpleGUI as sg
from subprocess import call

# import user data

with open('userdata.txt') as f2:
    user_data =  [line.rstrip() for line in f2]


# define the layout
layout = [
    [sg.Text('WeEatGood', font=("Calibri", 50), text_color='pink')],
    [sg.Text('Gib deinen SMS-Activate API-Key ein:')],
    [sg.Text('API-Key'), sg.InputText(user_data[0], key = 'api_key_field')],
    [sg.Text('Gib deinen Vornamen und den ersten Buchstaben des Nachnamens ein:')],
    [sg.Text('Vorname'), sg.InputText(user_data[1], key = 'surname_field')],
    [sg.Text('Nachname'), sg.InputText(user_data[2], key = 'name_field')],
    [sg.Button('Account erstellen'), sg.Button('Schritte im Warenkorb durchführen')]
]

# create the window
window = sg.Window('WeEatGood', layout, font='Calibri')

# event handling
while True:
    event, values = window.read()
    if event == 'Account erstellen':
        #if ''.join(values['api_key_field']) != ''.join(api_key):
#        if ''.join(values['api_key_field']).replace("('","").replace("',)","") != ''.join(api_key):
        if values['api_key_field'] != user_data[0]:
            f = open('userdata.txt', 'w')
            f.write(values['api_key_field']+"\n"+user_data[1]+"\n"+user_data[2])
            user_data[0]=values['api_key_field']
            f.close()
        if values['surname_field'] != user_data[1]:
            f = open('userdata.txt', 'w')
            f.write(user_data[0]+"\n"+values['surname_field']+"\n"+user_data[2])
            user_data[1]=values['surname_field']
            f.close()
        if values['name_field'] != user_data[2]:
            f = open('userdata.txt', 'w')
            f.write(user_data[0]+"\n"+user_data[1]+"\n"+values['name_field'])
            user_data[2]=values['name_field']
            f.close()
        window.close()
        call(["python", "ubereatstest.py"])

    elif event == sg.WINDOW_CLOSED:
        break




