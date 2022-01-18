import keyboard
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
import socket
from xlwt import Workbook
import xlrd
import pandas as pd
from build import utilities
from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import PySimpleGUI as sg
import sys
import shlex
import os
import time
import requests
import json
import pickle
import urllib3
from xlwt import Workbook
import random

# executor_url = driver.command_executor._url
# session_id = driver.session_id


def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver


f3 = open('SessionExec.txt', 'r')
line_to_read = [1]

for position, executor in enumerate(f3):
    if position in line_to_read:
        exesh = executor
        print(executor)
f3.close()

f3 = open('SessionExec.txt', 'r')
line_to_read = [0]

for position, sessionid in enumerate(f3):
    if position in line_to_read:
        SeSHH = sessionid
        print(sessionid)
f3.close()

## Session ID musste in ne neue TXT file gespeichert werden weil WebDriver faxen macht.
f4 = open('SessionIDCartAuto.txt', 'r')
line_to_read = [0]

for position, seshy2 in enumerate(f4):
    if position in line_to_read:
        seshy = seshy2
f4.close()

##define layout
layout = [
    [sg.Button('1.Tabs öffnen(nicht wiederholen)'), sg.Button('2.Kauf abschließen(kann wiederholt werden)')]
]

##Window creation
window = sg.Window('CartAutomate', layout, font='Calibri')

##event handling
while True:
    event, values = window.read()

    if event == '1.Tabs öffnen(nicht wiederholen)':

        ##Automatisierung beginnt hier
        ##3 weitere Tabs werden geöffnet
        sg.Popup("Es werden 3 weitere Tabs geöffnet", "Bitte klicke 'OK' und warte bis du insg. 4 Tabs hast.")
        bro = attach_to_session(exesh, seshy)
        print(bro.current_url)

        ##2nd tab
        bro.execute_script('''window.open("https://www.ubereats.com/de/checkout","_blank");''')
        bro.switch_to.window(bro.window_handles[1])
        from selenium.common.exceptions import NoSuchElementException

        try:
            time.sleep(6)
            bro.find_element_by_xpath("//button[@aria-label='Schließen']").click()
            time.sleep(2)

        except NoSuchElementException:
            ##3rd tab öffnet sich
            bro.execute_script('''window.open("https://www.ubereats.com/de/checkout","_blank");''')
            bro.switch_to.window(bro.window_handles[2])

            try:
                time.sleep(6)
                bro.find_element_by_xpath("//button[@aria-label='Schließen']").click()
                time.sleep(2)

            except NoSuchElementException:
                ##4th tab öffnet sich
                bro.execute_script('''window.open("https://www.ubereats.com/de/checkout","_blank");''')
                bro.switch_to.window(bro.window_handles[3])

            try:
                time.sleep(6)
                bro.find_element_by_xpath("//button[@aria-label='Schließen']").click()
                time.sleep(2)

            except NoSuchElementException:
                print("Alle Tabs wurden erfolgreich geöffnet")
                sg.Popup("Alle Tabs wurden efolgreich geöffnet", "Richte nun deine Uhrzeiten für deine Abholung/Lieferung ein und klicke den Button '2.Kauf Abschließen'.")
    elif event == '2.Kauf abschließen(kann wiederholt werden)':
        bro = attach_to_session(exesh, seshy)
        bro.switch_to.window(bro.window_handles[1])
        bro.execute_script(open("./cookiechanger.js").read())
        time.sleep(1)
        bro.execute_script(open("./locstoragechanger.js").read())
        time.sleep(2)
        bro.switch_to.window(bro.window_handles[2])
        bro.find_element_by_xpath("//*[@id='main-content']/div/div[3]/div[2]/div[2]/div[5]/div/div[1]/button").click()
        time.sleep(2)
        from selenium.common.exceptions import NoSuchElementException

        try:
            time.sleep(3)
            bro.find_element_by_xpath("//*[@id='main-content']/div[4]/div/div/div[2]/div[3]/button[1]").click()
            #bro.find_element_by_class_name('Zahlungspflichtig bestellen').click()
            time.sleep(3)

        except NoSuchElementException:
            time.sleep(3)
            #bro.find_element_by_class_name('Zahlungspflichtig bestellen').click()
            bro.find_element_by_xpath("//*[@id='main-content']/div/div[3]/div[2]/div[2]/div[5]/div/div[1]/button").click()
        #bro.execute_script("console.log('test')")
    elif event == sg.WINDOW_CLOSED:
        break

##Fetch Codes werden in den 2.Tab eingegeben.

#bro.switch_to.window(bro.window_handles[1])
#bro.switch_to.window(bro.window_handles[2])
#bro.get('https://www.ubereats.com/de/checkout')  ## Uber Cart Link einfügen
#bro = attach_to_session('http://127.0.0.1:60279', '0bec01fd1df8c21f53d51166b8eef3a5')
#bro.find_element_by_id('tsuid1').click()

### Der Grund warum es nicht klappt liegt daran dass Selenium bzw. urllib nichts mit "localhost" anfangen kann.
### Ersetze "localhost" mit "127.0.0.1" und es sollte laufen.