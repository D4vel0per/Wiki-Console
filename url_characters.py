reserved = lambda: {
    "!": "%21",
    "#": "%23",
    "$": "%24",
    "&": "%26",
    "'": "%27",
    "(": "%28",
    ")": "%29",
    "*": "%2A",
    "+": "%2B",
    ",": "%2C",
    "/": "%2F",
    ":": "%3A",
    ";": "%3B",
    "=": "%3D",
    "?": "%3F",
    "@": "%40",
    "[": "%5B",
    "]": "%5D",
    " ": "%20"
}

def url_encode(str):
    reserved_characters = reserved()

    for key_R in reserved_characters:
        str = str.replace(key_R, reserved_characters[key_R])

    return str
