import csv

from cs50 import SQL

open("car_db.db","w").close()

db = SQL("sqlite:///car_db.db")

db.execute("CREATE TABLE car (car_id INTEGER, carname TEXT, price INTEGER, rating INTEGER, PRIMARY KEY(car_id))")

db.execute("CREATE TABLE jointable (join_id INTEGER, cars_id INTEGER, types_id INTEGER, bodys_id INTEGER, PRIMARY KEY(join_id), FOREIGN KEY(cars_id) REFERENCES car(car_id), FOREIGN KEY(types_id) REFERENCES type(type_id), FOREIGN KEY(bodys_id) REFERENCES bodydesign(body_id))")

db.execute("CREATE TABLE type (type_id INTEGER, cartype TEXT, carclass TEXT, layout TEXT, engine TEXT, transmission TEXT, horsepower INTEGER, zerotosixty INTEGER, topspeed INTEGER, PRIMARY KEY(type_id), FOREIGN KEY(type_id) REFERENCES jointable(join_id))")

db.execute("CREATE TABLE bodydesign (body_id INTEGER, bodytype TEXT, length INTEGER, width INTEGER, height INTEGER, weight INTEGER, PRIMARY KEY(body_id), FOREIGN KEY(body_id) REFERENCES jointable(join_id))")


with open("car_db.csv","r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        carname = row["Car"].strip()
        price = row["Price"].strip()
        rating = row["Rating"].strip()
        car_id = db.execute("INSERT INTO car (carname, price, rating) VALUES(?, ?, ?)", carname, price, rating)
        
        for cartype in row["Type"].split("  ,  "):

            cartype = cartype.strip()
            carz_id = db.execute("INSERT INTO jointable(cars_id) VALUES((SELECT car_id FROM car WHERE carname =?))",carname)


            carclass = row["Class"].strip()
            layout = row["Layout"].strip()
            engine = row["Engine"].strip()
            transmission = row["Transmission"].strip()
            horsepower = row["Horsepower"].strip()
            zerotosixty = row["Zero-Sixty"].strip()
            topspeed = row["Topspeed"].strip()
            db.execute("INSERT INTO type (type_id, cartype, carclass, layout, engine, transmission, horsepower, zerotosixty, topspeed) VALUES ((SELECT cars_id FROM jointable WHERE cars_id=?),?, ?, ?, ?, ?, ?, ?, ?)" , carz_id, cartype, carclass, layout, engine, transmission, horsepower, zerotosixty, topspeed)

            bodytype = row["Body"].strip()
            length = row["Length"].strip()
            width = row["Width"].strip()
            height = row["Height"].strip()
            weight = row["Weight"].strip()
            db.execute("INSERT INTO bodydesign (body_id, bodytype, length, width, height, weight) VALUES ((SELECT cars_id FROM jointable WHERE cars_id=?),?, ?, ?, ?,?)" , carz_id, bodytype, length, width, height, weight)