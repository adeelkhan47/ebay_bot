import csv
import math
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def open_window(url, description, price, link, image_url, all_products):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    more_than_10 = False
    try:
        quantity = driver.find_element(By.CLASS_NAME, "d-quantity__availability").text
        driver.close()
        if "More than 10 available" in quantity:
            more_than_10 = True
        quantity_count = quantity.split(" ")[0]
        if more_than_10:
            new_price = float(price[1:].replace(",", ""))
            quantity = "10 and more"
            total_price = "$ " + str(new_price * 10) + " and more"
        else:
            new_price = float(price[1:].replace(",", ""))
            total_price = int(quantity_count) * new_price
            quantity = quantity_count

    except Exception as e:
        total_price = "N/A"
        quantity = "N/A"
        print("Quantity not found. ")
    fetched_item = {
        'Title': description,
        'Price': price,
        'Available Quantity': quantity,
        'Total Estimated Price': total_price,
        'Url': link,
        'Image Url': image_url,

    }
    all_products.append(fetched_item)


def get_ebay_store_items(store_name):
    options = webdriver.ChromeOptions()
    # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(options=options)
    all_products = []
    url = f"https://www.ebay.com/str/{store_name}?_fcid=1&_pgn=1"
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'str-search__input')))

    count = driver.find_element(By.CLASS_NAME, 'str-search__input').get_attribute("placeholder")
    count = int(count.split(" ")[2])
    total_pages = math.ceil(count / 48)
    page = 1
    try:
        while page <= total_pages:
            url = f"https://www.ebay.com/str/{store_name}?_fcid=1&_pgn={page}"
            driver.get(url)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'str-item-card')))

            items = driver.find_elements(By.CLASS_NAME, 'str-item-card')
            if len(items) == 0:
                break
            for index, item in enumerate(items):
                try:

                    time.sleep(0.5)
                    price = item.find_element(By.CLASS_NAME, "str-item-card__property-displayPrice").text
                    try:
                        image_url = item.find_element(By.CLASS_NAME, "str-image").find_element(By.CSS_SELECTOR,
                                                                                               "img.landscape.no-scaling.zoom").get_attribute(
                            "src")
                    except:
                        image_url = ""
                    description = item.find_element(By.CLASS_NAME, "str-item-card__property-title").text
                    item.click()

                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "lightbox-dialog__main")))
                        link = driver.find_element(By.CLASS_NAME, "lightbox-dialog__main")
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='quickviewDialogHeading']/a")))
                        # link = link.find_element(By.ID, "quickviewDialogHeading")
                        time.sleep(0.5)
                        link = link.find_element(By.XPATH, "//*[@id='quickviewDialogHeading']/a").get_attribute("href")
                    except:
                        link = ""
                    open_window(link, description, price, link, image_url, all_products)
                    # fetched_item = {
                    #     'Title': description,
                    #     'Price': price,
                    #     'Url': link,
                    #     'Image Url': image_url,
                    # }
                    # all_products.append(fetched_item)
                    #time.sleep(0.5)
                    driver.find_element(By.CLASS_NAME, "lightbox-dialog__close").click()
                    print(f"Page : {page} Item : {index} Passed.")

                except Exception as e:
                    print(f"Page : {page} Item : {index} Failed.")
            page += 1
    except Exception:
        print("Page Completed or Not Found.")
    driver.close()
    # The name of the CSV file you want to save
    filename = f"{store_name}_products.csv"

    # Writing to csv file
    with open(filename, 'w') as csvfile:
        # Field names
        fields = ['Title', 'Price', 'Url', 'Image Url']

        # Create a CSV dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # Write the headers
        writer.writeheader()

        # Write the product data
        for product in all_products:
            writer.writerow(product)
    return True


def get_ebay_usr_items(usr):
    options = webdriver.ChromeOptions()
    # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(options=options)
    all_products = []
    url = f"https://www.ebay.com/usr/{usr}?_fcid=1&_pgn=1"
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'str-search__input')))

    count = driver.find_element(By.CLASS_NAME, 'str-search__input').get_attribute("placeholder")
    count = int(count.split(" ")[2])
    total_pages = math.ceil(count / 48)
    page = 1
    try:
        while page <= total_pages:
            url = f"https://www.ebay.com/usr/{usr}?_fcid=1&_pgn={page}"
            driver.get(url)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'str-item-card')))

            items = driver.find_elements(By.CLASS_NAME, 'str-item-card')
            if len(items) == 0:
                break
            threads = []
            for index, item in enumerate(items):
                try:
                    # url = f"https://www.ebay.com/usr/{usr}?_fcid=1&_pgn={page}"
                    # driver.get(url)
                    #time.sleep(0.5)
                    price = item.find_element(By.CLASS_NAME, "str-item-card__property-displayPrice").text
                    try:
                        image_url = item.find_element(By.CLASS_NAME, "str-image").find_element(By.CSS_SELECTOR,
                                                                                               "img.landscape.no-scaling.zoom").get_attribute(
                            "src")
                    except:
                        image_url = ""
                    details = item.find_element(By.CLASS_NAME, "str-item-card__property-title")
                    link = details.get_attribute("href")
                    description = details.find_element(By.CLASS_NAME, "str-text-span").text

                    # thread = threading.Thread(target=open_window,
                    #                           args=(url, description, price, link, image_url, all_products))
                    # threads.append(thread)
                    # thread.start()
                    open_window(link, description, price, link, image_url, all_products)
                    print(len(all_products))
                    print(f"Page : {page} Item : {index} Passed.")
                except Exception as e:
                    print(f"Page : {page} Item : {index} Failed.")
            for thread in threads:
                thread.join()
            page += 1
    except Exception:
        print("Page Completed or Not Found.")
    driver.close()
    # The name of the CSV file you want to save
    filename = f"{usr}_products.csv"

    # Writing to csv file
    with open(filename, 'w') as csvfile:
        # Field names
        fields = ['Title', 'Price', 'Available Quantity', 'Total Estimated Price', 'Url', 'Image Url']

        # Create a CSV dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # Write the headers
        writer.writeheader()

        # Write the product data
        for product in all_products:
            writer.writerow(product)
    return True


if __name__ == '__main__':

    store_name = "axiomtest"
    if store_name:
        for each in store_name.split(","):
            status = get_ebay_store_items(each)
            print(f"Store : {each} : Processed => {status}")
    usr = "siliconprobe"
    if usr:
        for each in usr.split(","):
            status = get_ebay_usr_items(each)
            print(f"Store : {each} : Processed => {status}")
