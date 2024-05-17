import sqlite3
import pandas as pd
from glob import iglob
from os import path, makedirs
from pathlib import Path

OUT_PREFIX = "csv/"
OUT_SUFFIX = ".csv"


makedirs(OUT_PREFIX, exist_ok=True)

for dbname in iglob( str(Path.cwd()/"*db") ):
    dbname = dbname.split("\\")[-1]
    outpath = OUT_PREFIX + dbname + OUT_SUFFIX

    # Check if exported DB CSV exists
    print(f"DB > {dbname}")
    if path.isfile(outpath):
        print(f"  - {dbname} csv exists, next")
        continue
    print(f"  - {dbname} csv NOT exists, export")

    try:
        # Load Database
        conn = sqlite3.connect(
            dbname, 
            isolation_level=None, 
            detect_types=sqlite3.PARSE_COLNAMES
        )

        # Read TABLE `dictionary` and export
        tablename = "dictionary" # input("- TABLE NAME\n> ")
        df = pd.read_sql_query(f"SELECT * FROM {tablename}", conn)
        df.to_csv(outpath, index=False)

    except sqlite3.Error as error:
        print("    - ERROR :", error)
