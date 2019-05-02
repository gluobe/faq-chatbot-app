# import van modulen
import sqlite3
import mysql.connector
import os

mydb = mysql.connector.connect(
  host="faqchatbot.cluster-cq7bczewmzvu.eu-west-2.rds.amazonaws.com",
  user="abdul",
  passwd=os.getenv('DB_PASSWORD')
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")

print(mydb.is_connected().__str__())
'''
# Aanmaak database zet de thread uit. De databank woord in een andere threat gemaakt dan in de threat dat de code
# uitgevoert zal worden
conn = sqlite3.connect('faq_chat.db', check_same_thread=False)

cursor = conn.cursor()
# Aanmaak tabellen, na het aanmaken moeten deze lijnen weg
cursor.execute("""CREATE TABLE IF NOT EXISTS antwoorden (
                antwoord_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                antwoord TEXT
                )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS sleutelwoorden (
                sleutelw_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                antwoord_ID INTEGER REFERENCES antwoorden(antwoord_ID),
                sleutel TEXT NOT NULL UNIQUE
                );""")

cursor.execute("""CREATE TABLE IF NOT EXISTS links (
                links_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                sleutelw_ID INTEGER REFERENCES sleutelwoorden(sleutelw_ID),
                titel TEXT,
                link TEXT
                )""")


# commit de veranderingen
conn.commit()

# instellen wat we terug krijgen
conn.text_factory = str


# crud functies
# update
def update_link(link, titel):
    with conn:
        cursor.execute("""UPDATE links set link = :link WHere titel = :titel""",
                       {'link': link, 'titel': titel})


# insert
def insert_in_to_antwoorden(antwoord):
    with conn:
        cursor.execute("INSERT INTO antwoorden (antwoord) VALUES (:antwoord)", {'antwoord': antwoord})


def insert_in_to_links(sleutelid, titel, link):
    with conn:
        cursor.execute("INSERT INTO links (sleutelw_ID, titel, link) VALUES (:sleutelw_ID, :titel, :link)", {
            'sleutelw_ID': sleutelid, 'titel': titel, 'link': link})


def insert_in_to_sleutels(antID, sleutel):
    with conn:
        cursor.execute("INSERT INTO sleutelwoorden (antwoord_ID, sleutel) VALUES (:antwoord_ID, "
                       ":sleutel)", {'antwoord_ID': antID, 'sleutel': sleutel})


# get
def get_sleutels():
    return db_to_array(cursor.execute("SELECT sleutel from sleutelwoorden").fetchall())


def get_titels():
    return db_to_array(cursor.execute("SELECT titel from links").fetchall())


def get_links():
    return db_to_array(cursor.execute("SELECT link FROM links").fetchall())


def get_titel_en_links():
    teller = 0
    titelsenlinks = ""
    while teller <= get_titels().__len__() - 1:
        titelsenlinks += (get_titels()[teller] + " - " + get_links()[teller] + "\n")
        teller += 1
    return titelsenlinks


def get_antwoorden():
    return db_to_array(cursor.execute("SELECT antwoord FROM antwoorden").fetchall())


def get_antwoord(vraag):
    return cursor.execute("SELECT antwoord from antwoorden WHERE antwoord_ID = (SELECT antwoord_ID from sleutelwoorden"
                          " WHERE sleutel = :sleutel)", {'sleutel': vraag}).fetchone()[0]


def get_link(titel,sleutel):
    return cursor.execute("SELECT link FROM links WHERE titel = :titel and sleutelw_ID = (select sleutelw_ID from "
                          "sleutelwoorden where sleutel = :sleutel)", {'titel': titel.lower(), 'sleutel': sleutel.lower()}).fetchone()[0]


# help functies

# to array methode
def db_to_array(cursor_execut_fa):
    arr = []
    teller = 0
    while teller <= cursor_execut_fa.__len__() - 1:
        arr.append(cursor_execut_fa[teller][0])
        teller += 1
    return arr


def vullen():
    global ant
    if(db_to_array(cursor.execute("SELECT count(*) from sleutelwoorden").fetchall())[0]) == 0:
        # insert values
        insert_in_to_antwoorden("hallo, hoe gaat het?")
        insert_in_to_antwoorden("hulp nodig?")
        insert_in_to_antwoorden("De status van de server is \"Online\".")
        insert_in_to_antwoorden("De server staat aan")
        insert_in_to_antwoorden("De server staat uit")
        insert_in_to_antwoorden("hier is de lijst van de keywoorden:")
        insert_in_to_antwoorden(" documentatie vind je op volgende link: ")

        insert_in_to_sleutels(1, "hallo")
        insert_in_to_sleutels(2, "help")
        insert_in_to_sleutels(3, "status")
        insert_in_to_sleutels(6, "lijst")
        insert_in_to_sleutels(4, "aan")
        insert_in_to_sleutels(5, "uit")
        insert_in_to_sleutels(7, "documentatie")
        insert_in_to_sleutels(8, "confugureer")

        insert_in_to_links(7, "python", "http://tdc-www.harvard.edu/Python.pdf")
        insert_in_to_links(7, "ecs", "https://docs.aws.amazon.com/ecs/index.html#lang/en_us")
        insert_in_to_links(7, "ec2", "https://docs.aws.amazon.com/ec2/index.html#lang/en_us")
        insert_in_to_links(7, "ecr", "https://docs.aws.amazon.com/ecr/index.html#lang/en_us")
        insert_in_to_links(7, "s3", "https://docs.aws.amazon.com/s3/index.html#lang/en_us")
        insert_in_to_links(7, "codebuild", "https://docs.aws.amazon.com/codebuild/index.html#lang/en_us")
        insert_in_to_links(7, "codepipeline", "https://docs.aws.amazon.com/codepipeline/index.html#lang/en_us")
        insert_in_to_links(7, "docker", "https://docs.docker.com/")
        insert_in_to_links(7, "cloudformation", "https://docs.aws.amazon.com/cloudformation/index.html")
        insert_in_to_links(7, "terraform", "https://www.terraform.io/intro/index.html")
        insert_in_to_links(7, "kubernetes", "https://kubernetes.io/docs/home/")
        insert_in_to_links(7, "jenkins", "https://jenkins.io/doc/")
        ant = True
    else:
        ant = False
    return ant


vullen()
'''
