import os
from selenium import webdriver
import numpy as np
import json
from os import walk
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
import random
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from Google import Create_Service
import requests

CLIENT_SECRET_FILE = 'POVEZAVA DO AKREDITACIJE'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

driver.get("https://www.patreon.com/login")


time.sleep(35)
username = driver.find_element_by_id('email')
username.send_keys("UPORABNIŠKO IME")
time.sleep(3)

password = driver.find_element_by_id('password')
password.send_keys("GESLO")
time.sleep(3)

wait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="renderPageContentWrapper"]/div[1]/div/div/div[1]/div/div[1]/form/div[5]/button'))).click()
print("-- LOGIN BUTTON ")
time.sleep(10)


def get_google_drive_link(filename):
    page_token = None
    query = "mimeType='application/vnd.google-apps.folder' and name='"+ filename + "'"
    file_ids = ""
    print(query)
    while True:
        response = service.files().list(q=query,
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            file_ids = file.get('id')
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    if file_ids is not None:
        file_id = file_ids
        print('Var is not null')

        request_body = {
            'role': 'reader',
            'type': 'anyone'
        }

        response_permission = service.permissions().create(
            fileId=file_id,
            body=request_body
        ).execute()

        print(response_permission)

        # Print Sharing URL
        response_share_link = service.files().get(
            fileId=file_id,
            fields='webViewLink'
        ).execute()

        parameters = {"url": response_share_link["webViewLink"]}
        headers_dict = {
                        'content-type': 'application/x-www-form-urlencoded',
                        'x-rapidapi-host': 'url-shortener-service.p.rapidapi.com',
                        'x-rapidapi-key': 'ee94345ecamshcc45f2ef587e60ep1d4f6bjsn67c823e0d0a0'
                      }

        response = requests.post("https://url-shortener-service.p.rapidapi.com/shorten", data=parameters, headers=headers_dict)

        print(response.json())
        test = response.json()
        print("response STRING URL TEST")
        print(test["result_url"])

        print(response_share_link["webViewLink"])

        return test["result_url"]
    else:
        return ""


def get_immediate_subdirectories_wpath(a_dir):
    c = [f.path for f in os.scandir(a_dir) if f.is_dir()]
    return c


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_list_of_file_names(dir_with_path):
    f = []
    file_name = ""
    for (dirpath, dirnames, filenames) in walk(dir_with_path):
        f.extend(filenames)
        break
    for name in f:
        #if long version and mp3
        #("(long version)" in name.lower() or "(long edit)" in name.lower())
        print("name v GET LIST OF FILE NAMES")
        print(name)
        if ("(long version)" in name.lower() or "(long edit)" in name.lower() or "long edit" in name.lower() or "long version" in name.lower() or "full version" in name.lower() or "(extended version)" in name.lower() or "(main version)" in name.lower()) and (".mp3" in name or ".wav" in name):
            print("Found!")
            file_name = dir_with_path + "\\" + name
            break
    return file_name

def get_BPM(dir_with_path):
    f = []
    file_name = ""
    for (dirpath, dirnames, filenames) in walk(dir_with_path):
        f.extend(filenames)
        break
    for name in f:
        if ".txt" in name.lower():
            print("Found BPM!")
            file_name = name
            break
    return file_name


def get_file_name_wo_path(dir_with_path):
    f = []
    file_name = ""
    for (dirpath, dirnames, filenames) in walk(dir_with_path):
        f.extend(filenames)
        break
    for name in f:
        #if long version and mp3
        #("(long version)" in name.lower() or "(long edit)" in name.lower())
        if ("(long version)" in name.lower() or "(long edit)" in name.lower() or "(extended version)" in name.lower() or "(main version)" in name.lower() or "full version" in name.lower())  and (".mp3" in name or ".wav" in name):
            file_name = name
            break
    return file_name


def get_full_title(file_name, bpm_full):
    bpm = bpm_full.split(".",1)[0]
    print(bpm)
    if "future bass" in file_name.lower() or "dubstep" in file_name.lower():
        future_bass_title = "[FUTURE BASS TRACK " + bpm + " BPM] " + file_name
        return future_bass_title
    elif "technology" in file_name.lower() or "abstract" in file_name.lower() or "future" in file_name.lower():
        technology_title = "[ABSTRACT TRACK " + bpm + " BPM] " + file_name
        return technology_title
    elif "techno" in file_name.lower():
        techno_title = "[TECHNO TRACK " + bpm + " BPM] " + file_name
        return techno_title
    elif "house" in file_name.lower():
        house_title = "[HOUSE TRACK " + bpm + " BPM] " + file_name
        return house_title
    elif "electro" in file_name.lower() or "cyberpunk" in file_name.lower():
        cyber_title = "[CYBERPUNK TRACK " + bpm + " BPM] " + file_name
        return cyber_title
    elif "synthwave" in file_name.lower() or "80s" in file_name.lower():
        synth_title = "[SYNTHWAVE TRACK " + bpm + " BPM] " + file_name
        return synth_title
    elif "pop" in file_name.lower() or ("upbeat dance") in file_name.lower() or ("dance upbeat") in file_name.lower() or "dance" in file_name.lower() or "party" in file_name.lower():
        pop_title = "[POP TRACK " + bpm + " BPM] " + file_name
        return pop_title
    elif "hip hop" in file_name.lower() or "hip-hop" in file_name.lower() or "hip" in file_name.lower() or "hop" in file_name.lower() or "lofi" in file_name.lower() or "lo fi" in file_name.lower() or "lo-fi" in file_name.lower() or "hiphop" in file_name.lower() or "trap" in file_name.lower() or "vlog" in file_name.lower():
        hip_title = "[HIP HOP TRACK " + bpm + " BPM] " + file_name
        return hip_title
    elif "percussion" in file_name.lower() or "stomp" in file_name.lower() or "drums" in file_name.lower():
        percussion_title = "[PERCUSSION TRACK " + bpm + " BPM] " + file_name
        return percussion_title
    elif "corporate" in file_name.lower() or ("corporate" and "ambient") in file_name.lower():
        corporate_title = "[CORPORATE TRACK " + bpm + " BPM] " + file_name
        return corporate_title
    elif "ambient" in file_name.lower() or "documentaries" in file_name.lower() or "documentary" in file_name.lower():
        ambient_title = "[AMBIENT TRACK " + bpm + " BPM] " + file_name
        return ambient_title
    elif "funk" in file_name.lower() or "funky" in file_name.lower() or "groove" in file_name.lower() or "jazz" in file_name.lower() or "groovy" in file_name.lower():
        funk_title = "[FUNK TRACK " + bpm + " BPM] " + file_name
        return funk_title
    elif "rock" in file_name.lower() or "indie rock" in file_name.lower():
        rock_title = "[ROCK TRACK " + bpm + " BPM] " + file_name
        return rock_title
    elif "cinematic" in file_name.lower() or "epic" in file_name.lower() or "trailer" in file_name.lower():
        cinematic_title = "[CINEMATIC TRACK " + bpm + " BPM] " + file_name
        return cinematic_title
    else:
        edit_title = "[!!NEEDS EDITS!! BPM] " + file_name
        return edit_title


def get_title(dirname, bpm):
    if "(u)" in dirname:
        title = dirname.replace('(u)', '')
        return get_full_title(title, bpm)
    elif "(U)" in dirname:
        title = dirname.replace('(U)', '')
        return get_full_title(title, bpm)
    elif "(u o)" in dirname:
        title = dirname.replace('(u o)', '')
        return get_full_title(title, bpm)
    elif "(U O)" in dirname:
        title = dirname.replace('(U O)', '')
        return get_full_title(title, bpm)
    elif "(u a)" in dirname:
        title = dirname.replace('(u a)', '')
        return get_full_title(title, bpm)
    elif "(U A)" in dirname:
        title = dirname.replace('(U A)', '')
        return get_full_title(title, bpm)
    elif "(u y)" in dirname.lower():
        title = dirname.replace('(U Y)', '')
        return get_full_title(title, bpm)
    elif "(u y)" in dirname.lower():
        title = dirname.replace('(u y)', '')
        return get_full_title(title, bpm)
    elif "(u y)" in dirname.lower():
        title = dirname.replace('(u Y)', '')
        return get_full_title(title, bpm)
    else:
        return get_full_title(dirname, bpm)


def get_description(file_name):
    drive_link = get_google_drive_link(file_name)
    if "future bass" in file_name.lower() or "dubstep" in file_name.lower():
        return """Future Bass Background Music For Videos.
Download: """ + drive_link + """
Vibe: cool, upbeat, travel, chill.
Suitable for: youtube videos, vlogs, ads, commercials, presentation videos, technology videos and more!"""
    elif "technology" in file_name.lower() or "abstract" in file_name.lower() or "future" in file_name.lower():
        return """Abstract Technology Music For Videos.
Download: """ + drive_link + """
Vibe: ambient, inspiring, background, technology
Suitable for: technology videos, ads, commercials, presentation videos, car videos and more!"""
    elif "electro" in file_name.lower() or "cyberpunk" in file_name.lower() or "techno" in file_name.lower():
        return """EDM Music For Videos.
Download: """ + drive_link + """
Vibe: cool, upbeat, travel, chill, gaming, action.
Suitable for: youtube videos, vlogs, ads, commercials, presentation videos, technology videos, car videos and more!"""
    elif "house" in file_name.lower():
        return """House Music For Videos.
Download: """ + drive_link + """
Vibe: cool, fashion, chill, luxury.
Suitable for: youtube videos, vlogs, ads, commercials, presentation videos, technology videos, fashion videos and more!"""
    elif "synthwave" in file_name.lower() or "80s" in file_name.lower():
        return """Synthwave Background Music For Videos. 
Download: """ + drive_link + """
Vibe: retro, upbeat, cool, driving, city.
Suitable for: ads, commercials, car videos, technology videos, youtube videos and more!"""
    elif "pop" in file_name.lower() or ("upbeat dance") in file_name.lower() or ("dance upbeat") in file_name.lower() or "dance" in file_name.lower() or "party" in file_name.lower():
        return """Pop Background Music For Videos. 
Download: """ + drive_link + """
Vibe: happy, summer, pop, upbeat.
Suitable for: summer videos, vlog videos, commercials, ads, sport videos, travel videos and more!"""
    elif "lofi" in file_name.lower() or "lo-fi" in file_name.lower() or "lo fi" in file_name.lower():
        return """Lofi Background Music For Videos. 
Download: """ + drive_link + """
Vibe: lifestyle, vlog, upbeat.
Suitable for: vlogs, commercials, ads, tiktok, cooking videos, youtube videos and more!"""
    elif "hip hop" in file_name.lower() or "hip-hop" in file_name.lower() or "hip" in file_name.lower() or "hop" in file_name.lower() or "hiphop" in file_name.lower() or "trap" in file_name.lower() or "vlog" in file_name.lower():
        return """Hip Hop Background Music For Videos. 
Download: """ + drive_link + """
Vibe: lifestyle, vlog, upbeat.
Suitable for: vlogs, commercials, ads, tiktok, cooking videos, youtube videos and more!"""
    elif "percussion" in file_name.lower() or "stomp" in file_name.lower() or "drums" in file_name.lower():
        return """Percussion Background Music For Videos. 
Download: """ + drive_link + """
Vibe:  upbeat, catchy, cool.
Suitable for: ads, commercials, youtube videos, presentation videos, sports videos, technology videos, trailers and more!"""
    elif "corporate" in file_name.lower() or ("corporate" and "ambient") in file_name.lower():
        return """Corporate Uplifting Background Music For Videos. 
Download: """ + drive_link + """
Vibe: corporate, background, upbeat, uplifting.
Suitable for: news, ads, commercials, background, youtube videos, presentation videos and more!"""
    elif "ambient" in file_name.lower() or "documentaries" in file_name.lower() or "documentary" in file_name.lower():
        return """Ambient Uplifting Background Music For Videos. 
Download: """ + drive_link + """
Vibe: ambient, corporate, background, upbeat, uplifting.
Suitable for: tech, news, ads, commercials, background, youtube videos, presentation videos and more!"""
    elif "funk" in file_name.lower() or "funky" in file_name.lower() or "groove" in file_name.lower() or "jazz" in file_name.lower() or "groovy" in file_name.lower():
        return """Funk Background Music For Videos. 
Download: """ + drive_link + """
Vibe: funky, upbeat, happy, groovy.
Suitable for: commercials, ads, tiktok, cooking videos, youtube videos and more!"""
    elif "rock" in file_name.lower() or "indie rock" in file_name.lower():
        return """Rock Background Music For Videos.
Download: """ + drive_link + """
Vibe:  uplifting, lifestyle, action, trailer.
Suitable for: news, ads, commercials, background, youtube videos, sports videos, extreme videos, trailers and more!"""
    elif "cinematic" in file_name.lower() or "epic" in file_name.lower() or "trailer" in file_name.lower():
        return """Cinematic Background Music For Videos.
Download: """ + drive_link + """
Vibe:  cinematic, epic, action, trailer, uplifting.
Suitable for: news, ads, commercials, background, youtube videos, sports videos, extreme videos, trailers and more!"""
    else:
        return """Background Music For Videos.
Download: """ + drive_link + """
Vibe:  uplifting, upbeat, , .
Suitable for: ads, commercials, background, youtube videos, sports videos and more!"""


def get_picture_path(file_name):
    if "technology" in file_name.lower() or "abstract" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\7.jpg"
    elif "future bass" in file_name.lower() or "electro" in file_name.lower() or "synthwave" in file_name.lower() or "cyberpunk" in file_name.lower() or "house" in file_name.lower() or "dubstep" in file_name.lower() or "techno" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\1.jpg"
    elif "pop" in file_name.lower() or ("upbeat dance") in file_name.lower() or ("dance upbeat") in file_name.lower() or "dance" in file_name.lower() or "party" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\3.jpg"
    elif "hip hop" in file_name.lower() or "hip-hop" in file_name.lower() or "hip" in file_name.lower() or "hop" in file_name.lower() or "lo fi" in file_name.lower() or "lofi" in file_name.lower() or "lo-fi" in file_name.lower() or "hiphop" in file_name.lower() or "trap" in file_name.lower() or "vlog" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\2.jpg"
    elif "percussion" in file_name.lower() or "stomp" in file_name.lower() or "drums" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\4.jpg"
    elif "corporate" in file_name.lower() or ("corporate" and "ambient") in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\5.jpg"
    elif "ambient" in file_name.lower() or "documentaries" in file_name.lower() or "documentary" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\6.jpg"
    elif "funk" in file_name.lower() or "funky" in file_name.lower() or "groove" in file_name.lower() or "jazz" in file_name.lower() or "groovy" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\8.jpg"
    elif "rock" in file_name.lower() or "indie rock" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\9.jpg"
    elif "cinematic" in file_name.lower() or "epic" in file_name.lower() or "trailer" in file_name.lower():
        return "G:\\Ony Music Webstore\\Ony Products\\On Products New\\14.jpg"
    else:
        return 0


def get_tags(i, file_name):
    if "future bass" in file_name.lower() or "dubstep" in file_name.lower():
        future_bass = ["future bass", "ad", "adventure", "cool", "fashion", "travel", "upbeat", "youtube", "vlog", "high energy"]
        return future_bass[i]
    elif "technology" in file_name.lower() or "abstract" in file_name.lower() or "future" in file_name.lower():
        technology = ["abstract", "futuristic", "technology", "inspiring", "modern", "ambient", "medium energy"]
        return technology[i]
    elif "electro" in file_name.lower() or "cyberpunk" in file_name.lower() or "techno" in file_name.lower():
        electro = ["techno", "action", "ad", "aggressive", "modern", "sport", "technology", "videogame", "youtube", "high energy"]
        return electro[i]
    elif "synthwave" in file_name.lower() or "80s" in file_name.lower():
        synthwave = ["synthwave", "ad", "80s", "cool", "retro", "youtube", "medium energy"]
        return synthwave[i]
    elif "house" in file_name.lower():
        house = ["house", "ad", "fashion", "cool", "vlog", "youtube", "medium energy"]
        return house[i]
    elif "pop" in file_name.lower() or ("upbeat dance") in file_name.lower() or ("dance upbeat") in file_name.lower() or "dance" in file_name.lower() or "party" in file_name.lower():
        pop = ["pop", "adventure", "summer", "travel", "upbeat", "vlog", "youtube", "medium energy"]
        return pop[i]
    elif "lofi" in file_name.lower() or "lofi" in file_name.lower() or "lo-fi" in file_name.lower() or "lo fi" in file_name.lower():
        lofi = ["lofi", "hip hop", "chill", "ad", "vlog", "youtube", "upbeat", "low energy"]
        return lofi[i]
    elif "hip hop" in file_name.lower() or "hip-hop" in file_name.lower() or "hip" in file_name.lower() or "hop" in file_name.lower() or "hiphop" in file_name.lower() or "trap" in file_name.lower() or "vlog" in file_name.lower():
        hip_hop = ["hip hop", "ad", "chill", "vlog", "youtube", "upbeat", "medium energy"]
        return hip_hop[i]
    elif "percussion" in file_name.lower() or "stomp" in file_name.lower() or "drums" in file_name.lower():
        percussion = ["percussion", "ad", "typography", "upbeat", "cool", "high energy"]
        return percussion[i]
    elif "corporate" in file_name.lower() or ("corporate" and "ambient") in file_name.lower():
        corporate = ["corporate", "ad", "background", "inspiring", "ambient", "upbeat", "presentation", "youtube", "medium energy"]
        return corporate[i]
    elif "ambient" in file_name.lower() or "documentaries" in file_name.lower() or "documentary" in file_name.lower():
        ambient = ["ambient", "background", "calm", "corporate", "presentation", "technology", "youtube", "low energy"]
        return ambient[i]
    elif "funk" in file_name.lower() or "funky" in file_name.lower() or "groove" in file_name.lower() or "jazz" in file_name.lower() or "groovy" in file_name.lower():
        funk = ["funk", "fashion", "fun", "upbeat", "quirky", "ad", "youtube", "medium energy"]
        return funk[i]
    elif "rock" in file_name.lower() or "indie rock" in file_name.lower():
        rock = ["rock", "indie", "fun", "cool", "ad", "youtube", "medium energy"]
        return rock[i]
    elif "cinematic" in file_name.lower() or "epic" in file_name.lower() or "trailer" in file_name.lower():
        cinematic = ["cinematic", "epic", "ad", "adventure", "inspiring", "presentation", "medium energy"]
        return cinematic[i]
    else:
        notag = ["ad"]
        return notag[i]


def get_tag_len(file_name):
    if "future bass" in file_name.lower() or "dubstep" in file_name.lower():
        future_bass = ["future bass", "ad", "adventure", "cool", "fashion", "travel", "upbeat", "youtube", "vlog", "high energy"]
        return len(future_bass)
    elif "technology" in file_name.lower() or "abstract" in file_name.lower() or "future" in file_name.lower():
        technology = ["abstract", "futuristic", "technology", "inspiring", "modern", "ambient", "medium energy"]
        return len(technology)
    elif "electro" in file_name.lower() or "cyberpunk" in file_name.lower() or "techno" in file_name.lower():
        electro = ["techno", "action", "ad", "aggressive", "modern", "sport", "technology", "videogame", "youtube", "high energy"]
        return len(electro)
    elif "house" in file_name.lower():
        house = ["house", "ad", "fashion", "cool", "vlog", "youtube", "medium energy"]
        return len(house)
    elif "synthwave" in file_name.lower() or "80s" in file_name.lower():
        synthwave = ["synthwave", "ad", "80s", "cool", "retro", "youtube", "medium energy"]
        return len(synthwave)
    elif "pop" in file_name.lower() or ("upbeat dance") in file_name.lower() or ("dance upbeat") in file_name.lower() or "dance" in file_name.lower() or "party" in file_name.lower():
        pop = ["pop", "adventure", "summer", "travel", "upbeat", "vlog", "youtube", "medium energy"]
        return len(pop)
    elif "lofi" in file_name.lower() or "lofi" in file_name.lower() or "lo-fi" in file_name.lower() or "lo fi" in file_name.lower():
        lofi = ["lofi", "hip hop", "chill", "ad", "vlog", "youtube", "upbeat", "low energy"]
        return len(lofi)
    elif "hip hop" in file_name.lower() or "hip-hop" in file_name.lower() or "hip" in file_name.lower() or "hop" in file_name.lower() or "hiphop" in file_name.lower() or "trap" in file_name.lower() or "vlog" in file_name.lower():
        hip_hop = ["hip hop", "ad", "chill", "vlog", "youtube", "upbeat", "medium energy"]
        return len(hip_hop)
    elif "percussion" in file_name.lower() or "stomp" in file_name.lower() or "drums" in file_name.lower():
        percussion = ["percussion", "ad", "typography", "upbeat", "cool", "high energy"]
        return len(percussion)
    elif "corporate" in file_name.lower() or ("corporate" and "ambient") in file_name.lower():
        corporate = ["corporate", "ad", "background", "inspiring", "ambient", "upbeat", "presentation", "youtube", "medium energy"]
        return len(corporate)
    elif "ambient" in file_name.lower() or "documentaries" in file_name.lower() or "documentary" in file_name.lower():
        ambient = ["ambient", "background", "calm", "corporate", "presentation", "technology", "youtube", "low energy"]
        return len(ambient)
    elif "funk" in file_name.lower() or "funky" in file_name.lower() or "groove" in file_name.lower() or "jazz" in file_name.lower() or "groovy" in file_name.lower():
        funk = ["funk", "fashion", "fun", "upbeat", "quirky", "ad", "youtube", "medium energy"]
        return len(funk)
    elif "rock" in file_name.lower() or "indie rock" in file_name.lower():
        rock = ["rock", "indie", "fun", "cool", "ad", "youtube", "medium energy"]
        return len(rock)
    elif "cinematic" in file_name.lower() or "epic" in file_name.lower() or "trailer" in file_name.lower():
        cinematic = ["cinematic", "epic", "ad", "adventure", "inspiring", "presentation", "medium energy"]
        return len(cinematic)
    else:
        notag = ["ad"]
        return len(notag)


dir_with_path = get_immediate_subdirectories_wpath("X:\\No_Copyright\\Music\\Patreon Upload")
print(dir_with_path)

dir_names = get_immediate_subdirectories("X:\\No_Copyright\\Music\\Patreon Upload")
print("dir_names")
print(dir_names)
to_be_edited = []


for n in range(0, len(dir_with_path)):
    time.sleep(10)
    print(get_file_name_wo_path(dir_with_path[n]))

    if get_picture_path(get_file_name_wo_path(dir_with_path[n])) == 0:
        to_be_edited.append(get_file_name_wo_path(dir_with_path[n]))
        print(to_be_edited)
        continue

    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="LeftNav-LinkGroupsRow-Group-Button-Posts"]'))).click()
    time.sleep(10)
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="LeftNav-LinkGroupsRow-Group-Posts"]/li[1]/a'))).click()
    time.sleep(10)
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="post_type_button_audio_embed"]'))).click()
    print(get_file_name_wo_path(dir_with_path[n]))
    print(get_list_of_file_names(dir_with_path[n]))
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[2]/input').send_keys(get_picture_path(get_file_name_wo_path(dir_with_path[n])))
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/button/div[2]/input').send_keys(get_list_of_file_names(dir_with_path[n]))
    time.sleep(10)
    title = driver.find_element_by_id('post-title')
    title.send_keys(get_title(dir_names[n], get_BPM(dir_with_path[n])))
    time.sleep(10)
    desc = driver.find_element_by_xpath('//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[5]/div/div[2]/div/div/div[2]/div/div/div/div')

    desc.send_keys(get_description(dir_names[n]))
    time.sleep(10)

    tag_len = get_tag_len(dir_names[n])

    for i in range (0, tag_len):
        elementSUBMIT2 = driver.find_element_by_xpath('//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[8]/div[2]/div/div/input')
        elementSUBMIT2.send_keys(get_tags(i, dir_names[n]))
        time.sleep(3)
        elementSUBMIT2.send_keys(Keys.ENTER)
    time.sleep(10)

    driver.find_element_by_xpath('//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[3]/div/div[1]/textarea').send_keys(Keys.CONTROL + "a")
    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[3]/div/div[1]/textarea').send_keys(Keys.DELETE)

    time.sleep(5)


    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div/button[1]'))).click()
    time.sleep(10)

    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="reactTarget"]/div/div[1]/div[2]/div/div/nav/a/button'))).click()


print("SUCCESS")
print("////////THESE TRACKS NEED TO BE EDITED")
print(to_be_edited)

driver.quit()
