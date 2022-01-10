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
from subprocess import call
import sys
import shlex
import PySimpleGUI as sg
import os
import time
import requests
import json
import pickle
from xlwt import Workbook
import random
a=random.uniform(0.1,0.3)


with open('userdata.txt') as f:
    user_data = [line.rstrip() for line in f]

class Excel():
    def __init__(self):
        pass

    def reademail(self, emailPath):
        data = pd.read_excel(emailPath, 'Sheet1')
        df = data.to_dict()
        return df

def send_delayed_keys(element, text, delay=a):
    for c in text:
        endtime = time.time() + delay
        element.send_keys(c)
        time.sleep(endtime - time.time())


wb = Workbook()

sheet1 = wb.add_sheet('Sheet 1')
sheet1.col(0).width = 7000
sheet1.col(1).width = 7000
sheet1.col(2).width = 7000
sheet1.col(3).width = 3000


emailPath = "emailList.xlsx"
reademail = Excel()
emailList = reademail.reademail(emailPath)
l = len(emailList['username'])
E_num = l + 1
print('Start\n')
for i in range(l):
    temp = {
        'proxy': emailList['proxy'][i],
        'userAgent': emailList['userAgent'][i],
        'Url': emailList['Url'][i],
        'firstName': emailList['firstName'][i],
        'lastName': emailList['lastName'][i],
        'username': emailList['username'][i],
        'Passwd': emailList['Passwd'][i],
        'ConfirmPasswd': emailList['ConfirmPasswd'][i],
        'RecoveryEmail': emailList['RecoveryEmail'][i],
        'Month': emailList['Month'][i],
        'Day': emailList['Day'][i],
        'Year': emailList['Year'][i],
        'Gender': emailList['Gender'][i],
        'Country': emailList['Country'][i],
        'symbol': emailList['symbol'][i]
    }
    print("Username: ", emailList['username'][i])
    print("Password:", emailList['Passwd'][i] + '\n')
    print("proxy: ", emailList['proxy'][i])

    ########## User Agent
    #options = webdriver.ChromeOptions()
    chromedriver = utilities.findChromeDriverVersion()
    chrome_options = Options()
    chrome_options.add_argument("user-agent=userAgent")
    chrome_options.add_argument('--deny-permission-prompts')
    ##chrome_options.add_argument('--headless')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_experimental_option("prefs", {'profile.default_content_setting_values.geolocation': 2})
    chrome_options.add_extension('LocalStorageManager.crx')
    chrome_options.add_extension('EditThisCookie.crx')
    driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver)

    #File_object = open(a+"File_Name","Access_Mode")
    url = emailList['Url'][i]
    fileIDs = open("SessionExec.txt", "w")
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    print("Session ID", session_id)
    print("Executor Url", executor_url)
    fileIDs.write(session_id+"\n"+executor_url)
    fileIDs.close()
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(2)


    ##Das hier später benutzen um an der Excel den Anfangsbuchstaben vom Nachnamen und den Vornamen einzufügen!!!
    #firstName = driver.find_element_by_id('firstName')
    #send_delayed_keys(firstName, emailList['firstName'][i])

    #lastName = driver.find_element_by_id('lastName')
    #send_delayed_keys(lastName, emailList['lastName'][i])

    #username = driver.find_element_by_id('username')
    #send_delayed_keys(username, emailList['username'][i])

    #time.sleep(1)
    #Passwd = driver.find_element_by_name('Passwd')
    #send_delayed_keys(Passwd, emailList['Passwd'][i])

    #time.sleep(1)
    #ConfirmPasswd = driver.find_element_by_name('ConfirmPasswd')
    #send_delayed_keys(ConfirmPasswd, emailList['ConfirmPasswd'][i])

    #time.sleep(1)

    #driver.find_element_by_xpath('//*[@class="RveJvd snByac"]').click()

    #Hier Telefonnummer Code:
    #driver.find_element_by_xpath('//*[@class="_ap _d0 _dm _ar _aa _ab _ac _ad _ae _bk _bl _bm _bn _bp _bq _br _bs _bt _bu _af _ag _ah _ai _bz _c0 _c1 _b5 _c2 _bv _bw _bx _by"]').click()

    #time.sleep(1)
    #element1 = find_element_by_xpath('//span[contains(text(), "Russia")]')

    ########################################################### API #########################
    print("Verify Your Phone number!!")
    time.sleep(1)

    api_key = user_data[0]

    country = '43' #str(emailList['Country'][i])
    operator = 'any'
    service = 'ub'
    ref = '1074993'
    forward = '0'
    phoneException = '1'

    status_ready = '1'
    status_complete = '6'
    status_ban = '8'

    ######## Change of activation status

    access_ready = 'ACCESS_READY'  # number readiness confirmed
    access_ready_get = 'ACCESS_RETRY_GET'  # waiting for a new sms
    access_activation = 'ACCESS_ACTIVATION'  # service successfully activated
    access_cancel = 'ACCESS_CANCEL'  # activation canceled

    ######## Get activation status:

    status_wait = 'STATUS_WAIT_CODE'  # waiting for sms
    status_wait_retry = "STATUS_WAIT_RETRY"  # waiting for code clarification
    status_wait_resend = 'STATUS_WAIT_RESEND'  # waiting for re-sending SMS *
    status_cancel = 'STATUS_CANCEL'  # activation canceled
    status_ok = "STATUS_OK"  # code received

    # POSSIBLE MISTAKES: (ERROR)
    error_sql = 'ERROR_SQL'  # SQL-server error
    no_activation = 'NO_ACTIVATION'  # activation id does not exist
    bad_service = 'BAD_SERVICE'  # incorrect service name
    bad_status = 'BAD_STATUS'  # incorrect status
    bad_key = 'BAD_KEY'  # Invalid API key
    bad_action = 'BAD_ACTION'  # incorrect action

    # Balance
    balance = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getBalance')
    info = balance.text
    b1, b2 = info.split(":")
    print("Balance: ", b2)

    # number of available phones
    find_numbers = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getNumbersStatus&country=' + country + '&operator=' + operator)
    num_numbers = json.loads(find_numbers.text)

    a = num_numbers['ub_0']
    if a == '0':
        print('sorry no number available')
        driver.quit()
        sys.exit()
    else:
        print('Available phone numbers: ', a)

        # Order Number
        order_number = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getNumber&service=' + service + '&forward=' + forward + '&operator=' + operator + '&ref=' + ref + '&country=' + country)
        print('buy TEXT: ', order_number.text)
        info = order_number.text
        a, id, phone_number = info.split(":")
        print('Id: ', id)
        phone_number = phone_number[0:]
        print('Phone Number: +', phone_number)

        time.sleep(5)
        plusdruck = driver.find_element_by_xpath('//*[@class="c3 c4 c5 by c6 c7 c8 c1 ao"]')
        plusdruck.send_keys("+")
        time.sleep(1)
        phonenumber = driver.find_element_by_xpath('//*[@class="c3 c4 c5 by c6 c7 c8 c1 ao"]')
        send_delayed_keys(phonenumber, phone_number)
        time.sleep(1)
        #driver.find_element_by_id('mobile').send_keys(Keys.COMMAND + Keys.HOME, Keys.ARROW_RIGHT)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="cl cm c5 cf ae c4 aj cn co c3 cp cq c7 cr cs ct cu cv cw cx"]').click()

        # Activation status
        time.sleep(5)
        ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ready + '&id=' + id + '&forward=' + forward)
        if ch_activation_status.text in access_ready:
            print("number readiness confirmed\n")

            # SMS status
            time.sleep(3)
            get_sms = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getStatus&id=' + id)
            code = get_sms.text

            while status_wait in code or status_ok in code or status_cancel in code or status_wait_resend in code or status_wait_retry in code:
                if code in status_wait:
                    print("wait sometime for SMS")
                    time.sleep(20)
                    get_sms = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getStatus&id=' + id)
                    code = get_sms.text
                elif status_ok in code:
                    tex, m_code = code.split(':')
                    print("Your SMS code: ", m_code)
                    time.sleep(2)
                    actions = ActionChains(driver)
                    actions.send_keys(m_code)
                    actions.perform()
                    #codenumber2 = driver.find_element_by_xpath('//*[@id="PHONE_SMS_OTP-0"').click()
                    #time.sleep(2)
                    #codenumber = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div/div[1]/div[1]/div[2]/div/div/div[1]/div"')
                    #send_delayed_keys(codenumber, m_code)
                    ##time.sleep(2)
                    ##driver.find_element_by_xpath('//*[@class="RveJvd snByac"]').click()
                    # complete_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key='+api_key+'&action=setStatus&status='+status_complete+'&id='+id+'&forward='+forward)
                    # print("PVA complete")
                    break
                else:
                    ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
                    print("Cancel the activation")
                    print("sorry this number has some issues")
                    #driver.quit()
                    #sys.exit()

        else:
            ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
            print("Cancel the activation")
            print("sorry this number has some issues")
            #driver.quit()
            #sys.exit()

    ###Ab hier muss die Pasted Nummer gecleared werden und durch Faker Package muss ne Email gefaked werden.###
    time.sleep(2)
    fotze = driver.find_element_by_xpath('//*[@class="bc dz e0 e1 e2 e3 e4 e5 e6 e7 c3 ao e8 e9 c7 ea eb fk fl d8 c5 d9 by bu ee ef"]')
    fotze.send_keys(Keys.CONTROL +"a")
    fotze.send_keys(Keys.DELETE)
    time.sleep(1)
    f = Faker()
    fotze.send_keys(f.first_name())
    time.sleep(2)
    emailfeld = driver.find_element_by_xpath('//*[@class="bc dz e0 e1 e2 e3 e4 e5 e6 e7 c3 ao e8 e9 c7 ea eb fk fl d8 c5 d9 by bu ee ef"]')
    emailfeld.send_keys(f.email())
    time.sleep(1)
    driver.find_element_by_xpath('//*[@class="cl cm c5 cf ae c4 aj cn co c3 cp cq c7 cr cs ct cu cv cw cx"]').click()

    ####Passwort(22WeEatGood)####
    time.sleep(2)
    pw = driver.find_element_by_xpath('//*[@class="bc dz e0 e1 e2 e3 e4 e5 e6 e7 c3 ao e8 e9 c7 ea eb fk fl d8 c5 d9 by bu ee ef"]')
    pw.clear()
    time.sleep(1)
    pw.send_keys("22WeEatGood")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@class="cl cm c5 cf ae c4 aj cn co c3 cp cq c7 cr cs ct cu cv cw cx"]').click()

    ###Name und Nachname(Faker)###

    ###VORNAME###
    time.sleep(2)
    vname = driver.find_element_by_xpath('//*[@id="FIRST_NAME"]')
    vname.clear()
    time.sleep(1)
    vname.send_keys(user_data[1])

    ###NACHNAME###
    time.sleep(2)
    nachname = driver.find_element_by_xpath('//*[@id="LAST_NAME"]')
    nachname.clear()
    time.sleep(1)
    nachname.send_keys(user_data[2], f.last_name())
    time.sleep(1)
    driver.find_element_by_xpath('//*[@class="cl cm c5 cf ae c4 aj cn co c3 cp cq c7 cr cs ct cu cv cw cx"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@class="bw dl dm g8 fu ft g9 ga bc dg dh di dj gb gc gd ge gf gg gh gi dn dp dq do c3 fq g6 gj gk gl gm gn go gp gq"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@class="cl cm c5 cf ae c4 aj cn co c3 cp cq c7 cr cs ct cu cv cw cx"]').click()


    ##Ab hier Endet alles und SMS Activate sollte das Finale Signal ausgeben
    complete = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key='+api_key+'&action=setStatus&status='+ status_complete +'&id='+id+'&forward='+forward)
    print("Now, this account is completed.\n")
    time.sleep(360000)
