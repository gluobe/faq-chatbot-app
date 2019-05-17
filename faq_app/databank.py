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
        cursor.execute("CREATE TABLE IF NOT EXISTS answers (answer_ID INT AUTO_INCREMENT  PRIMARY KEY, "
                       "answer VARCHAR(255))")

        cursor.execute("CREATE TABLE IF NOT EXISTS links (link_ID INT AUTO_INCREMENT PRIMARY KEY, "
                       "link VARCHAR(255) NOT NULL UNIQUE)")

        cursor.execute("CREATE TABLE IF NOT EXISTS keywords (keyword_ID INT AUTO_INCREMENT PRIMARY KEY, "
                       "answer_ID INT NOT NULL,FOREIGN KEY fk_answer_ID(answer_ID) REFERENCES "
                       "answers(answer_ID), link_ID INT, FOREIGN KEY fk_link_ID_keyword(link_ID) "
                       "REFERENCES links(link_ID), keyword VARCHAR(255) NOT NULL UNIQUE)")

        cursor.execute("CREATE TABLE IF NOT EXISTS pages (page_ID INT PRIMARY KEY,"
                       " space_ID INT, FOREIGN KEY fk_page_ID_page(space_ID) REFERENCES pages(page_ID),"
                       " link_ID INT, FOREIGN KEY fk_link_ID_page(link_ID) REFERENCES links(link_ID),"
                       " title VARCHAR(255), url VARCHAR(255), type VARCHAR(255))")

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


