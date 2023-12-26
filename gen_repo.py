import sqlite3,json
from pathlib import Path

def gen_repo(cursor:sqlite3.Cursor,bucket_name:str,bucket_path:Path):

    for file in bucket_path.glob("*.json"):
        with open(file,"r",encoding='utf-8') as f:
            manifest = json.load(f)
            package = file.stem
            version = manifest.get("version")
            if manifest.get("url") != None:
                url = manifest.get("url")
            else:
                url = manifest.get("architecture").get("64bit").get("url")
                    
            if isinstance(url,str):
                sql = f'INSERT INTO {bucket_name} VALUES ("{package}","{version}","{str(url)}")'
                cursor.execute(sql)

db = sqlite3.connect('repo.db')
c = db.cursor()
db.execute('''CREATE TABLE Main (PACKAGE TEXT,VERSION TEXT,URL TEXT)''')
db.execute('''CREATE TABLE Extras (PACKAGE TEXT,VERSION TEXT,URL TEXT)''')

current_dir = Path(__file__).absolute().parent
gen_repo(c,"Main",current_dir.joinpath("Main").joinpath("bucket"))
gen_repo(c,"Extras",current_dir.joinpath("Extras").joinpath("bucket"))

db.commit()
db.close()
