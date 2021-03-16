import sys
import sqlite3
import os
from ..definitions import DATABASE_PATH


"""
    Module controlling creation, deletion and updating of data using an SQLite database.

    Websites are each mapped to a unique ID used to maintain a record of URL which have been previously 
    parsed for a specific website.

"""

connection = None  # Active database connection


def get_connection():
    global connection
    if not connection:
        connection = sqlite3.connect(DATABASE_PATH)
    return connection


def close_connection():
    connection.close()


def create_tables():
    """
        Generates tables using a SQL queries
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE Website
                     (website_id INTEGER PRIMARY KEY, name text)''')

    cursor.execute('CREATE TABLE Url_Journal (url_id INTEGER PRIMARY KEY, url text, website_id,'
                   'FOREIGN KEY (website_id) REFERENCES Website (website_id))')

    conn.commit()
    cursor.close()


def query_database(query: str):
    """ Executes a supplied  SQL query
    :param query: SQL Query
    :return: Resulting rows
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    results = cursor.execute(query)
    return results.fetchall()


def get_website_id(website_name: str) -> int:
    """ Get a website ID given a website name, if no ID exists for a website then a new ID is assigned & logged.
    :param website_name:
    :return: Integer ID
    """
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute(f"SELECT * FROM Website WHERE name='{website_name}'").fetchall()

    if not len(rows):
        cursor.execute(f"INSERT INTO Website (name) VALUES ('{website_name}')")
        rows = cursor.execute(f"SELECT * FROM Website WHERE name='{website_name}'").fetchall()
        conn.commit()

    return int(rows[0][0])


def get_listings(website_id) -> set:
    return set([r[1] for r in query_database(f'SELECT * FROM listing_journal WHERE website_id={website_id}')])


def add_listings(website_id, listing) -> str:
    """
        Adds a listing record for a specific Website to the application database, returning
        the ID of the newly appended record.

    :param website_id: Website ID the record is being added for
    :param listing:
    :return: The ID of the added URL
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO listing_journal (website_id, listing) VALUES  ({website_id}, '{listing}')")
    conn.commit()

    return cursor.execute(f"SELECT * FROM listing_journal WHERE listing='{listing}'").fetchall()[0][0]


def add_banned_urls(website_id, url, is_pagination) -> str:
    """
        Adds a listing record for a specific Website to the application database, returning
        the ID of the newly appended record.

    :param website_id: Website ID the record is being added for
    :param url:
    :param is_pagination: Specify whether banned URL is pagination or a data URL
    :return: The ID of the added URL
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO Banned_Url_Journal (website_id, url, is_pagination) VALUES  ({website_id}, '{url}', {is_pagination})")
    conn.commit()

    return cursor.execute(f"SELECT * FROM Banned_Url_Journal WHERE url='{url}'").fetchall()[0][0]

"""
    Executing this module as the point of entry re-creates the database.
"""

if __name__ == '__main__':
    create_tables()
