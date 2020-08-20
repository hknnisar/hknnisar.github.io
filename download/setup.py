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

task_summary = []

system = os.name
if system == 'posix':
    bs = '/'
elif system == 'nt':
    bs = '\\'

#dependencies
print('Checking dependencies...')
dependencies = ['kiteconnect','pandas','selenium','time','threading','urllib','requests','random','datetime','json','os','getpass','zipfile']
for depend in dependencies:
    try:
        __import__(depend)
    except:
        print('WARNING! %s not installed\nPlease run pip install %s'%(depend, depend))
        task_summary += ['Please run pip install %s'%(depend)]
print('Dependencies checked.')

#setup directory
print('Lets set everything up')
print('This is your working directory %s'%(os.getcwd()))
answer = input('Do you want to install in this directory? (Y/N) ')
if answer in ['n','N']:
    directory = input('Please give desired install directory: ')
else:
    directory = os.getcwd()
if not os.path.isdir(directory):
    os.mkdir(directory)
os.chdir(directory)

for file in os.listdir():
        if file in ['fno_calendar.pyc','Range.pyc','Instance.pyc']:
            os.remove(directory+bs+file)

print('Fetching latest KiteRange...')
url = 'https://hknnisar.github.io/download/KiteRange.zip'
r = requests.get(url, allow_redirects=True)
open('KiteRange.zip', 'wb').write(r.content)
print('Proceeding installation in %s'%(os.getcwd()))

# #copy modules to pycache
# if not os.path.isdir(directory+'\\__pycache__'):
#     os.mkdir(directory+'\\__pycache__')


try:
    with zipfile.ZipFile(directory+bs+'KiteRange.zip', 'r') as zip_ref:
        zip_ref.extractall(directory,pwd=bytes(getpass.getpass('Please give secret code install KiteRange: '),'utf-8'))
        files = ['Instance.py','fno_calendar.py','Range.py']
        py_compile.main(files)
        for file in files:
            os.remove(directory+bs+file) 
        pycache = '__pycache__'
        for file in os.listdir(directory+bs+pycache):
            os.rename(directory+bs+pycache+bs+file,directory+bs+file.split('.')[0]+'.pyc')
        zip_ref.close()
    os.remove(directory+bs+'KiteRange.zip')

    #chromedriver
    if not os.path.isfile(os.getcwd()+bs+'chromedriver.exe' if system == 'nt' else os.getcwd()+bs+'chromedriver'):
        print('Please fetch a compatible chromedriver from https://chromedriver.chromium.org/downloads')
        task_summary += ['Please fetch a compatible chromedriver from https://chromedriver.chromium.org/downloads']
    else:
        print('Please ensure the chromedriver version is compatible with installed Chrome version')
        task_summary += ['Please ensure the chromedriver version is compatible with installed Chrome version']
    
    #credentials
    if os.path.isfile(directory+bs+'cred'):
        answer = input('Proceed with the credentials found on the system?: (Y/N) ')
        if answer in ['n','N']:
            os.remove(directory+bs+'cred')
    else:
        answer = 'n'
    if answer in ['N','n']:
        print("Lets store and encrypt all credentials")
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
    task_summary += ['After importing Range, call Range.help() to get an introduction']
    print('__'*40+'\nHere is a short introduction on how to use the Range module')
    try:
        _temp = __import__('Range',fromlist=['Range'])
        getattr(_temp,'Range').help()
    except:
        print('Please install all dependencies')
    if len(task_summary) > 0:
        print('__'*40+'\n\nPlease complete the following tasks before running')
        for item in task_summary:
            print('-> '+item)
except Exception as e:
    print(str(e))
    print('To get a secret code please contact me on Telegram or Twitter @harshnisar or email me at harsh@harshnisar.com')
    for file in os.listdir():
        if file in ['fno_calendar.pyc','Range.pyc','Instance.pyc','fno_calendar.py','Range.py','Instance.py']:
            os.remove(directory+bs+file)
    if os.path.isfile(directory+bs+'KiteRange.zip'):
        os.remove(directory+bs+'KiteRange.zip')
