import time
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup


def get_words(link):
    """
    Function that gathers common first ASL words for initial data.
    """

    hundred_words_html = requests.get(link).text

    soup = BeautifulSoup(hundred_words_html, features='lxml')

    html_list = soup.find('ol', attrs={'class': 'col-list'}).find_all('li')

    word_list = []
    for i in html_list:
        word_list.append(i.text.replace('\n', ' ').strip())

    return word_list


def get_video_urls(driver, word, res):
    """
    Get URLs for videos associated with a particular phrase/word.
    """
    videos = driver.find_elements_by_tag_name('video')
    # videos = driver.find_elements_by_tag_name('source')

    url_list = []
    for video in videos:
        html = video.get_attribute('innerHTML')
        _, _, temp = html.partition('"')
        url, _, _ = temp.partition('"')

        url_list.append(f"{url}")

    res[f"{word}"] = url_list

    return res


def search_ASL(driver, words):
    """
    Searches all specified words on ASL website
    """
    res = {}
    for word in words:
        time.sleep(3)
        search_field = driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div/div/div/input')
        search_field.send_keys(word)
        driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div/div/div/span/button/span').click()
        time.sleep(3)
        res = get_video_urls(driver, word, res)
        print(str(res).replace("'", '"'))
        driver.back()
        driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div/div/div/input').clear()

        with open('test', 'w') as f:
            f.write(str(res).replace("'", '"'))

    return str(res)


def main():
    words = get_words('https://www.handspeak.com/word/most-used/')

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get('https://www.signasl.org/')

    res = search_ASL(driver, words)

    res = res.replace("'", '"')

    res = json.loads(res)

    return res

    driver.quit()


main()
