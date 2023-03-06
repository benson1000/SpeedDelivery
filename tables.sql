-- Create tables

-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE SEQUENCE account_seq;


CREATE TABLE account(
    id INTEGER PRIMARY KEY DEFAULT NEXTVAL ('account_seq'),
    firstname VARCHAR(256) NOT NULL,
    lastname VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    password VARCHAR(256) NOT NULL
);


-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE SEQUENCE delivery_seq;

CREATE TABLE delivery (
    order_id INTEGER PRIMARY KEY DEFAULT NEXTVAL ('delivery_seq'),
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL,
    address VARCHAR(256) NOT NULL,
    phone_no VARCHAR(60) NOT NULL,
    product VARCHAR(60) NOT NULL,
    dtime timestamp NOT NULL,
    special_instructions VARCHAR(256)
);
