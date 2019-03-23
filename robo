import os

import pandas as pd 
from datetime import datetime
from random import randint
import shutil

credentials = pd.read_csv('Credentials.csv')
accountListing = pd.read_csv('AccountListing.csv')

accountListing = accountListing.astype({"AccountOwnerID": str, "AccountNumber": str})
credentials =credentials.astype({"AccountOwnerID": str})


accountListing['LastDownloadBillDate'] = pd.to_datetime(accountListing['LastDownloadBillDate'])

accountListing['AccountNumber'] = accountListing['AccountNumber'].apply(lambda x: '0'+x if len(x)<10 else x )

def remove_overlay(driver):
    try:
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.acsInviteButton:nth-child(6)'))
        ).click()
    except:
        pass
def check_login(driver, one_credential,wait):
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
        
        click_sigin = driver.find_element_by_xpath('/html/body/form/div[10]/div[3]/div[1]/div/div/ng-form/div/exelon-decorator-simple[1]/div/div/div/button')
        click_sigin.click()

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
    one_credential = one_credential[1]
    AccountOwnerID = one_credential['AccountOwnerID']
    
    main_file = os.getcwd() + '/pdfs/' + AccountOwnerID
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
    
    click_sigin = driver.find_element_by_xpath('/html/body/form/div[10]/div[3]/div[1]/div/div/ng-form/div/exelon-decorator-simple[1]/div/div/div/button')
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

                driver.find_element_by_xpath('//*[@id="changeAccountDT"]/tbody/tr[{i}]/td[7]/span/span/button/span'.format(i=i)).click()
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
                    date = WebDriverWait(driver, wait).until(
                        EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/section[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[1]'))
                    ).text
                    date = datetime.strptime(date , '%m/%d/%Y')
                    if len(accountListing[(accountListing['AccountNumber']==accountNumber) & (accountListing['LastDownloadBillDate']==date) & (accountListing['AccountOwnerID']==AccountOwnerID)])==0:
                        WebDriverWait(driver, wait).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div/section[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[7]/a'))
                        ).click()
                        all_account_numbers.append((AccountOwnerID,accountNumber))
                        remove_overlay(driver)
                        
                except:
                    pass
                
                
                driver.get('https://secure.bge.com/Pages/ChangeAccount.aspx')
                for i in range(page_number):
                    print(i)
                    WebDriverWait(driver, wait).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="changeAccountDT_next"]')
                    )).click() 
                    time.sleep(2)

                remove_overlay(driver)
            
            except:
                failed_pdfs.append(string)
                check_login(driver, one_credential,wait)

                
            
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

    WebDriverWait(driver, wait).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/div[3]/div/header/div/button'))
            ).click()
    
    
    downloaded_pdfs = os.listdir(download_path)
    
    for i in (downloaded_pdfs):
        accountNumber = i.split('_')[0]
        date = datetime.strptime(i.split("_")[1].split('.')[0] , '%Y-%m-%d')
        AccountOwnerID = '1005698'

        if len(accountListing[(accountListing['AccountNumber']==accountNumber)&(accountListing['AccountOwnerID']==AccountOwnerID)])==0:
            one_row=pd.DataFrame([[AccountOwnerID,accountNumber,date,28]], columns=list(accountListing.columns))
            accountListing = accountListing.append(one_row)
        else:
            accountListing.loc[(accountListing['AccountNumber']==accountNumber) &(accountListing['AccountOwnerID']==AccountOwnerID),['LastDownloadBillDate']] = date


    main_path = os.getcwd() + '/pdfs/' + AccountOwnerID

    for i in downloaded_pdfs:
        shutil.move(download_path+i ,main_path)

    shutil.rmtree(download_path)

    os.getcwd() + '/pdfs/' + AccountOwnerID
    
accountListing.to_csv('AccountListing.csv')
