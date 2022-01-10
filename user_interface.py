# first try for a simple UI
import PySimpleGUI as sg
from subprocess import call
from selenium import webdriver
from build import utilities
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
# import user data
# executor_url = driver.command_executor._url
# session_id = driver.session_id

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
    [sg.Button('Accountdaten sichern'), sg.Button('Schritte im Warenkorb durchführen'), sg.Button('Script Starten!')]
]

# create the window
window = sg.Window('WeEatGood', layout, font='Calibri')



# event handling
while True:
    event, values = window.read()
    if event == 'Accountdaten sichern':
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
        else:
            sg.Popup("Erfolg", "Deine angegebenen Daten wurden erfolgreich gesichert!")
    elif event == 'Script Starten!':
            call(["python", "ubereatstest.py"])
    elif event == 'Schritte im Warenkorb durchführen':
            sg.Popup("kommt noch!")
            chromedriver = utilities.findChromeDriverVersion()
            chrome_options = Options()
            driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver)
            driver.get('chrome://inspect/#devices')
            #Automatisierung mit Cookies und Local Storage einführen
    elif event == sg.WINDOW_CLOSED:
        break

# cookies = browser.get_cookies()
# for cookie in cookies:
# print(cookie)




