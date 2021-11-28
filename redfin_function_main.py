import pandas as pd
import time
import re
from re import search
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def set_driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.maximize_window()  # For maximizing window
    print("Please wait while the website loads.")
    driver.implicitly_wait(20)

    driver.get("https://www.redfin.com/")
    return driver


def get_values():
    # zmoha@wurric.site
    email = input("enter email :")
    # redfin@123
    password = input("enter password :")
    search = input("enter search : ")
    return email, password, search


def scrap_redfin(driver, email, password, search):
    login_button = driver.find_element_by_css_selector(
        'button[data-rf-test-name="SignInLink"]'
    )
    login_button.click()

    enter_email = driver.find_element_by_css_selector(
        'input[name="emailInput"]')
    time.sleep(3)

    enter_email.send_keys(email)
    submit_email = driver.find_element_by_css_selector(
        'button[class="button Button submitButton primary"]')
    submit_email.click()
    enter_password = driver.find_element_by_css_selector(
        'input[class="password"]')
    time.sleep(3)

    enter_password.send_keys(password)
    logged_in = driver.find_element_by_css_selector(
        'button[data-rf-test-name="submitButton"]')
    logged_in.click()
    driver.implicitly_wait(30)
    # enter_search = driver.find_element_by_css_selector(
    #     'input[class="search-input-box"]')

    driver.refresh()

    enter_search = driver.find_element_by_css_selector(
        'input[class="search-input-box"]')
    time.sleep(10)

    enter_search.send_keys(search)

    click_search = driver.find_element_by_css_selector(
        'button[data-rf-test-name="searchButton"]')
    click_search.click()

    # heading = driver.find_element_by_css_selector(
    #     'h1[data-rf-test-id="h1-header"]')
    # print(sixth.text)
    # el1 = driver.find_element_by_css_selector('div[class="bottomV2 "]')
    # el2 = driver.find_element_by_css_selector('span[class="homecardV2Price"]')
    # print(el2.text)

    # complete = driver.find_elements_by_css_selector(
    #     'div[class="PhotosView bg-color-white above-the-fold"]')
    # print(complete.text)

    # scrape items
    price = []
    stats = []
    address = []
    page_count = driver.find_elements_by_css_selector(
        'a[class="clickable goToPage"]')
    page_no = 1
    for it in range(len(page_count)):

        for p in driver.find_elements_by_css_selector(
                'span[data-rf-test-name="homecard-price"]'):
            card_price = p.text
            price.append(card_price)

        st = driver.find_elements_by_css_selector('div[class="bottomV2 "]')
        for i in st:
            card_stats = i.find_element_by_css_selector(
                'div[class="HomeStatsV2 font-size-small "]').text
            n_text = re.sub('[\n]', ' ', card_stats)
            final_text = re.sub(',', ' ', n_text)
            stats.append(final_text)
        for ad in st:

            card_add = ad.find_element_by_css_selector(
                'span[data-rf-test-id="abp-streetLine"]').text
            address.append(card_add)
        page_no = page_no+1
        print('page {0} is extracted...'.format(page_no))
        next = driver.find_element_by_css_selector(
            'button[data-rf-test-id="react-data-paginate-next"]')
        next.click()
        time.sleep(10)

    all_houses = [price, [i for i in stats], address]

    # convert into dataframe
    house_details = pd.DataFrame(all_houses)
    house_details = house_details.T
    house_details = house_details.rename(
        columns={0: 'price', 1: 'house_statistics', 2: 'address'})
    # print(house_details.columns)
    print(house_details.shape)
    print()
    print(house_details['house_statistics'][1:2])
    print()
    return house_details


def save_csv(search, house_details):
    # saving into csv
    file_path = input(
        "please provide correct and complete path of your directory:")
    try:
        # house_details.to_csv('D:\\DataSets\\' + search + '.csv', index=False)
        house_details.to_csv(file_path + "\\" + search + '.csv', index=False)
        complete_path = file_path + "\\" + search + '.csv'
        print("file is saved successfully at {0}".format(complete_path))
    except:
        print("there is an error to save the file")


driver = set_driver()
email, password, search = get_values()
house_details = scrap_redfin(driver, email, password, search)
save_csv(search, house_details)
