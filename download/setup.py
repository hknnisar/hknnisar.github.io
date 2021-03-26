# -*- coding: utf-8 -*-
"""
Created on Sat May 30 14:23:49 2020

@author: harshnisar
"""

import getpass
import os
import json
import zipfile
import requests
import py_compile
import time

task_summary = []

system = os.name
if system == 'posix':
    bs = '/'
elif system == 'nt':
    bs = '\\'


print('\nHello from harshnisar.com.\nWelcome to the setup process.\n'+'__'*40)
time.sleep(1)
#dependencies

print('\nChecking dependencies...')
time.sleep(1)
dependencies = ['kiteconnect','pandas','selenium','time','threading','urllib','requests','random','datetime','json','os','getpass','zipfile']
for depend in dependencies:
    try:
        __import__(depend)
    except:
        print('WARNING! %s not installed\nPlease run pip install %s\n'%(depend, depend))
        task_summary += ['Please run pip install %s'%(depend)]
print('DONE! Dependencies checked.\n')

#setup directory
print('Lets set everything up')
time.sleep(1)
print('This is your working directory %s'%(os.getcwd()))
time.sleep(1)
answer = input('Do you want to install in this directory? (Y/N) ')
if answer in ['n','N']:
    directory = input('Please give desired install directory: ')
else:
    directory = os.getcwd()
if not os.path.isdir(directory):
    os.mkdir(directory)
os.chdir(directory)
print('DONE! Will install in %s\n'%(directory))
time.sleep(2)

install_type = input('What do you want to install?\n (1) KiteBase\n (2) KiteBase & KiteRange\n (3) KiteBase & KiteSwing\n (4) All the above\nResponse: ')
while install_type not in ['1','2','3','4']:
    install_type = input('Not a valid option\nWhat do you want to install?\n (1) KiteBase\n (2) KiteBase & KiteRange\n (3) KiteBase & KiteSwing\n (4) All the above\nResponse: ')


filelist = {'1':['fno_calendar.pyc','Instance.pyc'],'2':['fno_calendar.pyc','Range.pyc','Instance.pyc'],'3':['fno_calendar.pyc','Swing.pyc','Container.pyc','Instance.pyc'],'4':['fno_calendar.pyc','Range.pyc','Instance.pyc','Swing.pyc','Container.pyc']}
for file in os.listdir():
        if file in filelist[install_type]:
            os.remove(directory+bs+file)

print('OKAY, Fetching latest modules...')
time.sleep(1)
url = 'https://hknnisar.github.io/download/KiteBase.zip'
r = requests.get(url, allow_redirects=True)
open('KiteBase.zip', 'wb').write(r.content)
if install_type == '2':
    url = 'https://hknnisar.github.io/download/KiteRange.zip'
    r = requests.get(url, allow_redirects=True)
    open('KiteRange.zip', 'wb').write(r.content)
elif install_type=='3':
    url = 'https://hknnisar.github.io/download/KiteSwing.zip'
    r = requests.get(url, allow_redirects=True)
    open('KiteSwing.zip', 'wb').write(r.content)
elif install_type=='4':
    url = 'https://hknnisar.github.io/download/KiteRange.zip'
    r = requests.get(url, allow_redirects=True)
    open('KiteRange.zip', 'wb').write(r.content)
    url = 'https://hknnisar.github.io/download/KiteSwing.zip'
    r = requests.get(url, allow_redirects=True)
    open('KiteSwing.zip', 'wb').write(r.content)

print('DONE! Successfully fetched latest modules\n')
time.sleep(1)

# #copy modules to pycache
# if not os.path.isdir(directory+'\\__pycache__'):
#     os.mkdir(directory+'\\__pycache__')

ziplist = {'1':['KiteBase.zip'],'2':['KiteBase.zip','KiteRange.zip'],'3':['KiteBase.zip','KiteSwing.zip'],'4':['KiteBase.zip','KiteRange.zip','KiteSwing.zip']}
zipfilelist = {'KiteBase.zip':['Instance.py','fno_calendar.py'],'KiteRange.zip':['Range.py'],'KiteSwing.zip':['Swing.py','Container.py']}

