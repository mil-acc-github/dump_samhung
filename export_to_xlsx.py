import sqlite3
import pandas as pd
from glob import iglob
from os import path
from pathlib import Path

print(f"{str(Path.cwd()/'*db')}")
for dbname in iglob( str(Path.cwd()/"*db") ):
    dbname = dbname.split("\\")[-1]

    # Check if exported DB xlsx exists
    print(f"DB > {dbname}")
    if path.isfile(f"{dbname}.xlsx"):
        print(f"  - {dbname}.xlsx exists, next")
        continue
    print(f"  - {dbname}.xlsx NOT exists, export")

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
        df.to_excel(f"exported/{dbname}.xlsx", index=False, engine='xlsxwriter')

    except sqlite3.Error as error:
        print("    [ ERR ]", error)
