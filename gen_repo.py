import sqlite3,json
from pathlib import Path

def gen_repo(db:sqlite3.Connection,bucket_name:str,bucket_path:Path):
    
    cursor = db.cursor()
    #main_repo_path = pathlib.Path(r"D:\Scoop\Scoop\buckets\main\bucket")
    for file in bucket_path.glob("*.json"):
        with open(file,"r",encoding='utf-8') as f:
            manifest = json.load(f)
            package = file.stem
            version = manifest.get("version")
            if manifest.get("url") != None:
                url = manifest.get("url")
                hash_sum = manifest.get("hash")
            else:
                url = manifest.get("architecture").get("64bit").get("url")
                hash_sum = manifest.get("architecture").get("64bit").get("hash")
            if isinstance(url,str):
                hash_type = ""
                hash_value = ""
                for i in hash_sum:
                    if i == ":":
                        hash_type = hash_sum.split(":")[0]
                        hash_value = hash_sum.split(":")[1]
                        break
                if hash_type == "" and hash_value == "":
                    hash_type = "sha256"
                    hash_value = hash_sum
                sql = f'INSERT INTO {bucket_name} VALUES ("{package}","{version}","{str(url)}","{hash_type}","{hash_value}")'
                cursor.execute(sql)
    cursor.close()
    db.commit()

db = sqlite3.connect('repo.db')

db.execute('''CREATE TABLE Main (PACKAGE TEXT,VERSION TEXT,URL TEXT,HASH_TYPE TEXT,HASH_VALUE TEXT)''')
db.execute('''CREATE TABLE Extras (PACKAGE TEXT,VERSION TEXT,URL TEXT,HASH_TYPE TEXT,HASH_VALUE TEXT)''')

current_dir = Path(__file__).absolute().parent
gen_repo(db,"Main",current_dir.joinpath("Main").joinpath("bucket"))
gen_repo(db,"Extras",current_dir.joinpath("Extras").joinpath("bucket"))

db.close()
