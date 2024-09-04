from utilities import deleteChildren
import re

def ask_s_n(string, limit):
    for i in range(limit):
        q = input("\n" + string + " S/N: ")
        correct = re.search("^[SNsn]{1} *$", q)

        if correct:
            return correct.group()[0][0].upper() == "S"
        else:
            if (i == limit): return None
            print("Introduzca una de las dos opciones, le quedan " + str(limit - i - 1) + " intentos.")

def ask_for_p(paragraph_list):
    paragraph_list = [deleteChildren(x, ["sup", "style", "annotation"]) for x in paragraph_list]

    def duplicatedFilter(p):
        if (p[0].name == "math"):
            destroy = p[1]
            return destroy
        else:
            return p[0]

    paragraph_list = filter(duplicatedFilter, paragraph_list)
    paragraph_list = list(map(lambda x: x[0], paragraph_list))

    for i in range(len(paragraph_list)):
        current_p = paragraph_list[i]

        this_paragraph = current_p

        if (hasattr(current_p, "get_text")):
            this_paragraph = current_p.get_text().strip()

        print("\nP-" + str(i + 1) + ":")
        print(this_paragraph)

        if (i + 1) >= len(paragraph_list):
            print("\n" + "-"*25 + "Ultimo parrafo alcanzado." + "-"*25)
            break
        
        ans = ask_s_n("\n¿Quiere leer el siguiente parrafo?", 5)

        if (ans):
            continue
        else:
            break


async def ask(str, limit, no_links:filter=None):
    if (no_links is None): no_links = []
    which_one = input(str)
    restart = lambda: ask(str, limit, no_links)
    try:
        which_one = int(which_one) - 1
    except:
        print("Se le solicitó un número.")
        await restart()
            
    if (int(which_one) >= limit or which_one < 0):
        print("Seleccione un número dentro del rango.")
        await restart()
    
    if (int(which_one) in no_links):
        print("Esa opcion no tiene un link valido porque apunta a nuestra direccion actual")
        await restart()

    return which_one