f# -*- coding: utf-8 -*-
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
import subprocess

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

#runfiles from server?
run_from_server = input('Do you want to fetch runfiles from the server? (Y/N) ')
if run_from_server in ['Y','y']:
    run_from_server = True
else:
    run_from_server = False

filelist = {'1':['fno_calendar.pyc','Instance.pyc','run.sh'],'2':['fno_calendar.pyc','Range.pyc','Instance.pyc','run.sh'],'3':['fno_calendar.pyc','Swing.pyc','Container.pyc','Instance.pyc','run.sh'],'4':['fno_calendar.pyc','Range.pyc','Instance.pyc','Swing.pyc','Container.pyc','run.sh']}
if run_from_server:
    for file in os.listdir():
        if file in filelist[install_type]:
            os.remove(directory+bs+file)
else:
    for file in os.listdir():
        if (file in filelist[install_type]) & (file != 'run.sh'):
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
zipfilelist = {'KiteBase.zip':['Instance.py','fno_calendar.py','run.sh'],'KiteRange.zip':['Range.py'],'KiteSwing.zip':['Swing.py','Container.py']}

try:
    if not run_from_server:
        if os.path.isfile(directory+bs+'run.sh'):
            os.rename(directory+bs+'run.sh',directory+bs+'_run.sh') #rename existing runfile
    for thefile in ziplist[install_type]:
        with zipfile.ZipFile(directory+bs+thefile, 'r') as zip_ref:
            zip_ref.extractall(directory,pwd=bytes(getpass.getpass('Please give secret code to install '+thefile[:-4]+':'),'utf-8'))
            files = zipfilelist[thefile]
            if 'run.sh' in files:
                files.remove('run.sh')
            py_compile.main(files)
            for file in files:
                os.remove(directory+bs+file) 
            pycache = '__pycache__'
            for file in os.listdir(directory+bs+pycache):
                os.rename(directory+bs+pycache+bs+file,directory+bs+file.split('.')[0]+'.pyc')
            zip_ref.close()
        
        os.remove(directory+bs+thefile)
        
    if not run_from_server:
        os.remove(directory+bs+'run.sh')
        if os.path.isfile(directory+bs+'_run.sh'):
            os.rename(directory+bs+'_run.sh',directory+bs+'run.sh')
        
    print('DONE! Modules successfully installed\n')
    time.sleep(1)

    #chromedriver
    if not os.path.isfile(os.getcwd()+bs+'chromedriver.exe' if system == 'nt' else os.getcwd()+bs+'chromedriver'):
        if system == 'nt':
            print('Please fetch a compatible chromedriver from https://chromedriver.chromium.org/downloads\n')
            time.sleep(1)
            task_summary += ['Please fetch a compatible chromedriver from https://chromedriver.chromium.org/downloads']
        else:
            print('Fetching chromedriver from https://chromedriver.chromium.org/downloads')
            time.sleep(1)
        
            try:
                c2 = "google-chrome --version"
                p2 = subprocess.Popen(c2.split(), stdout=subprocess.PIPE)
                o2, e2= p2.communicate()
                ans2 = str(o2)
                version = int(ans2.split(' ')[2][:2])

                url = 'https://chromedriver.storage.googleapis.com/'
                response = requests.get(url)
                content=str(response.content)
                
                # version = '89'
                cdr_v = ''
                content = content.split('Contents')
                for item in content:
                    try:
                        interest = item.split('Key')[1].split('>')[1].split('<')[0].split('/')
                        if interest[1] == 'chromedriver_linux64.zip':
                            # print(interest[0])
                            if interest[0].split('.')[0] == str(version):
                                cdr_v = interest[0]
                    except IndexError:
                        pass
                cdr_url = 'https://chromedriver.storage.googleapis.com/%s/chromedriver_linux64.zip'%(cdr_v)
                r = requests.get(cdr_url, allow_redirects=True)
                open('chromedriver.zip', 'wb').write(r.content)
                with zipfile.ZipFile(directory+bs+'chromedriver.zip', 'r') as zip_ref:
                    zip_ref.extractall(directory)
                    zip_ref.close()
                os.chmod('chromedriver',0o777)
                os.remove(directory+bs+'chromedriver.zip')
                print('DONE! Compatible chromedriver downloaded\n')
            except:
                print('Please fetch a compatible chromedriver from https://chromedriver.chromium.org/downloads\n')
                time.sleep(1)
                task_summary += ['Please fetch a compatible chromedriver from https://chromedriver.chromium.org/downloads']
        
        
    else:
        if system == 'nt':
            print('Please ensure the chromedriver version is compatible with installed Chrome version\n')
            time.sleep(1)
            task_summary += ['Please ensure the chromedriver version is compatible with installed Chrome version']
        else:
            try:
                c1 = "./chromedriver -version"
                c2 = "google-chrome --version"
                p1 = subprocess.Popen(c1.split(), stdout=subprocess.PIPE)
                o1, e1= p1.communicate()
                p2 = subprocess.Popen(c2.split(), stdout=subprocess.PIPE)
                o2, e2= p2.communicate()
                ans1 = str(o1)
                ans2 = str(o2)
                ans1 = int(ans1.split(' ')[1][:2])
                ans2 = int(ans2.split(' ')[2][:2])
                if ans1 == ans2:
                    print('DONE! chromedriver vesion matched with installed Google Chrome version, v%d\n'%(ans1))
                else:
                    print('NOTE: chromedriver v%d installed, while Google Chrome v%d installed, download %d chromedriver\n'%(ans1,ans2,ans2))
                    time.sleep(1)
                    task_summary += ['Please download chromedriver v%d'%(ans2)]
            except:
                print('Please ensure the chromedriver version is compatible with installed Chrome version\n')
                time.sleep(1)
                task_summary += ['Please ensure the chromedriver version is compatible with installed Chrome version']
    
    #credentials
    if os.path.isfile(directory+bs+'cred'):
        answer = input('Proceed with the credentials found on the system?: (Y/N) ')
        #if you want to change password
        # re_encrypt = input('Re-encrypt? ')
        # if re_encrypt in ['Y','y']:
        #     os.system('openssl enc -in cred -out cred.dat -d -pbkdf2 -k %s'%(getpass.getpass('Password: ')))
        #     os.remove(directory+bs+'cred')
        #     os.system('openssl enc -aes-256-cbc -pbkdf2 -iter 20000 -in cred.dat -out cred -k %s'%(getpass.getpass('Password: ')))
        #     os.remove(directory+bs+'cred.dat')
        if answer in ['n','N']:
            os.remove(directory+bs+'cred')
        else:
            password = getpass.getpass("Please provide credentials password to fetch Client ID: ")
            os.system('openssl enc -d -aes-256-cbc -pbkdf2 -iter 20000 -in cred -out cred.dat -k %s'%(password))
            with open(directory+bs+'cred.dat') as json_file: 
                cred = json.load(json_file) 
            os.remove('cred.dat')
            client_id = cred['cliend_id']
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
        
        password = getpass.getpass('Please set a password for encryption of credentials: ')
        os.system('openssl enc -aes-256-cbc -pbkdf2 -iter 20000 -in cred.dat -out cred -k  %s'%(password))
        os.remove(directory+bs+'cred.dat')
    # task_summary += ['After importing Range, call Range.help() to get an introduction']
    # print('__'*40+'\nHere is a short introduction on how to use the Range module')
    # try:
    #     _temp = __import__('Range',fromlist=['Range'])
    #     getattr(_temp,'Range').help()
    # except:
    #     print('Please install all dependencies')
    if run_from_server:
        with open('run.sh','r') as f:
            content = f.read()
        f.close()
        content = content.replace('__client_id__',client_id)
        content = content.replace('__password__',password)
        with open('run.sh','w') as f:
            f.write(content)
        f.close()
        os.chmod('run.sh',0o777)

    
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
        if file in ['fno_calendar.pyc','Range.pyc','Instance.pyc','fno_calendar.py','Range.py','Instance.py','Swing.pyc','Container.pyc','Swing,py','Container.py','run.sh']:
            os.remove(directory+bs+file)
    for thefile in ziplist[install_type]:
        if os.path.isfile(directory+bs+thefile):
            os.remove(directory+bs+thefile)
    if not run_from_server:
        if os.path.isfile(directory+bs+'_run.sh'):
            os.rename(directory+bs+'_run.sh',directory+bs+'run.sh')