def update_link(link, title):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "UPDATE links SET link = %s WHERE title = %s"
        val = (link, title)

        cursor.execute(sql, val)
        mydb.commit()
        print("The link of " + title + "is updated")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to update MySQL table links {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


# insert
def insert_in_to_answers(answer):
    try:
        global cursor
        cursor = mydb.cursor()
        sql_insert_query = " INSERT INTO answers (answer_ID, answer) VALUES (%s,%s)"
        insert_tuple = (0, answer)
        cursor.execute(sql_insert_query, insert_tuple)
        mydb.commit()
        print("Record inserted successfully into table answers")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table answers {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_links(link):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "INSERT INTO links (link_ID, link) VALUES (%s, %s)"
        val = (0, link)
        cursor.execute(sql, val)
        mydb.commit()
        print("Record inserted successfully into table links")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table links {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_keywords(antID, keyword):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "INSERT INTO keywords (keyword_ID, answer_ID, keyword) VALUES (%s,%s,%s)"
        val = (0, antID, keyword)
        cursor.execute(sql, val)
        mydb.commit()
        print("Record inserted successfully into table keywords")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table keywords{}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_pages(pagesid, linkid, title, url, type):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "INSERT INTO pages (page_ID, link_ID, title, url, type)VALUES (%s,%s,%s,%s,%s)"
        val = (pagesid, linkid, title, url, type)
        cursor.execute(sql, val)
        mydb.commit()
        print("Record inserted successfully into table pages")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table pages{}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_keywords_li(antID, linkID, keyword):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "INSERT INTO keywords (keyword_ID, answer_ID, link_ID, keyword) VALUES (%s,%s,%s,%s)"
        val = (0, antID, linkID, keyword)
        cursor.execute(sql, val)
        mydb.commit()
        print("Record inserted successfully into table keywords")
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table keywords{}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def insert_in_to_pages_sp(pagesid, spaceid, linkid, title, url, type):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "INSERT INTO pages (page_ID, space_ID, link_ID, title, url, type)VALUES (%s,%s,%s,%s,%s,%s)"
        val = (pagesid, spaceid, linkid, title, url, type)
        cursor.execute(sql, val)
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
def get_keywords():
    try:
        global cursor
        cursor = mydb.cursor()
        cursor.execute("SELECT keyword FROM keywords")
        result = cursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get keyword from MSQL table keywords {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_titles():
    try:
        global cursor
        cursor = mydb.cursor()

        cursor.execute("SELECT title FROM pages")
        result = cursor.fetchall()
        return db_to_array(result)

    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get title from MYSQL table pages {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_links():
    try:
        global cursor
        cursor = mydb.cursor()
        cursor.execute("SELECT url FROM pages")
        result = cursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get links from MYSQL table pages {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_title_en_links():
    teller = 0
    titlesenlinks = ""
    while teller <= get_titles().__len__() - 1:
        titlesenlinks += (get_titles()[teller] + " - " + get_links()[teller] + "\n")
        teller += 1
    return titlesenlinks


def get_answers():
    try:
        global cursor
        cursor = mydb.cursor()
        cursor.execute("SELECT answer FROM answers")
        result = cursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get answer from MySQL table answers {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_answer(question):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "SELECT answer from answers " \
              "INNER JOIN keywords ON answers.answer_ID = keywords.answer_ID " \
              "WHERE LOWER(keyword) = LOWER(%s)"
        val = (question,)
        cursor.execute(sql, val)
        result = cursor.fetchone()[0]
        return result

    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get answer from MySQL table answers {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_link(title, keyword):
    try:
        global cursor
        global s
        result = []
        s = ""
        cursor = mydb.cursor()
        sql = "SELECT url FROM pages " \
              "INNER JOIN links ON pages.link_ID = links.link_ID " \
              "INNER JOIN keywords ON links.link_ID = keywords.link_ID " \
              "WHERE LOWER(title) = LOWER(%s) and LOWER(keyword) = LOWER(%s)"
        val = (title, keyword)
        cursor.execute(sql, val)
        url = cursor.fetchall()
        if url is not None:
            for i in url:
                result.append(i)
                s = s + "\n" + str(i[0])

            print("gevonden in de database")
        elif url is None:
            for i in get_confluence_pages():
                if i.title == title:
                    insert_in_to_pages_sp(i.id, i.spaceid, 1, i.title, os.getenv('CONFLUENCE_URL') + i.url, i.type)
                    s = os.getenv('CONFLUENCE_URL') + i.url
                    print("gevonden in confluence")
                    break
                else:
                    print("page not found 404")
                    s = ""

        return s
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get link from MSQL table pages {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_link_sp(title, keyword, space):
    try:
        global cursor
        result = ""
        cursor = mydb.cursor()
        sql = "SELECT url FROM pages " \
              "INNER JOIN links ON pages.link_ID = links.link_ID " \
              "INNER JOIN keywords ON links.link_ID = keywords.link_ID " \
              "WHERE LOWER(title) = LOWER(%s) AND LOWER(keyword) = LOWER(%s) " \
              "AND pages.space_id = %s AND pages.link_ID = links.link_ID"
        val = (title, keyword, space)
        cursor.execute(sql, val)
        url = cursor.fetchone()
        if url is not None:
            result = url[0]
            print("gevonden in de database")
        elif url is None:
            for i in get_confluence_pages():
                if i.title == title:
                    insert_in_to_pages_sp(i.id, i.spaceid, 1, i.title, os.getenv('CONFLUENCE_URL') + i.url, i.type)
                    result = os.getenv('CONFLUENCE_URL') + i.url
                    print("gevonden in confluence")
                    break
                else:
                    print("page not found 404")
                    result = ""
        return result
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get link from MSQL table pages {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_space_id(spacename):
    try:
        global cursor
        cursor = mydb.cursor()

        spl = "SELECT page_ID FROM pages WHERE LOWER(title) = LOWER(%s) AND type = 'global'"
        val = (spacename, )
        cursor.execute(spl, val)
        result = cursor.fetchone()[0]
        return result
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to get space_ID from MYSQL table spaces {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_pages():
    try:
        global cursor
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM pages")
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
    insert_in_to_answers("hallo, hoe gaat het?")
    insert_in_to_answers("hulp nodig?")
    insert_in_to_answers("De status van de server is \"Online\".")
    insert_in_to_answers("De server staat aan")
    insert_in_to_answers("De server staat uit")
    insert_in_to_answers("hier is de lijst van de keywoorden:")
    insert_in_to_answers(" documentatie vind je op volgende link: ")
    insert_in_to_answers(" configuratie vind je op volgende link: ")

    insert_in_to_links("documentatie")
    insert_in_to_links("confugureer")

    insert_in_to_keywords(1, "hallo")
    insert_in_to_keywords(2, "help")
    insert_in_to_keywords(3, "status")
    insert_in_to_keywords(6, "lijst")
    insert_in_to_keywords(4, "aan")
    insert_in_to_keywords(5, "uit")
    insert_in_to_keywords_li(7, 1, "documentatie")
    insert_in_to_keywords_li(8, 2, "confugureer")

    insert_in_to_pages(1, 1, "python", "http://tdc-www.harvard.edu/Python.pdf", "page")
    insert_in_to_pages(2, 1, "ecs", "https://docs.aws.amazon.com/ec2/index.html#lang/en_us", "page")
    insert_in_to_pages(3, 1, "ec2", "https://docs.aws.amazon.com/ec2/index.html#lang/en_us", "page")
    insert_in_to_pages(4, 1, "ecr", "https://docs.aws.amazon.com/ecr/index.html#lang/en_us", "page")
    insert_in_to_pages(5, 1, "s3", "https://docs.aws.amazon.com/s3/index.html#lang/en_us", "page")
    insert_in_to_pages(6, 1, "codebuild", "https://docs.aws.amazon.com/codebuild/index.html#lang/en_us", "page")
    insert_in_to_pages(7, 1, "codepipeline", "https://docs.aws.amazon.com/codepipeline/index.html#lang/en_us", "page")
    insert_in_to_pages(8, 1, "cloudformation", "https://docs.aws.amazon.com/cloudformation/index.html", "page")
    insert_in_to_pages(9, 1, "terraform",  "https://www.terraform.io/intro/index.html", "page")
    insert_in_to_pages(10, 1, "kubernetes", "http://tdc-www.harvard.edu/Python.pdf", "page")
    insert_in_to_pages(11, 1, "jenkins", "https://jenkins.io/doc/", "page")
    insert_in_to_pages(12, 1, "docker", "https://docs.docker.com/", "page")

# confluence


def zoek_page(space, title):
    p = confluence.get_all_pages_from_space(space=space.upper(), start=0, limit=500)
    link = ""
    for i in p:
        if title.lower() == str.lower(i['title']):
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
        p = confluence.get_all_pages_from_space(space=i.title, start=0, limit=500)
        for j in p:
            pa = page.Page(j['id'], j['title'], j['_links']['webui'], j['type'])
            pa.set_space_id(i.id)
            links.append(pa)
    return links


def spaces_vullen():
    for space in get_confluence_spaces():
        insert_in_to_pages(space.id, 1, space.title, os.getenv('CONFLUENCE_URL')+space.url, space.type)


def pages_vullen():
    for page in get_confluence_pages():
        insert_in_to_pages_sp(page.id, page.spaceid, 1, page.title, os.getenv('CONFLUENCE_URL')+page.url, page.type)


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
        pass
    except requests.exceptions.ConnectionError as e:
        print(e.strerror)
