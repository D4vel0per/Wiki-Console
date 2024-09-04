import subprocess
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from handleResultsPage import handle_results_page
from models import User
from bs4 import BeautifulSoup, Tag
import asyncio
from ask_funcs import ask_for_p, ask_s_n

def check_for_try_again(soup, selector):
    try_state = "found"
    if (soup.select_one(selector)):
        try_state = "try_again" if ask_s_n(
            "No hay resultados que cumplan los criterios de búsqueda. ¿Intentar de nuevo? ->",
            5
        ) else "close"

    return try_state

def get_soup(driver):
    return BeautifulSoup(driver.page_source, "html.parser")

async def search_for(driver, fetch_url, searchStr):
    
    print("SEARCH_FOR")
    driver.get(fetch_url)
    soup = get_soup(driver)
    element1 = driver.find_element(By.CSS_SELECTOR, '#searchText [name="search"]')
    element1.click()
    element1.send_keys(searchStr, Keys.ENTER)

    desam_selector = 'span.mw-disambig-icon'
    results_selector = 'li.mw-search-result.mw-search-result-ns-0 a'
    not_found_s = "p.mw-search-nonefound"
    soup = get_soup(driver)
            
    if (soup.select_one(results_selector) is not None):
        await handle_results_page(driver, results_selector, soup, desam_selector)

    try_state = check_for_try_again(get_soup(driver), not_found_s)
    if (try_state == "try_again"):
        srch = input("¿Que quieres buscar? -> ")
        await search_for(driver, fetch_url, srch)

    elif (try_state == "found"):
        soup = get_soup(driver)
        all_ps = soup.select("div.mw-content-ltr.mw-parser-output>p,blockquote,math")
        all_ps = list(filter(lambda p: p.get_text().strip(), all_ps))

        ask_for_p(all_ps)

    return driver
    

async def search(driver, search_count):
    driver.minimize_window()
    print("Getting response...")
    fetch_url = "https://es.wikipedia.org/w/index.php?search=&title=Especial:Buscar"
    driver.implicitly_wait(10)

    for i in range(5):
        user_search = input("¿Que quieres buscar? -> ")
        await search_for(driver, fetch_url, user_search)
        search_again = ask_s_n("¿Quiere buscar algún otro tema? ->", 5)
        if (not search_again):
            break
        

    '''
    element1 = driver.find_element(By.CSS_SELECTOR, '#searchText [name="search"]')
    element1.click()
    element1.send_keys(user_search, Keys.ENTER)
        
    desam_selector = 'span.mw-disambig-icon'
    results_selector = 'li.mw-search-result.mw-search-result-ns-0 a'
    soup = BeautifulSoup(driver.page_source, "html.parser")
            
    if (soup.select_one(results_selector) is not None):
        await handle_results_page(driver, results_selector, soup, desam_selector)
        search_again = ask_s_n("¿Quiere buscar algún otro tema? ->")
        if (search_again):
            await search_for(driver, user_search)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    '''
    print(driver.current_url)
    
    print("/" * 75)
    print("FINISHED.")
    driver.quit()
    return "OK!"

def review_data_get():
    pass

async def start(wait):
    await asyncio.sleep(wait)
    os.chdir(r"C:\Users\Omar David\adireviews")
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    driver = webdriver.Remote(
        options=options,
        command_executor="http://192.168.0.106:4444"
    )
    await search(driver, 0)

async def run_server():
    os.chdir(r"C:\Users\Omar David\adireviews\SeleniumGrid")
    print("STARTING SERVER...")
    process = await asyncio.create_subprocess_shell(
        'java -jar selenium-server-4.23.1.jar standalone', 
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    print("SERVER STARTED")

async def main():
    try:
        run_server_task = asyncio.create_task(
            run_server()
        )
        run_program_task = asyncio.create_task(
            start(10)
        )
        await run_program_task
        await run_server_task

    except Exception as e:
        print(type(e))
        ans = ask_s_n("An exception has occurred at main(), wanna see exception?", 5)
        if (ans): raise e
        else: print("OK!")

    
    
if __name__ == "__main__":
    asyncio.run(main())