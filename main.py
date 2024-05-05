from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Launch the browser
driver = webdriver.Chrome()

# Open URL
driver.get("http://www.google.com")

# Enter the keyword "amazon" in the search bar
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys("amazon")
search_bar.send_keys(Keys.RETURN)

# Print all the search results
search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
for result in search_results:
    print(result.text)

# # Click on the link which takes you to the amazon login page
amazon_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Amazon")
time.sleep(5)
amazon_link.click()

time.sleep(5)
driver.find_element(By.XPATH, "//*[@id='nav-signin-tooltip']/a/span").click()

# Login to https://www.amazon.in/ (You need to fill in your login details)
username = "username"
password = "password"

email_field = driver.find_element(By.ID, "ap_email")
email_field.send_keys(username)

time.sleep(5)
continue_button = driver.find_element(By.ID, "continue")
continue_button.click()

time.sleep(5)
password_field = driver.find_element(By.ID, "ap_password")
password_field.send_keys(password)

# Locate the submit button and click it
submit_button = driver.find_element(By.ID, "signInSubmit")
submit_button.click()


# Click on all buttons on search & select Electronics
buttons = driver.find_element(By.XPATH, "//select[@id='searchDropdownBox']")
for button in buttons:
    button.click()
#
# # Search for dell computers
search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
search_bar.clear()
search_bar.send_keys("dell computers")
search_bar.send_keys(Keys.RETURN)
#
# # Apply the filter of range Rs 30000 to 50000
range_filter = driver.find_element(By.LINK_TEXT, "₹30,000 - ₹50,000")
range_filter.click()


# Collecting prices from the first two pages
prices = []

for _ in range(2):  # Loop through the first two pages
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-include-content-margin")))
    products = driver.find_elements(By.CSS_SELECTOR, ".s-include-content-margin")
    for product in products:
        try:
            price_element = product.find_element(By.CSS_SELECTOR, ".a-price-whole")
            price = int(price_element.text.replace(",", ""))
            prices.append(price)
        except Exception as e:
            print(f"Failed to fetch price: {e}")
    # Navigate to the next page
    next_page_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
    next_page_button.click()
    time.sleep(2)  # Add a short delay for the next page to load

# Check if all prices are within the range
valid_prices = all(30000 <= price <= 50000 for price in prices)
if valid_prices:
    print("All products on the first two pages are within the range of Rs 30,000 to Rs 50,000.")
else:
    print("Some products on the first two pages are not within the specified range.")


# Collecting products with a rating of 5 out of 5 from the first two pages
for _ in range(2):  # Loop through the first two pages
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-include-content-margin")))
    products = driver.find_elements(By.CSS_SELECTOR, ".s-include-content-margin")
    for product in products:
        try:
            rating_element = product.find_element(By.CSS_SELECTOR, ".a-icon-star-small")
            rating = float(rating_element.text.split()[0])  # Extract the rating value
            if rating == 5.0:
                # If the rating is 5 out of 5, print the product details
                name_element = product.find_element(By.CSS_SELECTOR, ".a-size-medium")
                price_element = product.find_element(By.CSS_SELECTOR, ".a-price-whole")
                print("Product:", name_element.text)
                print("Price:", price_element.text)
                print("-" * 50)
        except Exception as e:
            print(f"Failed to fetch product details: {e}")
    # Navigate to the next page
    next_page_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
    next_page_button.click()
    time.sleep(2)  # Add a short delay for the next page to load

# Find and add the first product with a rating of 5 out of 5 to a new wish list
found_product = False
product_url = ""

for _ in range(2):  # Loop through the first two pages
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-include-content-margin")))
    products = driver.find_elements(By.CSS_SELECTOR, ".s-include-content-margin")
    for product in products:
        try:
            rating_element = product.find_element(By.CSS_SELECTOR, ".a-icon-star-small")
            rating = float(rating_element.text.split()[0])  # Extract the rating value
            if rating == 5.0:
                # If the rating is 5 out of 5, add the product to the wish list
                product_url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                # Click on the product to go to its details page
                product.click()
                found_product = True
                break
        except Exception as e:
            print(f"Failed to fetch product details: {e}")
    if found_product:
        break  # Exit the loop if a product with rating 5 out of 5 is found
    # Navigate to the next page
    next_page_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
    next_page_button.click()
    time.sleep(2)  # Add a short delay for the next page to load

# Add the product to the wish list
driver.find_element(By.ID, "add-to-wishlist-button-submit").click()

# Navigate to the wish list page
driver.get("https://www.amazon.in/gp/registry/wishlist")

# Validate if the product is added to the wish list
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[@href='{product_url}']")))
    print("Product is successfully added to the wish list!")
except Exception as e:
    print("Product is not added to the wish list:", e)

# Close the browser
driver.quit()