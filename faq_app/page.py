class Page:
    spaceid = ""

    def __init__(self, id, titel, url, type):
        self.id = id
        self.type = type
        self.titel = titel
        self.url = url

    def set_space_id(self, spaceid):
        self.spaceid = spaceid

    def __str__(self):
        return "Id = " + str(self.id) + "\n" + "titel = " + self.titel + "\n" + "url = " + self.url + "\n" \
               + "Type = " + self.type + "\n" + "space_id = " + str(self.spaceid) + "\n"


