gevonden_woord = ""
links = {"python": "http://tdc-www.harvard.edu/Python.pdf"}
gevraagd = ""


def check_for_word(sentence):
    global gevraagd
    global gevonden_woord

    gevraagd = str(sentence).split()

    for word in get_sleutel():
        new_w = word.replace("\n", "")
        for i in gevraagd:
            if new_w == i:
                gevonden_woord = new_w
                return True


def get_bericht():
    for x in get_antwoorden():
        if gevonden_woord in x:
            if gevonden_woord == "lijst":
                return x + str(sleutels_str())
            return x
    if gevonden_woord == "documentatie":
        return get_link()
    return "wij werken er aan"


def get_antwoorden():
    try:
        bestand = open("doc/antwoorden.txt", 'r')
    except IOError:
        print("bestands fout")
    antwoorden = []
    for i in bestand:
        antwoorden.append(i)
    return antwoorden


def get_sleutel():
    try:
        bestand = open("doc/sleutel_woorden.txt", 'r')
    except IOError:
        print("bestands fout")
    sleutels = []
    for i in bestand:
        sleutels.append(i)
    return sleutels


def sleutels_str():
    string = ""
    for i in get_sleutel():
        string += ("*"+i.replace("\n", "")+", * ")
    return string


def get_link():
    global link
    for i in links:
        for j in gevraagd:
            if i == j:
                link = "De documentatie over " + i + " vind je op volgende link: " + links[j]
                return link
            else:
                link = "Sorry ik weet het niet"
    return link

