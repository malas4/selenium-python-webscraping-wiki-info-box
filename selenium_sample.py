
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import csv

@pytest.fixture
def browser():

    driver =webdriver.Chrome(executable_path='')
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_wiki_search(browser):

    browser.get("https://www.wikipedia.com")
    languages = browser.find_element_by_id('searchLanguage')

    Select(languages).select_by_visible_text('English')

    search_input = browser.find_element_by_id('searchInput')
    search_input.send_keys('mars')
    search_button = browser.find_element_by_xpath('//div[@class ="search-container"]//button[@class ="pure-button pure-button-primary-progressive"]')
    search_button.click()
    #assert results page appears
    first_heading = browser.find_element_by_xpath('//*[@id="firstHeading"]').text
    assert first_heading == "Mars"


    num_rows = len(browser.find_elements_by_xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr'))
    assert num_rows > 0

    with open("wikidata.csv", mode = 'w') as wiki_file:
        writer = csv.writer(wiki_file)
        for r in range(num_rows):

            try:

                value = browser.find_element_by_xpath(
                '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[' + str(r) + ']').text
                writer.writerow([value])
                print(value)
            except:
                print("no text")


