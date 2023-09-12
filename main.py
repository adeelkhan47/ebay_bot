from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_ebay_store_items(url):
    # Start the Chrome driver
    options = webdriver.ChromeOptions()
    # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Ensure the page is loaded
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'str-item-card')))

    # Find all items
    items = driver.find_elements(By.CLASS_NAME, 'str-item-card')

    all_products = []

    for item in items:
        try:

            price = item.find_element(By.CLASS_NAME, "str-item-card__property-displayPrice").text
            image_url = item.find_element(By.CLASS_NAME, "str-image").find_element(By.CSS_SELECTOR,
                                                                                   "img.landscape.no-scaling.zoom").get_attribute(
                "src")
            description = item.find_element(By.CLASS_NAME, "str-item-card__property-title").text

            item.click()
            link = item.find_element(By.ID,"quickviewDialogHeading").find_element(By.TAG_NAME,"a").get_attribute("href")
            all_products.append({
                'Title': description,
                'price': price,
                'Url': "link",
                'image_url': image_url,

            })

        except Exception as e:
            print(f"Error processing item: {e}")

    # Close the browser
    driver.close()

    return all_products


if __name__ == '__main__':
    URL = "https://www.ebay.com/str/axiomtest?_fcid=1"
    products = get_ebay_store_items(URL)
    for product in products:
        print(product)
ø
