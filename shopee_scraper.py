from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import csv

#Access shadowRoot of an element
def expand_element(element): 
	return driver.execute_script("return arguments[0].shadowRoot", element)

#Search term by typing
def search(search_term):
	search_bar = driver.find_element(By.CLASS_NAME, 'shopee-searchbar-input__input')
	search_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div/div[1]/div[1]/button')
	search_bar.send_keys(search_term)
	search_btn.click()

#Search term by url
def get_url(term):
    """Generate an url from the search term"""
    template = "https://www.shopee.com.my/search?keyword={}"
    term = term.replace(' ','+')
    
    #add term query to url
    url = template.format(term)
    
    #add page query placeholder
    url+= '&page={}'
    url+= '&sortBy=sales'
    
    return url

def get_data():
        #Scroll to bottom
    # wait = WebDriverWait(driver, 7)
    # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'col-xs-2-4 shopee-search-item-result__item')))
    time.sleep(2)
    for i in list(range(5)):
        ActionChains(driver).scroll_by_amount(0,1000).perform()
        time.sleep(0.5)

    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    try:
        for item in soup.find_all('div', {'class': 'col-xs-2-4 shopee-search-item-result__item'}):
            #item name
            item_n = item.find('div', class_='ie3A+n bM+7UW Cve6sh')
            if item_n is None:
                name = ''
            else:
                name = item_n.text

            #item initial cost
            item_init_c = item.find('div', class_='vioxXd ZZuLsr d5DWld')
            if item_init_c is None:
                init_cost = ''
            else:
                init_cost = item_init_c.text

            #item cost
            item_c = item.find_all('span', class_='ZEgDH9')
            if item_c is None:
                cost = ''
            elif len(item_c) > 1:
                cost = f"{item_c[0].text} - {item_c[1].text}"
            else:
                cost = item_c[0].text

            #discount percentage
            item_dp = item.find('span', class_='percent')
            if item_dp is None:
                disc_percent = ''
            else:
                disc_percent = item_dp.text

            #item sales per month
            item_s = item.find('div', class_='r6HknA uEPGHT')
            if item_s is None:
                sales = ''
            else:
                sales = item_s.text

            #item location
            item_l = item.find('div', class_='zGGwiV')
            if item_l is None:
                location = ''
            else:
                location = item_l.text

            #item link
            item_link = item.find('a', href=True)
            if item_link is None:
                link = ''
            else:
                link = f"https://shopee.com.my{item_link['href']}"

            rows.append([term, name, init_cost, cost, disc_percent, sales, location, link])



    except TimeoutException:
        print("Loading took too much time! - Try again")

# Chrome options

chrome_options = Options()
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('disable-infobars')
#Enable when need to check source code
# chrome_options.add_experimental_option("detach", True)

# #Close Popups
# # Wait for the language prompt to appear and click it
# wait = WebDriverWait(driver, 7)
# language_prompt = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button')))
# language_prompt.click()

# Search term and sort by top_sales

rows = []

pre_search_terms = input(f"\nEnter the keywords you want to scrape for.\n(If you have multiple keywords please separate them with commas)\nEg:'spicy ramen, toys, bicycle lights'\n\nKeywords: ")
search_terms = [x.strip() for x in pre_search_terms.split(',')]

while True:
    try:
        max_pages = int(input(f"\nEnter how many pages you want to search for: "))
        break
    except:
        print("Please only put in numbers!")

for term in search_terms:
    print(f"\nscraping data for {term}...")
    url = get_url(term)

    # Invoke browser and load site

    driver = webdriver.Chrome(options=chrome_options)

    for page in range(0,max_pages):
        driver.get(url.format(page))

        if page == 0:
            wait = WebDriverWait(driver, 7)
            language_prompt = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button')))
            language_prompt.click()
            print("scrolling page..")
            get_data()
            print(f"scraped page {page+1}/{max_pages}")
        else:
            print("scrolling page..")
            get_data()
            print(f"scraped page {page+1}/{max_pages}")
        
    print(f'\nall "{term}" data has been scraped.')

# for k,v in enumerate(rows,1):
#     print(k,v)

with open('shopee_item_list.csv','w', newline='',encoding='utf-8') as f:
	writer=csv.writer(f)
	writer.writerow(['search_term', 'name', 'init_cost', 'cost', 'disc_percent', 'sales', 'location', 'link'])
	writer.writerows(rows)

print("\nall done! data is stored in a CSV file in your directory.")