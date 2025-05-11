# Initial Gate Code

# Used Libraries
tkinter
sqlite3
os
hashlib
pyserial

# Module
NRF2401
MFRC522

# References
https://howtomechatronics.com/tutorials/arduino/how-to-build-an-arduino-wireless-network-with-multiple-nrf24l01-modules/


# Tables
users
log


# build table
drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null,
    rfid integer not null,
    hash_password text not null,
    salt text not null,
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp,
    last_login datetime
);

insert into users
    (username, rfid, hash_password, salt, created_at, updated_at, last_login)
VALUES
    ('admin', 
    0, 
    '68c31190f052f70d61654d8dffa92f098a09d82c09f592f05b3522abef4b6623', 
    'bfba4abf451e2b13cfa8c6032cb0c6e7',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP);


select *
FROM users
WHERE username = 'admin';

drop table if exists logs;
CREATE TABLE logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        message_type TEXT NOT NULL,
                        description TEXT NOT NULL,
                        full_description TEXT NOT NULL
                    )