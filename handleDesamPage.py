from utilities import find_href
from ask_funcs import ask
from selenium.webdriver.common.by import By

async def handle_desam_page(driver, base_url, soup):
    print("Se obtuvieron varios resultados con un título similar:")
    querySelector = '[class="rellink noprint mw-disambig-page hatnote"]+p+ul li'
    
    li_list = tuple(soup.select(querySelector))
    links = tuple(map(lambda x: base_url + find_href(x), li_list))

    check = lambda x: x == base_url

    no_links = [ i if check(links[i]) else -1 for i in range(len(links)) ]
    no_links = tuple(filter(lambda i: i != -1, no_links))

    tag_texts = tuple(map(
        lambda li: tuple(li.children)[0].string + tuple(li.children)[1],
        li_list
    ))
        
    [
        print(
            f"{x + 1}.- {tag_texts[x]}", " (sin link)." if x in no_links else ""
        ) for x in range(len(tag_texts))
    ]
    selected = await ask("Cual te gustaria escoger? Seleccione un numero: ", len(tag_texts), no_links)

    print("Este es el link! -> " + links[selected])

    a_link = links[selected].replace(base_url, "")

    driver.find_element(By.CSS_SELECTOR, f"[href='{a_link}']").click()
