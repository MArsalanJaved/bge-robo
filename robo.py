import os

import pandas as pd 
from datetime import datetime,timedelta
from random import randint
import shutil

credentials = pd.read_csv('Credentials.csv')
accountListing = pd.read_csv('AccountListing.csv')

accountListing = accountListing.astype({"AccountOwnerID": str, "AccountNumber": str})
credentials = credentials.astype({"AccountOwnerID": str})


accountListing['LastDownloadBillDate'] = pd.to_datetime(accountListing['LastDownloadBillDate'])

accountListing['AccountNumber'] = accountListing['AccountNumber'].apply(lambda x: '0'+x if len(x)<10 else x )
credentials['LastUpdated'] = pd.to_datetime(credentials['LastUpdated'])
today = datetime.now()

def remove_overlay(driver):
    try:
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.acsInviteButton:nth-child(6)'))
        ).click()
    except:
        pass
    
def check_login(driver, one_credential,wait,page_number):
    if 'Login' in driver.current_url:
        driver.get("https://www.bge.com/Pages/default.aspx")

        WebDriverWait(driver, wait).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="s4-titlerow"]/header/div/button'))
        ).click()
        username = WebDriverWait(driver, wait).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="Username"]'))
        )
        password = driver.find_element_by_xpath('//*[@id="Password"]')
        username.send_keys(one_credential['Username'])
        password.send_keys(one_credential['Password'])
        
        WebDriverWait(driver, wait).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'ng-form.ng-dirty > div:nth-child(1) > exelon-decorator-simple:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(7)'))
        ).click()
        
    print ('returning None')
    driver.get('https://secure.bge.com/Pages/ChangeAccount.aspx')
    for i in range(page_number):
                    print(i)
                    WebDriverWait(driver, wait).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="changeAccountDT_next"]')
                    )).click() 
                    time.sleep(3)
    return None

import time
import os
import shutil
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


