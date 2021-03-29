import requests
import config
from bs4 import BeautifulSoup
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
file = open('version.txt', 'r')
fileContents = file.read()

if (data['version'] != fileContents):
    CinderFiles = requests.get('https://api.nexusmods.com/v1/games/darksouls3/mods/310/files.json?category=main', 
        headers = {
            'accept': 'application/json', 
            'apikey':'SkxEVGpsczRQMUxMckZZbVo3MzBKenN5d2J5SHhYMHpWSXVjWElMbjdQRT0tLXdsR3FqYXBNZWExUXBHTXNkM2hGV2c9PQ==--36a55a13f3a90230a584db021155dc8e23c7969d'
        }
    )
    data = CinderFiles.json()
    ids = []
    for p in data['files']:
        ids.append(p['id'][0])
    
    browser = webdriver.Firefox()
    browser.get('https://users.nexusmods.com/auth/continue?client_id=nexus&redirect_uri=https://www.nexusmods.com/oauth/callback&response_type=code&referrer=//www.nexusmods.com/darksouls3/mods/310?tab=files')
    login = browser.find_element_by_id('user_login')
    login.send_keys(config.username)
    password = browser.find_element_by_id('password')
    password.send_keys(config.password + Keys.RETURN)

    WebDriverWait(browser).until(lambda d:
        d.find_elements_by_css_selector("#mainContent")
    )
    for id in ids:
        browser.get('https://www.nexusmods.com/darksouls3/mods/310?tab=files&file_id=' + str(id))
        
    
    # cinderFiles = requests.get('https://www.nexusmods.com/darksouls3/mods/310?tab=files&file_id=' + str(ids[0]))
    # soup = BeautifulSoup(cinderFiles.content, 'html.parser')
    # elem = soup.find('div', class_='container')
    # print(elem.prettify())

    # authenticity_token=qIYGWJX6pfjTES3kCX9GhVqKSMSdTb8KoeqZ%2FpyKlpWQ6v0AFroqagO%2BgI%2FQizOD3I4fcpkJyUmMGEVFZ3MKQw%3D%3D&user%5Blogin%5D=thorzx&user%5Bpassword%5D=Thorxz111111&commit=Log+in