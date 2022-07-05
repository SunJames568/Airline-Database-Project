insert into airline values('United');

/*
Add 8 airports as follows:
Airport name: JFK, City: NYC, Country: USA, Airport Type: Both
Airport name: BOS, City: Boston, Country: USA, Airport Type: Both
Airport name: PVG, City: Shanghai, Country: China, Airport Type: Both
Airport name: BEI, City: Beijing, Country: China, Airport Type: Both
Airport name: SFO, City: San Francisco, Country: USA, Airport Type: Both
Airport name: LAX, City: Los Angeles, Country: USA, Airport Type: Both
Airport name: HKA, City: Hong Kong, Country: China, Airport Type: Both
Airport name: SHEN City: Shenzhen, Country: China, Airport Type: Both.

*/
insert into airport values('JFK', 'NYC', 'USA', 'Both');
insert into airport values('BOS', 'Boston', 'USA', 'Both');
insert into airport values('PVG', 'Shanghai', 'China', 'Both');
insert into airport values('BEI', 'Beijing', 'China', 'Both');
insert into airport values('SFO', 'San Francisco', 'USA', 'Both');
insert into airport values('LAX', 'Los Angeles', 'USA', 'Both');
insert into airport values('HKA', 'Hong Kong', 'China', 'Both');
insert into airport values('SHEN', 'Shenzhen', 'China', 'Both');

insert into customer values('testcustomer@nyu.edu', 'Test Customer 1', '81dc9bdb52d04dc20036dbd8313ed055', '1555', 'Jay St', 'Brooklyn', 'New York', '123-4321-4321', '54321', 'USA', '2025-12-24', '1999-12-19');
insert into customer values('user1@nyu.edu', 'User 1', '81dc9bdb52d04dc20036dbd8313ed055', '5405', 'Jay Street', 'Brooklyn', 'New York', '123-4322-4322', '54322', 'USA', '2025-12-25', '1999-11-19');
insert into customer values('user2@nyu.edu', 'User 2', '81dc9bdb52d04dc20036dbd8313ed055', '1702', 'Jay Street', 'Brooklyn', 'New York', '123-4323-4323', '54323', 'USA', '2025-10-24', '1999-10-19');
insert into customer values('user3@nyu.edu', 'User 3', '81dc9bdb52d04dc20036dbd8313ed055', '1890', 'Jay Street', 'Brooklyn', 'New York', '123-4324-4324', '54324', 'USA', '2025-09-24', '1999-09    -19');

insert into airplane values(1, 'United', 4, 'Boeing', 10);
insert into airplane values(2, 'United', 4, 'Airbus', 12);
insert into airplane values(3, 'United', 50, 'Boeing', 8);

insert into airline_staff values('admin', 'United', 'e2fc714c4727ee9395f324cd2e7f331f', 'Roe', 'Jones', '1978-05-25');
insert into staff_email values('admin', 'staff@nyu.edu');
insert into staff_phone values('admin', '111-2222-3333');
insert into staff_phone values('admin', '444-5555-6666');

insert into flight values(102, '2022-06-12 13:25:25', 3, 'United', 'SFO', 'LAX', '2022-06-12 16:50:25', 300, 'on-time');
insert into flight values(104, '2022-07-04 13:25:25', 3, 'United', 'PVG', 'BEI', '2022-07-04 16:50:25', 300, 'on-time');
insert into flight values(106, '2022-05-04 13:25:25', 3, 'United', 'SFO', 'LAX', '2022-05-04 16:50:25', 350, 'delayed');
insert into flight values(206, '2022-08-04 13:25:25', 2, 'United', 'SFO', 'LAX', '2022-08-04 16:50:25', 400, 'on-time');
insert into flight values(207, '2022-09-04 13:25:25', 2, 'United', 'LAX', 'SFO', '2022-09-04 16:50:25', 300, 'on-time');
insert into flight values(134, '2022-04-12 13:25:25', 3, 'United', 'JFK', 'BOS', '2022-04-12 16:50:25', 300, 'delayed');
insert into flight values(296, '2022-08-01 13:25:25', 1, 'United', 'PVG', 'SFO', '2022-08-01 16:50:25', 3000, 'on-time');
insert into flight values(715, '2022-06-28 10:25:25', 1, 'United', 'PVG', 'BEI', '2022-06-28 13:50:25', 500, 'delayed');
insert into flight values(839, '2021-09-12 13:25:25', 3, 'United', 'SHEN', 'BEI', '2021-09-12 16:50:25', 300, 'on-time');