all_account_numbers = []
failed_pdfs=[]
options = Options()
string = ''
# options.headless = True
wait = 60
for one_credential in credentials.iterrows():
    if one_credential[1]['LastUpdated']!=one_credential[1]['LastUpdated'] or today.date() != one_credential[1]['LastUpdated'].to_pydatetime().date():
        index_of_one_credentianls = one_credential[0]
        one_credential = one_credential[1]
        AccountOwnerID = one_credential['AccountOwnerID']

        main_file = os.getcwd() + '/pdfs/' + AccountOwnerID
        map(lambda x : shutil.rmtree(main_file +'/'+ x) ,[i for i in os.listdir(main_file)if 'temp' in i])
        temp_directory = main_file + '/temp_' +str(randint(100000000 ,999999999))+'/' 
        try:
            os.makedirs(temp_directory)
        except:
            pass

        download_path =  temp_directory

        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2) 
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/pdf")
        fp.set_preference("pdfjs.disabled",True)
        fp.set_preference("browser.download.dir", download_path)
        driver = webdriver.Firefox(options=options ,firefox_profile=fp)  
        driver.get("https://www.bge.com/Pages/default.aspx")

        WebDriverWait(driver, wait).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="s4-titlerow"]/header/div/button'))
        ).click()
        username = WebDriverWait(driver, wait).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="Username"]'))
        )
        password = driver.find_element_by_xpath('//*[@id="Password"]')
        username.send_keys(one_credential['Username'])
        password.send_keys(one_credential['Password'])
        click_sigin = driver.find_element_by_css_selector('ng-form.ng-dirty > div:nth-child(1) > exelon-decorator-simple:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(7)')
        click_sigin.click()

        page_number = 0
        while True:
            time.sleep(2)
            number_of_rows=len(driver.find_elements_by_xpath('//*[@id="changeAccountDT"]/tbody/tr'))
            for i in range(1,number_of_rows+1):
                try:
                    remove_overlay(driver)
                    accountNumber = WebDriverWait(driver, wait).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="changeAccountDT"]/tbody/tr[{i}]/td[1]'.format(i=i)))
                    ).text
                    if i == 1:
                        first_accountNumber = accountNumber

                    one_row = accountListing[(accountListing['AccountNumber']==accountNumber)&(accountListing['AccountOwnerID']==AccountOwnerID)]
                    print len(one_row)
                    if len(one_row) != 0:
                        LastDownloadBillDate = one_row['LastDownloadBillDate'].iloc[0]
                        BillCycleDays = one_row['BillCycleDays'].iloc[0]
                        print('in loop')
                        current_date = datetime.now().date()
                        if current_date <= (LastDownloadBillDate+timedelta(days=int(BillCycleDays))).date():
                            print ('skipping',accountNumber, AccountOwnerID)
                            continue


                    driver.find_element_by_xpath('//*[@id="changeAccountDT"]/tbody/tr[{i}]/td[7]/span/span/button/span'.format(i=i)).click()
                    remove_overlay(driver)       

                    WebDriverWait(driver, wait).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="excNavLeft"]/ul/li[1]/ul/li[4]/div'))
                    ).click()
                    remove_overlay(driver)

                    WebDriverWait(driver, wait).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="excNavLeft"]/ul/li[1]/ul/li[4]/div'))
                    ).click()
                    remove_overlay(driver)      

                    WebDriverWait(driver, wait).until(
                        EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/section[2]/div/div[3]/div/select/option[2]'))
                    ).click()
                    remove_overlay(driver)

                    driver.find_element_by_xpath('//*[@id="filter-apply"]').click()
                    remove_overlay(driver)
                    try:
    #                     date = WebDriverWait(driver, wait).until(
    #                         EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/section[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[1]'))
    #                     ).text
    #                     date = datetime.strptime(date , '%m/%d/%Y')
    #                     if len(accountListing[(accountListing['AccountNumber']==accountNumber) & (accountListing['LastDownloadBillDate']==date) & (accountListing['AccountOwnerID']==AccountOwnerID)])==0:
    #                         WebDriverWait(driver, wait).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/section[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[7]/a'))
    #                         ).click()
    #                         all_account_numbers.append((AccountOwnerID,accountNumber))
    #                         remove_overlay(driver)

                        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/section[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[7]/a'))
                                                ).click()

                    except:
                        pass


                    driver.get('https://secure.bge.com/Pages/ChangeAccount.aspx')
                    for i in range(page_number):
                        WebDriverWait(driver, wait).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="changeAccountDT_next"]')
                        )).click() 
                        time.sleep(1)

                    remove_overlay(driver)

                except Exception as e:
                    print (e)
                    failed_pdfs.append(string)
                    remove_overlay(driver)
                    check_login(driver, one_credential,wait, page_number)



            WebDriverWait(driver, wait).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="changeAccountDT_next"]')
                )).click()   
            time.sleep(2)
            accountNumber = WebDriverWait(driver, wait).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="changeAccountDT"]/tbody/tr[{i}]/td[1]'.format(i=1)))
                ).text  
            page_number+=1
            if first_accountNumber == accountNumber:
                break    

        #logout
        WebDriverWait(driver, wait).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.btn-accent:nth-child(3)'))
                ).click()


        downloaded_pdfs = os.listdir(download_path)

        for i in (downloaded_pdfs):
            try:
                while True:
                    if True in [True for s in downloaded_pdfs if 'part' in s]:
                        print('Sleeping for 2 seconds')
                        downloaded_pdfs = os.listdir(download_path)
                        time.sleep(2)
                    else:
                        break
                accountNumber = i.split('_')[0]
                date = datetime.strptime(i.split("_")[1].split('.')[0] , '%Y-%m-%d')

                if len(accountListing[(accountListing['AccountNumber']==accountNumber)&(accountListing['AccountOwnerID']==AccountOwnerID)])==0:
                    one_row=pd.DataFrame([[AccountOwnerID,accountNumber,date,28]], columns=list(accountListing.columns))
                    accountListing = accountListing.append(one_row)
                else:
                    accountListing.loc[(accountListing['AccountNumber']==accountNumber) &(accountListing['AccountOwnerID']==AccountOwnerID),['LastDownloadBillDate']] = date
            except:
                pass

        main_path = os.getcwd() + '/pdfs/' + AccountOwnerID

        for i in downloaded_pdfs:
            try:
                shutil.move(download_path+i ,main_path)
            except:
                pass

        shutil.rmtree(download_path)

        credentials.loc[index_of_one_credentianls,'LastUpdated'] = today
        
        accountListing.to_csv('AccountListing.csv', index=False)
        credentials.to_csv('Credentials.csv',index=False)
try:
    driver.quit()
except:
    pass
