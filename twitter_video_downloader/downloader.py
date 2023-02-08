import os
import operator
from collections import namedtuple
import logging
import argparse
import requests
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

version_tag = "1.0.0"
update_check_endpoint = "https://api.github.com/repos/rly0nheart/twitter-video-downloader/releases/latest"


# create the downloads directory if it doesn't already exist
def path_finder():
    os.makedirs("twitter_downloads", exist_ok=True)


# print license note
def notice():
    return f"""
    twitter-video-downloader {version_tag} Copyright (C) 2023  Richard Mwewa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
    """


# check for updates via the GitHub api
def check_updates():
    path_finder()
    print(notice())
    response = requests.get(update_check_endpoint).json()
    if response['tag_name'] == version_tag:
        # ignore if the program is up-to-date
        pass
    else:
        print(
            f"[UPDATE] A new release is available ({response['tag_name']}). Run 'pip install --force-reinstall --no-deps git+git://github.com/rly0nheart/twitter-video-downloader' to get the updates.")


class TwitterVideoDownloader:
    def __init__(self):
        # create argument parser)
        # set selenium to --headless (hides the firefox browser)
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        self.driver = webdriver.Chrome(options=option)
        self.download_endpoint = "https://twittervideodownloader.com"

    # select video quality
    # returns xpath_element
    def video_quality(self):
        xpath_element = "/html/body/div[2]/div/center/div[5]/div[1]/a"
        return xpath_element

    # download video
    def download_video(self, url):
        path_finder()
        print(f"Started downloader with {url}")
        self.driver.get(self.download_endpoint)
        url_entry_field = self.driver.find_element(By.NAME, "tweet")
        url_entry_field.send_keys(url)
        url_entry_field.send_keys(Keys.ENTER)
        print("Loading web resource, please wait..")
        download_btn = WebDriverWait(self.driver, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/center/div[5]/div[1]/a")))

        hrefs = self.driver.find_elements(By.XPATH, "/html/body/div[2]/div/center/div[@class='row']/div[1]/a")
        qualities = self.driver.find_elements(By.XPATH, "/html/body/div[2]/div/center/div[@class='row']/div[2]/p")
        assert hrefs and "cannot find hrefs"
        assert qualities and "cannot find qualities"
        assert len(hrefs) == len(qualities) and "qualities count not equal to hrefs"
        hrefs = [i.get_attribute("href") for i in hrefs]
        qualities = [i.text for i in qualities]

        Links = namedtuple("Links", ['width', 'height', "area", "href"])
        links = []
        for i in range(len(hrefs)):
            w, h = qualities[i].split(':')[0].strip().split('x')
            w = int(w)
            h = int(h)
            links.append(Links(w, h, w * h, hrefs[i]))
        links.sort(key=operator.itemgetter(2), reverse=True)
        print(links)

        video_url = links[0].href
        save_name = "_".join(url[url.find("://") + 3:].split("/")[1:])
        save_dir = "./twitter_downloads"
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        with requests.get(video_url, stream=True) as response:
            response.raise_for_status()
            with open(os.path.join(save_dir, f"{save_name}.mp4"), 'wb') as file:
                for chunk in tqdm(response.iter_content(chunk_size=8192), desc=f"Downloading {file.name}"):
                    file.write(chunk)
                print(f"Downloaded:", file.name)
        self.driver.close()
