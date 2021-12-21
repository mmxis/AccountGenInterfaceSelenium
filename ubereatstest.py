from xlwt import Workbook
import xlrd
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import sys
import os
import time
import requests
import json
from xlwt import Workbook
import random
a=random.uniform(0.1,0.3)


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
    options = webdriver.ChromeOptions()
    options = Options()
    options.add_argument("user-agent=userAgent")
    driver = webdriver.Chrome(options=options)

    #driver = webdriver.Chrome()

    url = emailList['Url'][i]
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(2)

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

    api_key = 'xyxyxyxyxy'

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
        phone_number = phone_number[2:]
        print('Phone Number: +49', phone_number)

        time.sleep(5)
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
                    codenumber = driver.find_element_by_id('code')
                    send_delayed_keys(codenumber, m_code)
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@class="RveJvd snByac"]').click()
                    # complete_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key='+api_key+'&action=setStatus&status='+status_complete+'&id='+id+'&forward='+forward)
                    # print("PVA complete")
                    break
                else:
                    ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
                    print("Cancel the activation")
                    print("sorry this number has some issues")
                    driver.quit()
                    sys.exit()

        else:
            ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
            print("Cancel the activation")
            print("sorry this number has some issues")
            driver.quit()
            sys.exit()

    time.sleep(3)
    phone_url = "https://auth.uber.com/v2/?breeze_local_zone=dca1&next_url=https%3A%2F%2Fwww.ubereats.com%2Flogin-redirect%2F%3Fcampaign%3Dsignin_universal_link%26marketing_vistor_id%0%26redirect%3D%252Fde&state=0%3D&x-uber-analytics-session-id=0"
    veryfi_url = "https://auth.uber.com/v2/?breeze_local_zone=dca1&next_url=https%3A%2F%2Fwww.ubereats.com%2Flogin-redirect%2F%3Fcampaign%3Dsignin_universal_link%26marketing_vistor_id%0%26redirect%3D%252Fde&state=0%3D&x-uber-analytics-session-id=0"
    main_url = "https://auth.uber.com/v2/?breeze_local_zone=dca1&next_url=https%3A%2F%2Fwww.ubereats.com%2Flogin-redirect%2F%3Fcampaign%3Dsignin_universal_link%26marketing_vistor_id%0%26redirect%3D%252Fde&state=0%3D&x-uber-analytics-session-id=0"
    a = driver.current_url
    while veryfi_url in a or phone_url in a or main_url in a:
        if main_url in a:
            break
        else:
            time.sleep(2)
            print("This is not correct page\nplz wait some time")
            a = driver.current_url

    driver.find_element_by_id('mobile').clear()

    time.sleep(1)
    RecoveryEmail = driver.find_element_by_xpath('//*[@spellcheck="false"]')
    send_delayed_keys(RecoveryEmail, emailList['RecoveryEmail'][i])

    time.sleep(1)
    driver.find_element_by_xpath('//*[@aria-label="Day"]').send_keys(int(emailList['Day'][i]))

    time.sleep(1)
    element = driver.find_element_by_id('month')
    drp = Select(element)
    drp.select_by_visible_text(emailList['Month'][i])

    time.sleep(1)
    driver.find_element_by_xpath('//*[@aria-label="Year"]').send_keys(int(emailList['Year'][i]))

    time.sleep(1)
    element = driver.find_element_by_id('gender')
    drp = Select(element)
    drp.select_by_visible_text(emailList['Gender'][i])

    time.sleep(1)
    driver.find_element_by_xpath('//*[@class="RveJvd snByac"]').click()

    time.sleep(5)
    current_Url = driver.current_url
    du_Url = 'https://auth.uber.com/login/?uber_client_name=eatsWebSignUp'
    if du_Url in current_Url:
        # time.sleep(2)
        #driver.find_element_by_xpath('//*[@class="Ce1Y1c"]').click()
        #time.sleep(2)
        #driver.find_element_by_xpath('//*[@class="Ce1Y1c"]').click()
        #time.sleep(2)
        #driver.find_element_by_xpath('//*[@class="Ce1Y1c"]').click()
        #time.sleep(10)
        driver.find_element_by_xpath('//*[@class="RveJvd snByac"]').click()

        time.sleep(10)
        cur_url = driver.current_url
        fail_url = 'https://auth.uber.com/v2/?breeze_local_zone=dca1&next_url=https%3A%2F%2Fwww.ubereats.com%2Flogin-redirect%2F%3Fcampaign%3Dsignin_universal_link%26marketing_vistor_id%0%26redirect%3D%252Fde&state=0%3D&x-uber-analytics-session-id=0'
        if fail_url in cur_url:
            print("This account take some time")
            print("Plz Cut this browser yourself\n")
            time.sleep(3)

            sheet1.write(i, 0, emailList['username'][i])
            sheet1.write(i, 1, emailList['Passwd'][i])
            sheet1.write(i, 2, emailList['RecoveryEmail'][i])
            sheet1.write(i, 3, "Bad")
            wb.save('verify_Emails.xls')

        else:
            time.sleep(3)
            sheet1.write(i, 0, emailList['username'][i])
            sheet1.write(i, 1, emailList['Passwd'][i])
            sheet1.write(i, 2, emailList['RecoveryEmail'][i])
            sheet1.write(i, 3, "Ok")
            wb.save('verify_Emails.xls')
    else:
        # time.sleep(2)
        # driver.find_element_by_xpath('//*[@class="RveJvd snByac"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="Ce1Y1c"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="Ce1Y1c"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="Ce1Y1c"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="RveJvd snByac"]').click()

        time.sleep(10)
        cur_url = driver.current_url
        fail_url = 'https://auth.uber.com/v2/?breeze_local_zone=dca1&next_url=https%3A%2F%2Fwww.ubereats.com%2Flogin-redirect%2F%3Fcampaign%3Dsignin_universal_link%26marketing_vistor_id%0%26redirect%3D%252Fde&state=0%3D&x-uber-analytics-session-id=0'
        if fail_url in cur_url:
            print("This account take some time")
            print("Plz Cut this browser yourself")
            time.sleep(3)

            sheet1.write(i, 0, emailList['username'][i])
            sheet1.write(i, 1, emailList['Passwd'][i])
            sheet1.write(i, 2, emailList['RecoveryEmail'][i])
            sheet1.write(i, 3, "Bad")
            wb.save('verify_Emails.xls')
        else:
            time.sleep(3)

            sheet1.write(i, 0, emailList['username'][i])
            sheet1.write(i, 1, emailList['Passwd'][i])
            sheet1.write(i, 2, emailList['RecoveryEmail'][i])
            sheet1.write(i, 3, "Ok")
            wb.save('verify_Emails.xls')
    complete = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key='+api_key+'&action=setStatus&status='+ status_complete +'&id='+id+'&forward='+forward)
    print("Now, this account is completed.\n")
    driver.quit()
    time.sleep(20000)
