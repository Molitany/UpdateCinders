from platform import version
import sys
import os
import configparser
import requests
import zipfile
import config
from requests.api import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


cinderVersion = requests.get('https://api.nexusmods.com/v1/games/darksouls3/mods/310.json', 
    headers = {
        'accept': 'application/json', 
        'apikey':'SkxEVGpsczRQMUxMckZZbVo3MzBKenN5d2J5SHhYMHpWSXVjWElMbjdQRT0tLXdsR3FqYXBNZWExUXBHTXNkM2hGV2c9PQ==--36a55a13f3a90230a584db021155dc8e23c7969d'
    }
)

data = cinderVersion.json()
file = open('./version.txt', 'r')
fileContents = file.read()

if (data['version'] != fileContents):
    with open('./version.txt', 'w') as file:
        file.write(data['version'])
        file.close()
    CinderFiles = requests.get('https://api.nexusmods.com/v1/games/darksouls3/mods/310/files.json?category=main', 
        headers = {
            'accept': 'application/json', 
            'apikey':'SkxEVGpsczRQMUxMckZZbVo3MzBKenN5d2J5SHhYMHpWSXVjWElMbjdQRT0tLXdsR3FqYXBNZWExUXBHTXNkM2hGV2c9PQ==--36a55a13f3a90230a584db021155dc8e23c7969d'
        }
    )

    data = CinderFiles.json()
    ids = []
    for p in data['files']:
        if ('Model' not in p['name']):
            ids.append(p['id'][0])
    
    browser = webdriver.Firefox()
    browser.get('https://users.nexusmods.com/auth/continue?client_id=nexus&redirect_uri=https://www.nexusmods.com/oauth/callback&response_type=code&referrer=//www.nexusmods.com/darksouls3/mods/310?tab=files')
    login = browser.find_element_by_id('user_login')
    login.send_keys(config.username)
    password = browser.find_element_by_id('password')
    password.send_keys(config.password + Keys.RETURN)

    wait = WebDriverWait(browser, 10, poll_frequency=1)
    wait.until(lambda d:
        d.find_elements_by_css_selector("#mainContent")
    )
    for id in ids:
        browser.get('https://www.nexusmods.com/darksouls3/mods/310?tab=files&file_id=' + str(id))
        downloadBtn = wait.until(lambda d:
            d.find_element_by_css_selector("#slowDownloadButton")
        )
        downloadBtn.click()
        download = wait.until(lambda d: 
            d.find_element_by_css_selector("p > a")
        )
        href = download.get_attribute('href')
        local_filename = href.split('/')[-1].split('?')[0].replace('%20', ' ')
        browser.close()

        with requests.get(href, stream = True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                total = int(r.headers.get('content-length'))
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    downloaded += len(chunk)
                    f.write(chunk)
                    done = int(50*downloaded/total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                    sys.stdout.flush()
            sys.stdout.write('\n')

        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            zip_ref.extractall(config.unzip)
        
        configParser = configparser.ConfigParser()
        configParser.read(config.unzip + '/modengine.ini')
        configParser.set('online', 'blockNetworkAccess', "0")
        with open(config.unzip + '/modengine.ini', 'w') as f:
            configParser.write(f)
