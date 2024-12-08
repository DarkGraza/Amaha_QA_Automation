import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

url = "https://www.radiustheme.com/demo/wordpress/themes/zilly/"
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)
time.sleep(5)


pages = []

# Function for appending product categories
def counting(cat_list):
    categories = dict()
    categories['Total Count'] = 0
    for _ in cat_list:
        categories['Total Count'] += 1
        cat = _.text.strip()
        if cat in categories:
            categories[cat] = categories[cat] + 1
        else:
            categories[cat] = 1
    pages.append(categories)


def screenshot(name):
    ss_path = os.path.join(r"C:\Users\msati\OneDrive\Desktop\ZillySS", name)
    driver.save_screenshot(ss_path)


# Locate trending categories
trending_section = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@data-id="ebf650e"]//a[@rel="tag"]')
    )
)
time.sleep(5)
print("Number of categories: " , len(trending_section))
counting(trending_section)
print("Categories in the trending section at home page: ",pages)

# Click See More on trending section
trending_page = driver.find_element(By.XPATH, '//div[@data-id="b423390"]//a')
trending_page.click()
time.sleep(3)

#Click Load until no load is option visible
while True:
    try:
        load = driver.find_element(By.XPATH, "//button[@data-paged]")
        present_page = load.get_property('data-paged')
        last_page = load.get_attribute('data-max-page')
        load.click()
        time.sleep(5)
    except:
        break

# Locate all product categories
prod_cats = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@class="product-cat"]//a')
        )
    )
counting(prod_cats)
print("All categories in trending section after Load: ", pages[1])


# Locate a product to add in cart
add_cart = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,'//a[@title="Add to cart"]')
    )
)
# Using Javascript to mimick user action
driver.execute_script("arguments[0].scrollIntoView(true);", add_cart)
driver.execute_script("arguments[0].click();", add_cart)

# Locating cart icon and redirect into cart page
cart = driver.find_element(By.ID, "rtsb-cart-float-menu")
cart.click()
time.sleep(2)


view_cart = driver.find_element(By.XPATH, '//a[@class="button wc-forward"]')
view_cart.click()

# increasing cart product quantity
plus = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="rtsb-quantity-btn rtsb-quantity-plus"]')
    )
)
ss_name = "SS_after_adding_to_cart.png"
screenshot(ss_name)
plus.click()
time.sleep(1)




time.sleep(1)

# removal of all items in cart
remove = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//a[@class="remove"]')
    )
)
ss_name = "SS_after_removing_from_cart.png"
screenshot(ss_name)
remove.click()




# Return from cart to trending page
return_from_cart = driver.find_element(By.XPATH, '//a[@class="button wc-backward"]')
ss_name = "SS_return_from_cart.png"
screenshot(ss_name)
return_from_cart.click()

# Sending "organic" word in hidden form and wait for the dropdown of suggestions
keyword = "organic"
search = driver.find_element(By.CSS_SELECTOR, "input.form-control.product-search-form.product-autocomplete-js")
search.click()
#driver.execute_script("argument[0].click()", search)
search.send_keys(keyword)
time.sleep(3)
ss_name = "SS_organic_search.png"
screenshot(ss_name)

# Dropdown
suggestions = driver.find_elements(By.XPATH, '//ul//h3')
search_suggestions = []
for _ in suggestions:
    search_suggestions.append(_.text)
search_suggestions.append(f"Total Suggestions: {len(suggestions)}")
print(f"Search Suggestions for {keyword} -> ",search_suggestions)

driver.quit()
