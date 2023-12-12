import psycopg2
from psycopg2 import Error
import csv

# Abrir archivo csv
def leer_csv(filename):
    data = []
    with open(filename, 'r', newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for linea in lector_csv:
            data.append(linea)
    data = data[1:]
    return data

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        user="enfgen",
        password="enfgen1",
        host="localhost",
        port=5432,
        database="bd_enfgen"
    )

    datos = leer_csv("age.csv")

    # Create a cursor object
    cursor = connection.cursor()

    # Insertar los datos
    insert_query = "INSERT INTO asociacion_genetica_de_enfermedad (id, cod_mutacion, cod_enfermedad) VALUES (%s,%s,%s)"
    cursor.executemany(insert_query, datos)
    connection.commit()
    print("Data inserted successfully")

    # Show all users
    select_query = "SELECT * FROM asociacion_genetica_de_enfermedad"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Id: {row[0]}, Tipo: {row[1]}")

    if not rows:
        print("No users found")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")