import sqlite3
import json
from models import Category

def get_all_categories():
    """This function queries the database for all categories, converts each row into an Category instance, converts the list to JSON & responds to the client request."""
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        ORDER BY label ASC
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            category = Category(row['id'], row['label'])

            categories.append(category.__dict__)

    return json.dumps(categories)

def get_single_category(id):
    """This function queries the database for one category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        WHERE c.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        category = Category(data['id'], data['label'])

        return json.dumps(category.__dict__)

def create_category(new_category):
    """This function inserts a new category into the database."""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            ( label )
        VALUES
            ( ? );
        """, (new_category['label'], ))

        id = db_cursor.lastrowid

        new_category['id'] = id

    return json.dumps(new_category)

def update_category(id, new_category):
    """This function updates the category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
            SET
                label = ?
        WHERE id = ?
        """, (new_category['label'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def delete_category(id):
    """This function deletes a single category/row"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """, (id, ))
