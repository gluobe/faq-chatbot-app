from atlassian import Confluence
from faq_app import conflu
from faq_app import page

import os

confluence = Confluence(
    url='https://confluence-test.xploregroup.net',
    username='simbaa1',
    password=os.getenv('DB_PASSWORD'))


pages = confluence.get_all_pages_from_space(space="GLUO", start=0, limit=500)
for item in pages:
    conflu.set_page(item['id'])

'''
    print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")

print(conflu.get_spaces_id())
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")

print(confluence.get_all_spaces(start=0, limit=500))
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")

'''


def zoek_page(space, titel):

    p = confluence.get_all_pages_from_space(space=space.upper(), start=0, limit=500)
    link = ""
    for i in p:
        if titel.lower() == str.lower(i['title']):
            link = i['_links']['webui']
        conflu.set_page(i['id'])
    print(link)


def get_confluence_spaces():
    p = confluence.get_all_spaces(start=0, limit=500)
    links = []
    for j in p:
        p = page.Page(j['id'], j['key'], j['_links']['webui'], j['type'])
        links.append(p)
    return links


def get_confluence_pages():
    links = []
    for i in get_confluence_spaces():
        p = confluence.get_all_pages_from_space(space=i.titel, start=0, limit=500)
        for j in p:
            p = page.Page(j['id'], j['title'], j['_links']['webui'], j['type'])
            p.set_space_id(i.id)
            links.append(p)
    return links


for i in get_confluence_spaces():
    print(i)

print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")

for i in get_confluence_pages():
    print(i)
