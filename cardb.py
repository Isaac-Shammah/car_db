import csv

from cs50 import SQL

open("cardb.db","w").close()

db = SQL("sqlite:///cardb.db")

db.execute("CREATE TABLE cars (cars_id INTEGER, carname TEXT, price INTEGER, rating INTEGER, PRIMARY KEY(cars_id))")

db.execute("CREATE TABLE joint (join_id INTEGER, car_id INTEGER, PRIMARY KEY(join_id), FOREIGN KEY(car_id) REFERENCES cars(cars_id))")

db.execute("CREATE TABLE types (types_id INTEGER, cartype TEXT, carclass TEXT, layout TEXT, engine TEXT, transmission TEXT, horsepower INTEGER, zerotosixty INTEGER, topspeed INTEGER, PRIMARY KEY(types_id), FOREIGN KEY(types_id) REFERENCES joint(join_id))")

db.execute("CREATE TABLE designs (designs_id INTEGER, design TEXT, length INTEGER, width INTEGER, height INTEGER, weight INTEGER, PRIMARY KEY(designs_id), FOREIGN KEY(designs_id) REFERENCES joint(join_id))")


with open("cardb.csv","r") as file:
    reader = csv.DictReader(file)

    for row in reader:

        carname = row["Car"].strip()
        price = row["Price"].strip()
        rating = row["Rating"].strip()

        cars_id = db.execute("INSERT INTO cars (carname, price, rating) VALUES(?,?,?)", carname, price, rating)

        for cartype in row["Type"].split(" , "):

            cartype = cartype.strip()
            carclass = row["Class"].strip()
            layout = row["Layout"].strip()
            engine = row["Engine"].strip()
            transmission = row["Transmission"].strip()
            horsepower = row["Horsepower"].strip()
            zerotosixty = row["Zero-Sixty"].strip()
            topspeed = row["Topspeed"].strip()

            carz_id = db.execute("INSERT INTO joint (car_id) VALUES((SELECT cars_id FROM cars WHERE carname =?))",carname)
            db.execute("INSERT INTO types (types_id, cartype, carclass, layout, engine, transmission, horsepower, zerotosixty, topspeed) VALUES ((SELECT car_id FROM joint WHERE car_id=?),?,?,?,?,?,?,?,?)" , carz_id, cartype, carclass, layout, engine, transmission, horsepower, zerotosixty, topspeed)

            design = row["Body"].strip()
            length = row["Length"].strip()
            width = row["Width"].strip()
            height = row["Height"].strip()
            weight = row["Weight"].strip()

            db.execute("INSERT INTO designs (designs_id, design, length, width, height, weight) VALUES ((SELECT car_id FROM joint WHERE car_id=?),?,?,?,?,?)" , carz_id, design, length, width, height, weight)