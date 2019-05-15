# import van modulen
import mysql.connector
import os
import requests
from atlassian import Confluence
import page


mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  passwd=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_NAME')
)

if mysql.connector.connect():
    print("DB connection ok")
else:
    print("DB Connection faild")

confluence = Confluence(
    url=os.getenv('CONFLUENCE_URL'),
    username=os.getenv('CONFLUENCE_USER'),
    password=os.getenv('CONFLUENCE_PW'))


try:
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS faqchat")
except mysql.connector.Error as errors:
    mydb.rollback()
    print("Failed to create database faqchat {}".format(errors))
finally:
    # closing database connection.
    cursor.close()

# print(mydb.is_connected().__str__())
# Aanmaak tabellen, na het aanmaken moeten deze lijnen weg


def create_tables():
    try:
        global cursor
        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS antwoorden (antwoord_ID INT AUTO_INCREMENT  PRIMARY KEY, "
                       "antwoord VARCHAR(255))")

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS sleutelwoorden (sleutelw_ID INT AUTO_INCREMENT PRIMARY KEY, antwoord_ID"
            " INT NOT NULL,FOREIGN KEY fk_antwoord_ID(antwoord_ID) REFERENCES antwoorden(antwoord_ID),"
            " sleutel VARCHAR(255) NOT NULL UNIQUE)")

        cursor.execute("CREATE TABLE IF NOT EXISTS links (links_ID INT AUTO_INCREMENT PRIMARY KEY, sleutelw_ID INT"
                       " NOT NULL,FOREIGN KEY fk_sleutelw_ID(sleutelw_ID) REFERENCES sleutelwoorden(sleutelw_ID),"
                       " titel VARCHAR(255) NOT NULL UNIQUE, link VARCHAR(255))")

        cursor.execute("CREATE TABLE IF NOT EXISTS spaces (space_ID INT PRIMARY KEY,"
                       " link_id INT NOT NULL, FOREIGN KEY fk_link_ID_space(link_id) REFERENCES links(links_ID),"
                       " type VARCHAR(255))")

        cursor.execute("CREATE TABLE IF NOT EXISTS pages (page_ID INT PRIMARY KEY,"
                       " link_id INT NOT NULL, FOREIGN KEY fk_link_ID_page(link_id) REFERENCES links(links_ID), "
                       "space_id INT NOT NULL, FOREIGN KEY fk_space_ID_page(space_id) REFERENCES spaces(space_ID),"
                       "type VARCHAR(255))")

        cursor.execute("SHOW TABLES")
        for x in cursor:
            print("Table: " + str(x[0]) + " was created")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed create tables {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def update_link(link, titel):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "UPDATE links SET link = %s WHERE titel = %s"
        val = (link, titel)

        cursor.execute(sql, val)
        mydb.commit()
        print("The link of " + titel + "is updated")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to update MySQL table links {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


# insert
def insert_in_to_antwoorden(antwoord):
    try:
        global cursor
        cursor = mydb.cursor()
        sql_insert_query = """ INSERT INTO `antwoorden`
                            (`antwoord_ID`,`antwoord`) VALUES (%s,%s)"""
        insert_tuple = (0, antwoord)
        cursor.execute(sql_insert_query, insert_tuple)
        mydb.commit()
        print("Record inserted successfully into table antwoorden")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table antwoorden {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_links(titel, link):
    try:
        global cursor
        cursor = mydb.cursor()
        sql_insert_query = "INSERT INTO links (links_ID,sleutelw_ID, titel, link) " \
                           "VALUES (%s, (SELECT sleutelw_ID FROM sleutelwoorden WHERE sleutel='documentatie'), %s,%s)"
        insert_tuple = (0, titel, link)
        cursor.execute(sql_insert_query, insert_tuple)
        mydb.commit()
        print("Record inserted successfully into table links")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table links {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_sleutels(antID, sleutel):
    try:
        global cursor
        cursor = mydb.cursor()
        sql_insert_query = """ INSERT INTO sleutelwoorden (sleutelw_ID, antwoord_ID, sleutel) 
                                VALUES (%s,%s,%s) """
        insert_tuple = (0, antID, sleutel)
        cursor.execute(sql_insert_query, insert_tuple)
        mydb.commit()
        print("Record inserted successfully into table sleutelwoorden")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table sleutelwoorden{}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_spaces(spaceID, titel,type):
    try:
        global cursor
        cursor = mydb.cursor()
        sql_insert_query = """ INSERT INTO spaces (space_ID, link_id, type) 
                                VALUES (%s,(SELECT links_ID FROM links WHERE titel=%s),%s) """
        insert_tuple = (spaceID, titel, type)
        cursor.execute(sql_insert_query, insert_tuple)
        mydb.commit()
        print("Record inserted successfully into table spaces")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table spaces{}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_pages(pagesID, spaceID, titel,type):
    try:
        global cursor
        cursor = mydb.cursor()
        sql_insert_query = """ INSERT INTO pages (page_ID, link_id,space_id,type) 
                                VALUES (%s,(SELECT links_ID FROM links WHERE titel=%s),%s,%s) """
        insert_tuple = (pagesID, titel, spaceID, type)
        cursor.execute(sql_insert_query, insert_tuple)
        mydb.commit()
        print("Record inserted successfully into table pages")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table pages{}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


# get
def get_sleutels():
    try:
        global cursor
        cursor = mydb.cursor()

        cursor.execute("SELECT sleutel FROM sleutelwoorden")
        result = cursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get sleutel from MSQL table sleutels {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_titels():
    try:
        global cursor
        cursor = mydb.cursor()

        cursor.execute("SELECT titel FROM links")
        result = cursor.fetchall()
        return db_to_array(result)

    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get titel from MYSQL table links {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_links():
    try:
        global cursor
        cursor = mydb.cursor()
        cursor.execute("SELECT link FROM links")
        result = cursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get links from MYSQL table links {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_titel_en_links():
    teller = 0
    titelsenlinks = ""
    while teller <= get_titels().__len__() - 1:
        titelsenlinks += (get_titels()[teller] + " - " + get_links()[teller] + "\n")
        teller += 1
    return titelsenlinks


def get_antwoorden():
    try:
        global cursor
        cursor = mydb.cursor()
        cursor.execute("SELECT antwoord FROM antwoorden")
        result = cursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get antwoorden from MySQL table antwoorden {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_antwoord(vraag):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "SELECT antwoord from antwoorden WHERE antwoord_ID = " \
              "(SELECT antwoord_ID from sleutelwoorden WHERE sleutel = LOWER(%s))"
        sleutel = (vraag,)

        cursor.execute(sql, sleutel)
        result = cursor.fetchone()[0]
        return result

    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get antwoord from MySQL table antwoorden {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_link(titel, sleutel):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "SELECT link FROM links WHERE LOWER(titel) = LOWER(%s) and sleutelw_ID = " \
              "(select sleutelw_ID from sleutelwoorden where sleutel = LOWER(%s))"
        sleutel = (titel, sleutel)
        cursor.execute(sql, sleutel)
        url = cursor.fetchone()
        if url is not None:
            result = url[0]
            print("gevonden in de database")
        elif url is None:
            for i in get_confluence_pages():
                if i.titel == titel:
                    insert_in_to_links(i.titel, os.getenv('CONFLUENCE_URL') + i.url)
                    insert_in_to_pages(i.id, i.spaceid, i.titel, i.type)
                    result = os.getenv('CONFLUENCE_URL') + i.url
                    print("gevonden in confluence")
                    break
                else:
                    print("page not found 404")
                    result = ""

        return result
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get link from MSQL table links {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_link2(titel, sleutel, space):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "SELECT link FROM links " \
              "inner join sleutelwoorden on links.sleutelw_ID = sleutelwoorden.sleutelw_ID " \
              "inner join spaces on links.links_ID = spaces.link_id " \
              "inner join pages on pages.space_id = spaces.space_ID " \
              "WHERE LOWER(links.titel) = LOWER(%s) and sleutelwoorden.sleutel = LOWER(%s) and pages.space_id = %s "
        sleutel = (titel, sleutel, space)
        cursor.execute(sql, sleutel)
        url = cursor.fetchone()
        if url is not None:
            result = url[0]
            print("gevonden in de database")
        elif url is None:
            for i in get_confluence_pages():
                if i.titel == titel:
                    insert_in_to_links(i.titel, os.getenv('CONFLUENCE_URL') + i.url)
                    insert_in_to_pages(i.id, i.spaceid, i.titel, i.type)
                    result = os.getenv('CONFLUENCE_URL') + i.url
                    print("gevonden in confluence")
                    break
                else:
                    print("page not found 404")
                    result = ""

        return result
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get link from MSQL table links {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_spaces():
    try:
        global cursor
        cursor = mydb.cursor()

        cursor.execute("SELECT space_ID, titel, link, type FROM spaces"
                       " INNER JOIN links ON spaces.link_id = links.links_ID")
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get space from MYSQL table spaces {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_pages():
    try:
        global cursor
        cursor = mydb.cursor()

        cursor.execute("SELECT p.page_ID, l.titel,l.link,p.type, p.space_id FROM pages"
                       " p INNER JOIN links l ON p.link_id = l.links_ID")
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get page from MYSQL table pages {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


# hulp functie

# to array methode
def db_to_array(cursor_execut_fa):
    arr = []
    teller = 0
    while teller <= cursor_execut_fa.__len__() - 1:
        arr.append(cursor_execut_fa[teller][0])
        teller += 1
    return arr


def vullen():
    # insert values
    insert_in_to_antwoorden("hallo, hoe gaat het?")
    insert_in_to_antwoorden("hulp nodig?")
    insert_in_to_antwoorden("De status van de server is \"Online\".")
    insert_in_to_antwoorden("De server staat aan")
    insert_in_to_antwoorden("De server staat uit")
    insert_in_to_antwoorden("hier is de lijst van de keywoorden:")
    insert_in_to_antwoorden(" documentatie vind je op volgende link: ")
    insert_in_to_antwoorden(" configuratie vind je op volgende link: ")

    insert_in_to_sleutels(1, "hallo")
    insert_in_to_sleutels(2, "help")
    insert_in_to_sleutels(3, "status")
    insert_in_to_sleutels(6, "lijst")
    insert_in_to_sleutels(4, "aan")
    insert_in_to_sleutels(5, "uit")
    insert_in_to_sleutels(7, "documentatie")
    insert_in_to_sleutels(8, "confugureer")

    insert_in_to_links("python", "http://tdc-www.harvard.edu/Python.pdf")
    insert_in_to_links("ecs", "https://docs.aws.amazon.com/ecs/index.html#lang/en_us")
    insert_in_to_links("ec2", "https://docs.aws.amazon.com/ec2/index.html#lang/en_us")
    insert_in_to_links("ecr", "https://docs.aws.amazon.com/ecr/index.html#lang/en_us")
    insert_in_to_links("s3", "https://docs.aws.amazon.com/s3/index.html#lang/en_us")
    insert_in_to_links("codebuild", "https://docs.aws.amazon.com/codebuild/index.html#lang/en_us")
    insert_in_to_links("codepipeline", "https://docs.aws.amazon.com/codepipeline/index.html#lang/en_us")
    insert_in_to_links("docker", "https://docs.docker.com/")
    insert_in_to_links("cloudformation", "https://docs.aws.amazon.com/cloudformation/index.html")
    insert_in_to_links("terraform", "https://www.terraform.io/intro/index.html")
    insert_in_to_links("kubernetes", "https://kubernetes.io/docs/home/")
    insert_in_to_links("jenkins", "https://jenkins.io/doc/")

# confluence


def zoek_page(space, titel):
    p = confluence.get_all_pages_from_space(space=space.upper(), start=0, limit=500)
    link = ""
    for i in p:
        if titel.lower() == str.lower(i['title']):
            link = i['_links']['webui']
    print(link)


def get_confluence_spaces():
    p = confluence.get_all_spaces(start=0, limit=500)
    links = []
    for j in p:
        pa = page.Page(j['id'], j['key'], j['_links']['webui'], j['type'])
        links.append(pa)
    return links


def get_confluence_pages():
    links = []
    for i in get_confluence_spaces():
        p = confluence.get_all_pages_from_space(space=i.titel, start=0, limit=500)
        for j in p:
            pa = page.Page(j['id'], j['title'], j['_links']['webui'], j['type'])
            pa.set_space_id(i.id)
            links.append(pa)
    return links


def spaces_vullen():
    for space in get_confluence_spaces():
        insert_in_to_links(space.titel, os.getenv('CONFLUENCE_URL')+space.url)
        insert_in_to_spaces(space.id, space.titel, space.type)


def pages_vullen():
    for page in get_confluence_pages():
        insert_in_to_links(page.titel, os.getenv('CONFLUENCE_URL')+page.url)
        insert_in_to_pages(page.id, page.spaceid, page.titel, page.type)


def check_if_populated():
    create_tables()
    try:
        global cursor
        tables = []
        cursortables = mydb.cursor()
        cursorcount = mydb.cursor()
        cursortables.execute("SHOW TABLES")
        for table in cursortables:
            tables.append(table[0])
        for item in tables:
            sql = "SELECT * FROM " + item
            cursorcount.execute(sql)
            cursorcount.fetchall()
            result = cursorcount.rowcount
            print(str(result) + " "+str(item))
            if result is None:
                if item == "pages":
                    pages_vullen()
                elif item == "spaces":
                    spaces_vullen()
                else:
                    vullen()
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to check if MSQL database is populated {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


# check_if_populated()
def url_check():
    try:
        for link in get_spaces():
            responce = requests.get('http://mple.com')
            print(responce.status_code)
            print(link)
    except requests.exceptions.ConnectionError as e:
        print(e.strerror)


# url_check()

cursortest = mydb.cursor()
sql1 = "SELECT link FROM links " \
      "inner join sleutelwoorden on links.sleutelw_ID = sleutelwoorden.sleutelw_ID " \
      "inner join spaces on links.links_ID = spaces.link_id " \
      "inner join pages on pages.space_id = spaces.space_ID " \
      "WHERE LOWER(links.titel) = LOWER(%s) and sleutelwoorden.sleutel = LOWER(%s) and pages.space_id = %s "
sleutel1 = ("Gluo", "documentatie", "71270433")
cursortest.execute(sql1, sleutel1)
url1 = cursortest.fetchone()
print(url1)