insert into ticket values(1,  null, 102, '2022-06-12 13:25:25', null, null, null, null, null, null);
insert into ticket values(2,  null, 102, '2022-06-12 13:25:25', null, null, null, null, null, null);
insert into ticket values(3,  null, 102, '2022-06-12 13:25:25', null, null, null, null, null, null);
insert into ticket values(4,  null, 104, '2022-07-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(5,  null, 104, '2022-07-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(6,  null, 106, '2022-05-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(7,  null, 106, '2022-05-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(8,  null, 839, '2021-09-12 13:25:25', null, null, null, null, null, null);
insert into ticket values(9,  null, 102, '2022-06-12 13:25:25', null, null, null, null, null, null);
insert into ticket values(11, null, 134, '2022-04-12 13:25:25', null, null, null, null, null, null);
insert into ticket values(12, null, 715, '2022-06-28 10:25:25', null, null, null, null, null, null);
insert into ticket values(14, null, 206, '2022-08-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(15, null, 206, '2022-08-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(16, null, 206, '2022-08-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(17, null, 207, '2022-09-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(18, null, 207, '2022-09-04 13:25:25', null, null, null, null, null, null);
insert into ticket values(19, null, 296, '2022-08-01 13:25:25', null, null, null, null, null, null);
insert into ticket values(20, null, 296, '2022-08-01 13:25:25', null, null, null, null, null, null);

update ticket
set email = 'testcustomer@nyu.edu', purchase_date_time = '2022-05-04 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233334444, card_name = 'Test Customer 1', expire_date = '2023-03-01'
where ticket_id = 1;

update ticket
set email = 'user1@nyu.edu', purchase_date_time = '2022-05-03 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 1', expire_date = '2023-03-01'
where ticket_id = 2;

update ticket
set email = 'user2@nyu.edu', purchase_date_time = '2022-06-04 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 2', expire_date = '2023-03-01'
where ticket_id = 3;

update ticket
set email = 'user1@nyu.edu', purchase_date_time = '2022-05-21 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 1', expire_date = '2023-03-01'
where ticket_id = 4;

update ticket
set email = 'testcustomer@nyu.edu', purchase_date_time = '2022-06-28 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233334444, card_name = 'Test Customer 1', expire_date = '2023-03-01'
where ticket_id = 5;

update ticket
set email = 'testcustomer@nyu.edu', purchase_date_time = '2022-05-02 11:55:55', sold_price = 350, card_type = 'credit', card_number = 1111222233334444, card_name = 'Test Customer 1', expire_date = '2023-03-01'
where ticket_id = 6;

update ticket
set email = 'user3@nyu.edu', purchase_date_time = '2022-04-03 11:55:55', sold_price = 350, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 3', expire_date = '2023-03-01'
where ticket_id = 7;

update ticket
set email = 'user3@nyu.edu', purchase_date_time = '2021-09-03 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 3', expire_date = '2023-03-01'
where ticket_id = 8;

update ticket
set email = 'user3@nyu.edu', purchase_date_time = '2022-04-04 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 3', expire_date = '2023-03-01'
where ticket_id = 9;

update ticket
set email = 'user3@nyu.edu', purchase_date_time = '2022-07-23 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 3', expire_date = '2023-03-01'
where ticket_id = 11;

update ticket
set email = 'testcustomer@nyu.edu', purchase_date_time = '2022-0-02 11:55:55', sold_price = 500, card_type = 'credit', card_number = 1111222233334444, card_name = 'Test Customer 1', expire_date = '2023-03-01'
where ticket_id = 12;

update ticket
set email = 'user3@nyu.edu', purchase_date_time = '2022-07-01 11:55:55', sold_price = 400, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 3', expire_date = '2023-03-01'
where ticket_id = 14;

update ticket
set email = 'user1@nyu.edu', purchase_date_time = '2022-07-02 11:55:55', sold_price = 400, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 1', expire_date = '2023-03-01'
where ticket_id = 15;

update ticket
set email = 'user2@nyu.edu', purchase_date_time = '2022-06-19 11:55:55', sold_price = 400, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 2', expire_date = '2023-03-01'
where ticket_id = 16;

update ticket
set email = 'user1@nyu.edu', purchase_date_time = '2022-05-11 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233335555, card_name = 'User 1', expire_date = '2023-03-01'
where ticket_id = 17;

update ticket
set email = 'testcustomer@nyu.edu', purchase_date_time = '2022-06-25 11:55:55', sold_price = 300, card_type = 'credit', card_number = 1111222233334444, card_name = 'Test Customer 1', expire_date = '2023-03-01'
where ticket_id = 18;

update ticket
set email = 'user1@nyu.edu', purchase_date_time = '2022-07-04 11:55:55', sold_price = 3000, card_type = 'credit', card_number = 1111222233334444, card_name = 'Test Customer 1', expire_date = '2023-03-01'
where ticket_id = 19;

update ticket
set email = 'testcustomer@nyu.edu', purchase_date_time = '2022-04-12 11:55:55', sold_price = 3000, card_type = 'credit', card_number = 1111222233334444, card_name = 'Test Customer 1', expire_date = '2023-03-01'
where ticket_id = 20;

insert into rate values('testcustomer@nyu.edu', 102, '2022-06-12 13:25:25', 4, "Very Comfortable");
insert into rate values('user1@nyu.edu', 102, '2022-06-12 13:25:25', 5, "Relaxing, check-in and onboarding very professional");
insert into rate values('user2@nyu.edu', 102, '2022-06-12 13:25:25', 3, "Satisfied and will use the same flight again");
insert into rate values('testcustomer@nyu.edu', 104, '2022-07-04 13:25:25', 1, "Customer Care services are not good");
insert into rate values('user1@nyu.edu', 104, '2022-07-04 13:25:25', 5, "Comfortable journey and Professional");

