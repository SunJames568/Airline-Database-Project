create table customer
(
email varchar(30),
name varchar(50) not null,
password varchar(50) not null,
building_number varchar(50),
street varchar(50),
city varchar(50),
state varchar(50),
phone_number varchar(12),
passport_num int,
passport_country varchar(50),
passport_expiration date,
birth_date date,
primary key(email));

create table airport
(
airport_name varchar(50),
city varchar(50),
country varchar(50),
type varchar(50),
primary key(airport_name));

create table airline
(
airline_name varchar(50),
primary key(airline_name));

create table airplane
(
airplane_id int,
airline_name varchar(50),
seating_capacity int,
manufacturing_company varchar(50),
age int,
primary key(airplane_id, airline_name),
foreign key(airline_name) references airline(airline_name) on delete cascade
);

create table flight
(
flight_num int,
depart_date_time datetime,
airplane_id int,
airline_name varchar(50),
depart_airport varchar(50),
arrival_airport varchar(50),
arrival_date_time datetime,
base_price float(6),
delay_status varchar(50),

primary key(flight_num, depart_date_time),
foreign key(airplane_id, airline_name) references airplane(airplane_id, airline_name) on delete set null,
foreign key(depart_airport) references airport(airport_name) on delete set null,
foreign key(arrival_airport) references airport(airport_name) on delete set null
);

create table ticket
(
ticket_id int,
email varchar(30),
flight_num int,
depart_date_time datetime,
sold_price float(6),
card_type varchar(50),
card_number numeric(16, 0),
card_name varchar(50),
expire_date date,
purchase_date_time timestamp,
primary key(ticket_id),
foreign key(email) references customer(email) on delete set null,
foreign key(flight_num, depart_date_time) references flight(flight_num, depart_date_time) on delete cascade
);

create table rate
(
email varchar(30),
flight_num int,
depart_date_time datetime,
rating_level float(2),
comment varchar(300),
primary key(email, flight_num, depart_date_time),
foreign key(email) references customer(email) on delete cascade,
foreign key(flight_num, depart_date_time) references flight(flight_num, depart_date_time) on delete cascade
);

create table airline_staff
(
username varchar(50),
airline_name varchar(50),
password varchar(500),
first_name varchar(50),
last_name varchar(50),
birth_date date,
primary key(username),
foreign key(airline_name) references airline(airline_name) on delete set null
);

create table staff_phone
(
username varchar(50),
phone_number varchar(13),
primary key(username,phone_number),
foreign key(username) references airline_staff(username) on delete cascade
);

create table staff_email
(
username varchar(50),
email_address varchar(50),
primary key(username,email_address),
foreign key(username) references airline_staff(username) on delete cascade
);

# view for future flights
create view future_flight as
SELECT *
FROM flight
WHERE depart_date_time > CURDATE();

# view for flights with vacancies
create view open_flight as
SELECT distinct
        flight_num,
        depart_date_time,
        airplane_id,
        airline_name,
        depart_airport,
        arrival_airport,
        arrival_date_time,
        base_price,
        delay_status
FROM future_flight natural join ticket
WHERE email is null;

/*
CREATE ROLE staff;
grant staff to airline_staff;
grant select, update, insert on flight to staff;
grant select on rates to staff;
grant insert on airplane to staff;
grant insert on airport to staff;

CREATE ROLE custom;
grant custom to customer;
grant select on flight to custom;
grant update on tickets to custom;
grant insert on rates to custom;
grant insert on rates to custom;
*/