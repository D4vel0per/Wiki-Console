from bs4 import BeautifulSoup, Tag
from math_parser import from_alt_to_txt

def find_href(li):
    tag = li.findChildren()[0]
    if len(tag.findChildren()) == 0:
        return ""
    else:
        return tag.findChildren()[0].get("href")

def string_mrow (mrow_tag):
    elements = tuple(filter(lambda x: x.get_text().strip(), mrow_tag.contents))
    results = ""
    for element in elements:
        if element.name == "mrow" or element.name == "mstyle":
            results += string_mrow(element)
        elif element.name == "msqrt":
            results += f"√({string_mrow(element)})"
        else:
            results += element.get_text()

    return results


def clean_HTML(str):
    soup = BeautifulSoup(str, "html.parser")
    text = soup.get_text().split()

    return "".join(text)

def deleteChildren(parent: Tag, tag_names: list):
    for child in parent.findChildren():
        if (child.name in tag_names):
            child.extract()
        elif (hasattr(child, "find_all") and len(child.find_all()) > 0):
            child = deleteChildren(child, tag_names)[0]

    if (parent.name == "blockquote"):
        div_quote = parent.find("div", attrs={"class": "quote"})
        if (not div_quote): 
            div_quote = deleteChildren(parent.find("math"), tag_names)[0]


        text = div_quote.get_text().strip()
        if (not div_quote.string):
            for child in div_quote.findChildren():
                child.extract()

        div_quote.string = f"«{text}»"

    elif (parent.name == "math" and parent.find("mrow")):
        math_parsed = ""
        if (parent.get("alttext")):
            math_parsed = from_alt_to_txt(parent.get("alttext"))

        mrow = parent.find("mrow")

        math_text = string_mrow(mrow)
        
        for child in parent.findChildren():
            child.extract()

        if (len(math_parsed) > 0):
            print(math_parsed)
            parent.string = math_parsed
        else:
            parent.string = clean_HTML(math_text)

        return [parent, True]

    return [parent, False]

# MODIFY THE string_mrow TO INSPECT THE alttext ATTRIBUTE DIRECTLY