try:
    for thefile in ziplist[install_type]:
        with zipfile.ZipFile(directory+bs+thefile, 'r') as zip_ref:
            zip_ref.extractall(directory,pwd=bytes(getpass.getpass('Please give secret code to install '+thefile[:-4]+':'),'utf-8'))
            files = zipfilelist[thefile]
            py_compile.main(files)
            for file in files:
                os.remove(directory+bs+file) 
            pycache = '__pycache__'
            for file in os.listdir(directory+bs+pycache):
                os.rename(directory+bs+pycache+bs+file,directory+bs+file.split('.')[0]+'.pyc')
            zip_ref.close()
        os.remove(directory+bs+thefile)
        
    print('DONE! Modules successfully installed\n')
    time.sleep(1)

    #chromedriver
    if not os.path.isfile(os.getcwd()+bs+'chromedriver.exe' if system == 'nt' else os.getcwd()+bs+'chromedriver'):
        print('Please fetch a compatible chromedriver from https://chromedriver.chromium.org/downloads\n')
        time.sleep(1)
        task_summary += ['Please fetch a compatible chromedriver from https://chromedriver.chromium.org/downloads']
    else:
        print('Please ensure the chromedriver version is compatible with installed Chrome version\n')
        time.sleep(1)
        task_summary += ['Please ensure the chromedriver version is compatible with installed Chrome version']
    
    #credentials
    if os.path.isfile(directory+bs+'cred'):
        answer = input('Proceed with the credentials found on the system?: (Y/N) ')
        if answer in ['n','N']:
            os.remove(directory+bs+'cred')
    else:
        answer = 'n'
    if answer in ['N','n']:
        print("\nLets store and encrypt all credentials")
        time.sleep(1)
        api_key = input('Please give the api_key: ')
        api_secret = input('Please give the api_secret: ')
        client_id = input('Please give the Kite Client ID: ')
        client_pass = getpass.getpass('Please give the Kite Password: ')
        client_pin = getpass.getpass('Please give the Kite Pin: ')
        answer = input('Have you setup a Telegram Bot? (Y/N) ')
        if answer in ['Y','y']:
            bot_token = input('Please give the Telegram bot token: ')
            bot_chatID = input('Please give the Telegram bot chat ID: ')
            # cred = 
        with open(os.getcwd()+bs+'cred.dat','w') as json_file:
            json.dump({'api_key':api_key,'cliend_id':client_id,'client_pass':client_pass,'client_pin':client_pin,'api_secret':api_secret},json_file)
        
        os.system('openssl enc -in cred.dat -out cred -e -aes256 -k %s'%(getpass.getpass('Please set a password for encryption: ')))
        os.remove(directory+bs+'cred.dat')
    # task_summary += ['After importing Range, call Range.help() to get an introduction']
    # print('__'*40+'\nHere is a short introduction on how to use the Range module')
    # try:
    #     _temp = __import__('Range',fromlist=['Range'])
    #     getattr(_temp,'Range').help()
    # except:
    #     print('Please install all dependencies')
    if len(task_summary) > 0:
        print('\n'+'__'*40+'\nDONE! You are almost all set! Please complete the following tasks before running')
        time.sleep(1)
        for item in task_summary:
            print('-> '+item)
    else:
        print('\n'+'__'*40+'\nDONE! You are all set!')
        time.sleep(1)
except Exception as e:
    print('\nSetup FAILED\n')
    time.sleep(1)
    print(str(e))
    time.sleep(1)
    print('\nTo get a secret code please contact me on Telegram or Twitter @harshnisar or email me at harsh@harshnisar.com')
    time.sleep(1)
    for file in os.listdir():
        if file in ['fno_calendar.pyc','Range.pyc','Instance.pyc','fno_calendar.py','Range.py','Instance.py','Swing.pyc','Container.pyc','Swing,py','Container.py']:
            os.remove(directory+bs+file)
    for thefile in ziplist[install_type]:
        if os.path.isfile(directory+bs+thefile):
            os.remove(directory+bs+thefile)
