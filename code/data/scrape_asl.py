import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_words(link):
    """
    Function that gathers common first ASL words for initial data.
    From: https://www.handspeak.com/word/most-used/
    """

    hundred_words_html = requests.get(link).text

    soup = BeautifulSoup(hundred_words_html, features='lxml')

    html_list = soup.find('ol', attrs={'class': 'col-list'}).find_all('li')

    word_list = []

    # Clean up html and populate words into list
    for i in html_list:
        word_list.append(i.text.replace('\n', ' ').strip())

    return word_list


def get_video_urls(driver, word, res):
    """
    Get URLs for videos associated with a particular phrase/word and populate to dictionary.
    """

    videos = driver.find_elements_by_tag_name('video')

    url_list = []
    for video in videos:
        html = video.get_attribute('innerHTML')

        # Hacky way to parse off associated URLs
        _, _, temp = html.partition('"')
        url, _, _ = temp.partition('"')

        url_list.append(url)

    res[word] = url_list

    return res


def search_ASL(driver, words):
    """
    Searches all specified words on ASL website
    """
    res = {}  # Dictionary to house words as associated video urls
    for word in words:
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/form/div/div/div/input'))
        )

        search_field.send_keys(word)  # adds word to search field

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/div/div/div/span/button/span'))
        )

        button.click()  # click search button

        res = get_video_urls(driver, word, res)


        driver.back()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/form/div/div/div/input'))
        ).clear()


    return res


if __name__ == '__main__':
    words = get_words('https://www.handspeak.com/word/most-used/')

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get('https://www.signasl.org/')

    res = search_ASL(driver, words)

    res = json.dumps(res)

    # Write json string to file
    with open ('videos.json', 'w') as f:
        f.write(res)

    driver.quit()
