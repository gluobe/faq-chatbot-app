# import van modulen
import mysql.connector
import os

mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  passwd=os.getenv('DB_PASSWORD'),
  database="faqchat"
)


try:
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS faqchat")
except mysql.connector.Error as errors:
    mydb.rollback()
    print("Failed to insert into MySQL table sleutels {}".format(errors))
finally:
    # closing database connection.
    cursor.close()
    print("MySQL connection is closed")

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
                       " titel VARCHAR(255), link VARCHAR(255))")

        print("Tables are created")
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
        print("Failed to opdate MySQL table links {}".format(error))
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


def insert_in_to_links(sleutelid, titel, link):
    try:
        global cursor
        cursor = mydb.cursor()
        sql_insert_query = "INSERT INTO `links` (`links_ID`,`sleutelw_ID`, `titel`, `link`) VALUES (%s, %s, %s,%s)"
        insert_tuple = (0, sleutelid, titel, link)
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


# get
def get_sleutels():
    try:
        global cursor
        cursor = mydb.cursor()

        cursor.execute("SELECT sleutel FROM sleutelwoorden")
        result = mycursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table sleutels {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_titels():
    try:
        global cursor
        cursor = mydb.cursor()

        cursor.execute("SELECT titel FROM links")
        result = mycursor.fetchall()
        return db_to_array(result)

    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table sleutels {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_links():
    try:
        global cursor
        cursor = mydb.cursor()
        cursor.execute("SELECT link FROM links")
        result = mycursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table sleutels {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_titel_en_links():
    try:
        teller = 0
        titelsenlinks = ""
        while teller <= get_titels().__len__() - 1:
            titelsenlinks += (get_titels()[teller] + " - " + get_links()[teller] + "\n")
            teller += 1
        return titelsenlinks
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table sleutels {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_antwoorden():
    try:
        global cursor
        cursor = mydb.cursor()
        cursor.execute("SELECT antwoord FROM antwoorden")
        result = mycursor.fetchall()
        return db_to_array(result)
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table sleutels {}".format(error))
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
        result = mycursor.fetchone()[0]
        return result

    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table sleutels {}".format(error))
    finally:
        # closing database connection.
        cursor.close()
        print("MySQL connection is closed")


def get_link(titel, sleutel):
    try:
        global cursor
        cursor = mydb.cursor()
        sql = "SELECT link FROM links WHERE titel = LOWER(%s) and sleutelw_ID = " \
              "(select sleutelw_ID from sleutelwoorden where sleutel = LOWER(%s))"
        sleutel = (titel, sleutel,)

        cursor.execute(sql, sleutel)
        result = mycursor.fetchone()[0]
        return result
    except mysql.connector.Error as error:
        mydb.rollback()
        print("Failed to insert into MySQL table sleutels {}".format(error))
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
