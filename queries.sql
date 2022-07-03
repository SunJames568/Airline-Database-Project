# view for future flights
create view future_flight as
SELECT *
FROM flight
WHERE depart_date_time > CURDATE();

# 1. View Public Info
#   a. search future flight based on depart airport, arrival airport, and departure date (+ return for round trip)

#   by airport
SELECT *
FROM future_flight
WHERE depart_airport = @depart_port 
    and arrival_airport = @arrival_port 
    and CONVERT(depart_date_time, date) = @depart_d_t;
#        (For return flights)
SELECT *
FROM future_flight
WHERE depart_airport = @arrival_port 
    and arrival_airport = @depart_port 
    and (CONVERT(depart_date_time, date) = @return_d_t);

#   by city
SELECT *
FROM future_flight, airport as d, airport as a
WHERE depart_airport = d.airport_name
    and d.city = @depart_city
    and arrival_airport = a.airport_name
    and a.city = @arrival_city
    and CONVERT(depart_date_time, date) = @depart_d_t;
#       return flights
SELECT *
FROM future_flight, airport as d, airport as a
WHERE depart_airport = d.airport_name
    and d.city = @arrival_city
    and arrival_airport = a.airport_name
    and a.city = @depart_city
    and (CONVERT(depart_date_time, date) = @return_d_t);
#   b. see status based on airline name, flight num, arrival/depart date
SELECT status
FROM future_flight
WHERE airline_name = @line_name 
    and flight_num = @f_num 
    and CONVERT(depart_date_time, date) = @depart_d 
    and CONVERT(arrival_date_time, date) = @arrival_d;

# 2. Register system for customers + airline staff
INSERT into customer values(@email, @name, @password, @b_num, @street, @city, @state, @phone, @pass_country, @pass_exp, @birth_d);
# 3. Login for customers + staff


#Customer requirements
# 1. View flights (future + specify date range, destination, and/or depart airport)
SELECT flight_num, depart_date_time, airplane_ID, airline_name, depart_airport, arrival_airport, arrival_date_time, base_price, delay_status,
FROM ticket natural join future_flight
WHERE email = @email;

SELECT *
FROM flights
WHERE email = @email 
    and (depart_airport = @depart_port or @depart_port = "") 
    and (arrival_airport = @arrival_port or @arrival_port = "")
    and (CONVERT(depart_date_time, date) between @date1 and @date2);

# 2. Search for flights (depart airport, arrival port)
SELECT *
FROM future_flight
WHERE depart_airport = @depart_port 
    and arrival_airport = @arrival_port 
    and CONVERT(depart_date_time, date) = @depart_d_t;

    # For return flights
SELECT *
FROM future_flight
WHERE depart_airport = @arrival_port 
    and arrival_airport = @depart_port 
    and (CONVERT(depart_date_time, date) = @return_d_t);

# 3. Purchase tickets (choose flight and purchase; build with flight search together)
    # Check for openings
SELECT *
FROM open_flight
WHERE flight_num = @flight_num and depart_date_time = @depart_date_time

    # Check if seating over %60
SELECT count(email)/seating_capacity as ratio\
FROM ticket natural join open_flight natural join airplane\
WHERE flight_num = @f_num \
    and depart_date_time = @depart_d_t

    # Find vaccant ticket
SELECT ticket_id\
    FROM ticket\
    WHERE flight_num = @f_num and depart_date_time = @depart_d_t

UPDATE ticket\
    SET sold_price = @price, email = @c_email, card_type = @c_type, card_name = @c_name, expire_date = @exp_date, purchase_date_time = @purchase_d_t and depart_date_time=depart_date_time \
    WHERE ticket_id = @t_id;
# 4. Cancel trip (more than 24 hrs FROM depart, ticket free to other customers)

    # Check if flight is eligible for cancellation
SELECT *
FROM future_flight
WHERE flight_num = @f_num 
    and depart_date_time = @depart_d_t
    and (TIMESTAMPDIFF(HOUR, NOW(), depart_date_time) > 24);

UPDATE ticket
    set email, sold_price, card_type, card_number, card_name, expire_date, purchase_date_time = null
    WHERE email = @email;

# 5. rate + comment on flights (previous they took)
INSERT into rate values(@email, @f_num, @depart_d_t, @rating_lvl, @comment);
# 6. Track spending (total spent in past year and bar graph/table of monthly spending for past 6 months. Can specify date range)
    # total spent Past year (default view)
SELECT sum(sold_price) as total
FROM ticket
WHERE email = @c_email 
    and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE();
    # total spent (specify)
SELECT sum(sold_price) as total
FROM ticket
WHERE email = @c_email  
    and CONVERT(purchase_date_time, date) between @date1 and @date2;

    # Monthly spending Past 6 months (default view)
SELECT date_format(purchase_date_time, '%M') as month, sum(sold_price) as m_spend
FROM ticket
WHERE email = @c_email 
    and CONVERT(purchase_date_time, date) between (DATE_ADD(CURDATE(), INTERVAL -6 MONTH)) and CURDATE()
GROUP BY date_format(purchase_date_time, '%M');

    # Monthly spending specified
SELECT date_format(purchase_date_time, '%M') as month, sum(sold_price) as m_spend
FROM ticket
WHERE email = @c_email 
    and CONVERT(purchase_date_time, date) between @date1 and @date2
