create table customer
(
email varchar(30),
name varchar(20) not null,
password varchar(20) not null,
building_number varchar(20),
street varchar(20),
city varchar(20),
state varchar(20),
phone_number varchar(12),
passport_country varchar(20),
passport_expiration date,
birth_date date,
primary key(email));

create table airport
(
airport_name varchar(20),
city varchar(20),
country varchar(20),
type varchar(5),
primary key(airport_name));

create table airline
(
airline_name varchar(20),
primary key(airline_name));

create table airplane
(
airline_id int,
airline_name varchar(20),
seating_capacity int,
maufacturing_company varchar(20),
age int,
primary key(airline_id,airline_name),
foreign key(airline_name) references airline(airline_name) on delete set null
);

create table flight
(
flight_num int,
depart_date_time timestamp,
airline_id int,
airline_name varchar(20),
depart_airport varchar(20),
arrival_airport varchar(20),
arrival_date_time timestamp,
base_price float(6),
delay_status varchar(20),

primary key(flight_num, depart_date_time) on delete set null,
foreign key(airline_id, airline_name) references airplane(airline_id, airline_name) on delete set null,
foreign key(depart_airport) references airport(airport_name) on delete set null,
foreign key(arrival_airport) references airport(airport_name) on delete set null
);

create table tickets
(
ticket_id varchar(20),
email varchar(30),
flight_num int,
depart_date_time timestamp,
sold_price float(6),
card_type varchar(20),
card_number numeric(16, 0),
card_name varchar(20),
expire_date date,
purchase_date_time timestamp,
primary key(ticket_id),
foreign key(email) references customer(email) on delete set null,
foreign key(flight_num, depart_date_time) references flight(flight_num, depart_date_time) on delete set null
);

create table rates
(
email varchar(30),
flight_num int,
depart_date_time timestamp,
rating_level float(2),
comment varchar(300),
primary key(email, flight_num, depart_date_time),
foreign key(email) references customer(email) on delete cascade,
foreign key(flight_num, depart_date_time) references flight(flight_num, depart_date_time) on delete cascade
);

create table airline_staff
(
username varchar(20),
airline_name varchar(20),
password varchar(500),
first_name varchar(20),
last_name varchar(20),
birth_date date,
primary key(username),
foreign key(airline_name) references airline(airline_name) on delete set null
);

create table staff_phone
(
username varchar(20),
phone_number varchar(13),
primary key(username,phone_number),
foreign key(username) references airline_staff(username) on delete cascade
);

create table staff_emails
(
username varchar(20),
email_address varchar(20),
primary key(username,email_address),
foreign key(username) references airline_staff(username) on delete cascade
);
