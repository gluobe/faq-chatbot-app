import databank

gevonden_woord = ""
gevraagd = []


# deze fuctie gaat zoeken in de zin of er een sleutelwoord is
def check_for_word(sentence):
    global gevraagd
    global gevonden_woord

    gevraagd = str(sentence).split()

    for word in databank.get_sleutels():
        for i in gevraagd:
            if word == i.lower():
                gevonden_woord = word
                return True


# deze functie zoekt naar een antwoord voor het gevonde woord
# indien het woord 'documentatie' is wordt de fuctie get_link() opgeroepen
# indien het woord 'lijst' is gaat de fuctie sleutels_str opgeroepen worden
# anders word de opgeslagen antwoord verzonden
def get_bericht():
    x = databank.get_antwoord(gevonden_woord)
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
    for i in databank.get_sleutels():
        string += ("*" + i + "* ")
    return string


# zoekt een "titel" in de opgegeven zin en geeft het door naar de databank, de databank geeft een link terug
'''
def get_link():
    global link
    for i in databank.get_titels():
        for j in gevraagd:
            if i == j:
                link = "*" + i + "*" + databank.get_antwoord(gevonden_woord) + "\n" + databank.get_link(j, gevonden_woord)
                return link
            else:
                link = "Ik weet niet welke documentatie u zoekt, ik heb volgende documentatie links: "
    return link

'''


def get_link():
    global link
    global teller
    global arr
    link = ""
    arr = {}
    for t in databank.get_titels():
        titelarr = str(t).split()
        teller = 0
        for s in titelarr:
            if s in gevraagd:
                teller += 1
        if teller == titelarr.__len__() or teller >= (titelarr.__len__()/2):
            link = "*" + t + "*" + databank.get_antwoord(gevonden_woord) + "\n" + databank.get_link(t, gevonden_woord)
            arr.update({teller: link})
            # print(arr)
    link = arr.get(max(arr.keys()))
    return link


print(check_for_word("documentatie Azure en Ansible"))
print(get_bericht())
