from hashlib import new
import sqlite3
import json

from models import Tag

TAGS = [
    {
        "id": 1,
        "label": "JavaScript"
    },
    {
        "id": 2,
        "label": "Python"
    }
]
    
def get_all_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        """)
        
        tags = []
        
        data = db_cursor.fetchall()
        
        for row in data:
            tag = Tag(row["id"], row["label"])
            tags.append(tag.__dict__)
            
        return json.dumps(tags)
    
def get_single_tag(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        WHERE t.id = ?
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        tag = Tag(data["id"], data["label"])
        
        return json.dumps(tag.__dict__)
    
def create_tag(new_tag):
    # max_id = TAGS[-1]["id"]
    # new_id = max_id + 1
    # tag["id"] = new_id
    # TAGS.append(tag)
    # return tag
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Tags (label)
        VALUES (?)
        """, (new_tag["label"], ))
        
        id = db_cursor.lastrowid
        
        new_tag["id"] = id
        
    return json.dumps(new_tag)

def update_tag(id, new_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE Tags
            SET 
                label = ?
        WHERE id = ?
        """, (new_tag["label"], id))
        
        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else:
        return True
    
def do_PUT(self):
    content_len = int(self.headers.get('content-length', 0))
    post_body = self.rfile.read(content_len)
    post_body = json.loads(post_body)
    
    (resource, id) = self.parse_url(self.path)
    
    success = False
    
    if resource == "tags":
        success = update_tag(id, post_body)
        
    if success:
        self._set_headers(204)
    else:
        self._set_headers(404)
        
    self.wfile.write("".encode())
    
def delete_tag(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM Tags
        WHERE id = ?
        """, (id, ))