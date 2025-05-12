from util.db import TinyInterface
import uuid
import os
import datetime

db = TinyInterface(db_path='data/file_metadata.json', table_name='files')

def register_file(path):
    filename = os.path.basename(path)
    record = db.get(filename=filename)
    if record:
        return record[0]["eid"]

    stat = os.stat(path)
    new_record = {
        "eid": str(uuid.uuid4()),
        "filename": filename,
        "path": path,
        "tags": [],
        "size": stat.st_size,
        "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "last_modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
    }
    db.add(new_record)
    return new_record["eid"]

def get_file_by_eid(eid):
    return db.get(eid=eid)[0] if db.get(eid=eid) else None

def update_tags(eid, tags):
    db.update({"tags": tags}, eid=eid)

def add_tag(eid, tag):
    file = get_file_by_eid(eid)
    if file and tag not in file["tags"]:
        file["tags"].append(tag)
        update_tags(eid, file["tags"])

def remove_tag(eid, tag):
    file = get_file_by_eid(eid)
    if file and tag in file["tags"]:
        file["tags"].remove(tag)
        update_tags(eid, file["tags"])

def list_files():
    return db.all()

def get_file_by_filename(filename):
    record = db.get(filename=filename)
    return record[0] if record else None