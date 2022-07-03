insert into airline values('JetBlue');

insert into airport values('JFK', 'NYC', 'USA', null);
insert into airport values('PVG', 'Shanghai', 'China', null);


insert into customer values('sya@gmail.com', 'Swanyee', '1234', '20', 'Jacobs St', 'NYC', 'NY', '917-345-9381', 'USA', '2009-12-20', '2000-04-18');
insert into customer values('james@gmail.com', 'James', 'badPassword', '18B', 'Sun Rd', 'NYC', 'NY', '917-345-6301', 'USA', '2007-11-18', '2001-09-04');
insert into customer values('josh@gmail.com', 'Josh', '9101', '13C', 'Adams St', 'NYC', 'NY', '917-345-8512', 'USA', '2010-10-19', '1998-12-20');
insert into customer values('sdl@gmail.com', 'Sid', 'password', '13C', 'Dan St', 'NYC', 'NY', '917-345-8512', 'USA', '2010-10-19', '1998-12-20');

insert into airplane values(1234, 'JetBlue', 10, 'Boeing', 3);
insert into airplane values(5678, 'JetBlue', 3, 'Airbus', 2);
insert into airplane values(9101, 'JetBlue', 10, 'Boeing', 5);

insert into airline_staff values('Jacob2005', 'JetBlue', 'AnotherPoorPassword19831', 'Jacob', 'Williams', '1998-10-19');
insert into staff_email values('Jacob2005', 'Jacob2005@hotmail.com');
insert into staff_phone values('Jacob2005', '917-345-8512');

insert into flight values(201, '2023-07-23 11:10:11', 1234, 'JetBlue', 'JFK', 'PVG', '2017-07-23 13:10:11', 103.99, 'ontime');
insert into flight values(402, '2021-10-25 09:10:11', 5678, 'JetBlue', 'PVG', 'JFK', '2017-07-24 13:10:11', 103.50, 'delayed');

insert into ticket values(94841, 'sya@gmail.com',  201, '2023-07-23 11:10:11', 59.00, 'Credit', 948103754061, 'Visa', '2037-05-01', '2017-07-14 05:10:12');
insert into ticket values(42932, 'josh@gmail.com', 201, '2023-07-23 11:10:11', 49.99, 'Credit', 648103754041, 'MasterCard', '2027-05-01', '2017-07-19 09:10:11');
insert into ticket values(56713, 'james@gmail.com', 402, '2021-10-25 09:10:11', 47.59, 'Debit', 148123754011, 'Visa', '2024-05-01', '2017-05-29 04:10:01');
insert into ticket values(62343, null, 402, '2021-10-25 09:10:11', 42.59, null, null, null, null, null);