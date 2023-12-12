import psycopg2
from psycopg2 import Error
import random

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        user="juanito",
        password="juanito123",
        host="localhost",
        port=5432,
        database="postgres"
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Create "users" table
    create_table_query = '''CREATE TABLE users
                            (ID SERIAL PRIMARY KEY     NOT NULL,
                            NAME           TEXT    NOT NULL,
                            EMAIL          TEXT     NOT NULL);'''

    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL")

    # Insert random users
    users = [
        ("John Doe", "john@example.com"),
        ("Jane Smith", "jane@example.com"),
        ("Michael Johnson", "michael@example.com"),
        ("Emily Brown", "emily@example.com")
    ]

    insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.executemany(insert_query, users)
    connection.commit()
    print("Data inserted successfully")

    # Show all users
    select_query = "SELECT * FROM users"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

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
