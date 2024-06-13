import sqlite3
import pandas as pd
from glob import iglob
from os import path
from pathlib import Path

print(f"{str(Path.cwd()/'*db')}")
for dbname in iglob( str(Path.cwd()/"*db") ):
    dbname = dbname.split("\\")[-1]

    # Check if exported DB CSV exists
    print(f"DB > {dbname}")
    if path.isfile(f"{dbname}.csv"):
        print(f"  - {dbname}.csv exists, next")
        continue
    print(f"  - {dbname}.csv NOT exists, export")

    try:
        # Load Database
        conn = sqlite3.connect(
            f"{dbname}", 
            isolation_level=None, 
            detect_types=sqlite3.PARSE_COLNAMES
        )

        # Read TABLE `dictionary` and export
        tablename = "dictionary" # input("- TABLE NAME\n> ")
        df = pd.read_sql_query(f"SELECT * FROM {tablename}", conn)
        df.to_csv(f"exported/{dbname}.csv", index=False, encoding="utf-8-sig")

    except sqlite3.Error as error:
        print("    [ ERR ]", error)