group by date_format(purchase_date_time, '%M');

# 7. Logout

/*Airline requirements
1. View flights: Defaults will be showing all the future flights operated by the airline he/she works for 
the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline 
he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see 
all the customers of a particular flight.
*/
#default view
SELECT *
FROM future_flight
WHERE airline_name = @line_name 
    and depart_date_time between CURDATE() and DATE_ADD(CURDATE(), INTERVAL 30 DAY); 

#filter flights by airport
SELECT *
FROM flights
WHERE airline_name = @line_name 
    and (depart_airport = @depart_port or @depart_port = "") 
    and (arrival_airport = @arrival_port or @arrival_port = "")
    and (CONVERT(depart_date_time, date) between @date1 and @date2);

#view customers FROM specific flight 
SELECT email, name
FROM ticket
WHERE flight_num = @f_num and depart_date_time = @depart_d_t;


#2. Create new flights: He or she creates a new flight, providing all the needed data, via forms. The 
# application should prevent unauthorized users FROM doing this action. Defaults will be showing all the 
# future flights operated by the airline he/she works for the next 30 days.
INSERT into flight values(@flight_num, @depart_date_time, @airplane_id, @airline_name, @depart_airport, @arrival_airport, @arrival_date_time, @base_price, @delay_status);

    # Insert ticket values based on seat capacity
for i in range(data2['seating_capacity']):
            ins2 = 'INSERT into ticket values(%s, NULL, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL)'
            cursor.execute(ins2, (i, flight_num, depart_date_time))

#3. Change Status of flights: He or she changes a flight status (FROM on-time to delayed or vice versa) via forms. 
UPDATE flight
    SET delay_status = @status, depart_date_time = depart_date_time
    WHERE flight_num = @flight_num and depart_date_time = @depart_d_t;

#4. Add airplane in the system: He or she adds a new airplane, providing all the needed data, via forms. 
#The application should prevent unauthorized users FROM doing this action. In the confirmation page, 
#she/he will be able to see all the airplanes owned by the airline he/she works for.
INSERT into airplane values(@airplane_id, @airline_name, @seating_capacity, @maufacturing_company, @age);
#Confirmation view
select *
from airplane
where airline_name = @airline_name;

#5. Add new airport in the system: He or she adds a new airport, providing all the needed data, via 
#forms. The application should prevent unauthorized users FROM doing this action.
INSERT into aiport values(@airport_name, @city, @country, @type);

/*6. View flight ratings: Airline Staff will be able to see each flight’s average ratings and all the comments 
and ratings of that flight given by the customers.*/
SELECT avg(rating_level)
FROM rate
WHERE flight_num = @flight_num and depart_date_time = @depart_d_t;

SELECT email, comment
FROM rate
WHERE flight_num = @flight_num and depart_date_time = @depart_d_t;

/*7. View frequent customers: Airline Staff will also be able to see the most frequent customer within 
the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has 
taken only on that particular airline.*/
WITH flightCount(email, amount) as (
    SELECT email, count(ticket_ID)
    FROM ticket natural join flight
    WHERE airline_name = @airline_name 
        and CONVERT(depart_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE()
    GROUP by email
),
    mostFlights(amount) as (
    SELECT max(amount)
    FROM flightCount
)
SELECT email, amount
FROM flightCount, mostFlights
WHERE flightCount.amount = mostFlights.amount

/*8. View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month 
wise tickets sold in a bar chart/table.*/
#Custom
SELECT count(ticket_ID)
FROM ticket natural join flight
WHERE airline_name = @airline_name
    and CONVERT(depart_date_time, date) between @date1 and @date2;
#Last Year
SELECT count(ticket_ID)
FROM ticket natural join flight
WHERE airline_name = @airline_name
    and email is not null\
    and CONVERT(depart_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE();
#Last Month
SELECT count(ticket_ID)
FROM ticket natural join flight
WHERE airline_name = @airline_name
    and email is not null\
    and CONVERT(depart_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 MONTH) and CURDATE();

# Bar Charts
    #Custom
SELECT date_format(depart_date_time, '%M'), count(ticket_ID)
FROM ticket natural join flight
WHERE airline_name = @airline_name
    and email is not null\
    and CONVERT(depart_date_time, date) between @date1 and @date2
GROUP BY date_format(depart_date_time, '%M');
    # Last Year
SELECT date_format(purchase_date_time, '%%M') as month, count(ticket_ID) as m_sold\
FROM ticket natural join flight\
WHERE airline_name = %s\
    and email is not null\
    and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE()\
GROUP BY date_format(purchase_date_time, '%%M');
    #Last Month
    SELECT date_format(depart_date_time, '%M'), count(ticket_ID)
FROM ticket natural join flight
WHERE airline_name = @airline_name
    and email is not null\
    and CONVERT(depart_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 MONTH) and CURDATE()
GROUP BY date_format(depart_date_time, '%M');

/*9. View Earned Revenue: Show total amount of revenue earned FROM ticket sales in the last month and 
last year*/
# last month
SELECT sum(sold_price)
FROM ticket natural join flight
WHERE airline_name = @airline_name
    and CONVERT(depart_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 MONTH) and CURDATE();
# last year
SELECT sum(sold_price)
FROM ticket natural join flight
WHERE airline_name = @airline_name
    and CONVERT(depart_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE();




