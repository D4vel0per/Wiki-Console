from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from handleDesamPage import handle_desam_page
from Library import BASE_URLs

from ask_funcs import ask

async def handle_results_page (driver, selector, soup, desam_selector):
    print("Resultados conseguidos: ")
    res = list(map(lambda a: a.get_text().strip(), soup.select(selector)))
    res = list(filter(lambda text: len(text) > 0, res))
    [print(f"{x + 1}.- " + res[x]) for x in range(len(res))]
    which_one = await ask("Cual te gustaria escoger? Seleccione un numero: ", len(res))

    href = list(
        map(lambda x: x.get_attribute("href"), 
            filter(lambda a: a.text, driver.find_elements(
                By.CSS_SELECTOR,
                selector
                )
            )
        )
    )[which_one]
            
    print("Este es el link! -> " + href)
    
    link = driver.find_element(
        By.CSS_SELECTOR,
        f'[href="{href.replace(BASE_URLs["WIKIPEDIA"], "")}"]'
    )
    link.click()
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    if (soup.select_one(desam_selector)):
        await handle_desam_page(driver, BASE_URLs["WIKIPEDIA"], soup)