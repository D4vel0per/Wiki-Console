from urllib.request import urlopen
from bs4 import BeautifulSoup
import mechanicalsoup
import asyncio

# BEAUTIFUL SOUP

#def beauty (url):
#    url = "http://olympus.realpython.org/profiles"
#    page = urlopen(url)
#    html = page.read().decode("utf-8")
#    soup = BeautifulSoup(html, "html.parser")
#    return soup

# MECHANICAL SOUP

#async def mechanical (url, i):
#    browser = mechanicalsoup.Browser()
#    page = browser.get(url)
#    dice = page.soup.select("#result")[0]
#    print("Call " + str(i))

#    return dice.text

#async def main_function (count):
#    url = "http://olympus.realpython.org/dice"
#    print("Please wait...")
#    L = await asyncio.gather(
#        *[mechanical(url, i) for i in range(count)]
#    )
    
