class Page:
    spaceid = ""

    def __init__(self, id, title, url, type):
        self.id = id
        self.type = type
        self.title = title
        self.url = url

    def set_space_id(self, spaceid):
        self.spaceid = spaceid

    def __str__(self):
        return "Id = " + str(self.id) + "\n" + "title = " + self.title + "\n" + "url = " + self.url + "\n" \
               + "Type = " + self.type + "\n" + "space_id = " + str(self.spaceid) + "\n"


