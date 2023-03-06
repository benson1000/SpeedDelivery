
import psycopg2


P_HOST0 = 'postgres://ldqtkymuvcsnlr:'

P_HOST1 = 'd8a8cbb1f77ae9f99769c29a85a42f7df830e670aacfa'
P_HOST2 = '0afd6a5476d85743200@ec2-3-209-39-2.compute-1.'
P_HOST3 = 'amazonaws.com:5432/dipeglem2kl7d'

P_HOST = P_HOST0 + P_HOST1 + P_HOST2 + P_HOST3

conn = psycopg2.connect(P_HOST, sslmode='require')

cursor = conn.cursor()


query1 = "CREATE SEQUENCE account_seq;"


query2 = """CREATE TABLE account(
    id INTEGER PRIMARY KEY DEFAULT NEXTVAL ('account_seq'),
    fullname VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    address INTEGER NOT NULL,
    phone_no INTEGER NOT NULL,
    password VARCHAR(256) NOT NULL
);"""


# SQLINES LICENSE FOR EVALUATION USE ONLY
query3 = "CREATE SEQUENCE delivery_seq;"

query4 = """CREATE TABLE delivery (
    order_id INTEGER PRIMARY KEY DEFAULT NEXTVAL ('delivery_seq'),
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL UNIQUE,
    address VARCHAR(256) NOT NULL,
    phone_no VARCHAR(60) NOT NULL UNIQUE,
    product VARCHAR(60) NOT NULL,
    dtime timestamp NOT NULL,
    special_instructions VARCHAR(256)
);"""

cursor.execute(query1)
conn.commit()

cursor.execute(query2)
conn.commit()

cursor.execute(query3)
conn.commit()

cursor.execute(query4)
conn.commit()

cursor.close()
conn.close()
