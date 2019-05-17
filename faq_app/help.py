import databank

gevonden_woord = ""
gevraagd = []
idchannel = ""


# deze fuctie gaat zoeken in de zin of er een sleutelwoord is
# geeft de gevonden woord door
# geeft de idchannel door
# geeft de zin door
def check_for_word(sentence, channelid):
    global gevraagd
    global gevonden_woord
    global idchannel

    gevraagd = str(sentence).split()
    idchannel = channelid

    for word in databank.get_keywords():
        for i in gevraagd:
            if word == i.lower():
                gevonden_woord = word
                return True


# deze functie zoekt naar een antwoord voor het gevonde woord
# indien het woord 'documentatie' is wordt de fuctie get_link() opgeroepen
# indien het woord 'lijst' is gaat de fuctie sleutels_str opgeroepen worden
# anders word de opgeslagen antwoord verzonden
def get_bericht():
    x = databank.get_answer(gevonden_woord)
    if gevonden_woord == "lijst":
        return x + "\n " + sleutels_str()
    if gevonden_woord == "documentatie":
        return get_link()
    else:
        return x


# neemt de array van sleutelwoorden en zet die om in 1 string
# de "*" aan het begin en het einde van het woord maken de tekst vet in slack
def sleutels_str():
    string = ""
    for i in databank.get_keywords():
        string += ("*" + i + "* ")
    return string


# haal de link op in de database
# zoekt naar de juiste titel
def get_link():
    global link
    global teller
    global arr
    link = ""
    arr = {}
    for t in databank.get_titles():
        titelarr = str(t).split()
        teller = 0
        for s in titelarr:
            if s in gevraagd:
                teller += 1
        if teller == titelarr.__len__() or teller >= (titelarr.__len__()/2):
            if get_space_id(idchannel) != "":
                link = "*" + t + "*" + databank.get_answer(gevonden_woord) + "\n" + \
                       databank.get_link_sp(t, gevonden_woord, get_space_id(idchannel))
            else:
                link = "*" + t + "*" + databank.get_answer(gevonden_woord) + "\n" + databank.get_link(t, gevonden_woord)

            arr.update({teller: link})
    link = arr.get(max(arr.keys()))
    return link


# wijs de juiste channelid bij de juiste space, zelf toe te wijzen
def get_space_id(channelid):
    if channelid == "CJR8SR1JR":
        return databank.get_space_id("FAQD")
    elif channelid == "CJJ9PRH39":
        return databank.get_space_id("FAQO")
    else:
        return ""
