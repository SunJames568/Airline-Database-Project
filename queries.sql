select *
from flight
where depart_date_time > CURDATE();

select *
from flight
where delay_status = 'delayed';

select name
from customer natural join tickets

select *
from airplane
where airline_name = "Jet Blue";

# view for future flights
create view future_flight as
select *
from flight
where depart_date_time > CURDATE();

# 1. View Public Info
#   a. search future flight based on depart airport, arrival airport, and departure date (+ return for round trip)

#   by airport
select *
from future_flight
where depart_airport = @depart_port 
    and arrival_airport = @arrival_port 
    and CONVERT(depart_date_time, date) = @depart_d_t;
#        (For return flights)
select *
from future_flight
where depart_airport = @arrival_port 
    and arrival_airport = @depart_port 
    and (CONVERT(depart_date_time, date) = @return_d_t or @return_d_t is NULL);

#   by city
select *
from future_flight, airport as d, airport as a
where depart_airport = d.airport_name
    and d.city = @depart_city
    and arrival_airport = a.airport_name
    and a.city = @arrival_city
    and CONVERT(depart_date_time, date) = @depart_d_t;
#       return flights
select *
from future_flight, airport as d, airport as a
where depart_airport = d.airport_name
    and d.city = @arrival_city
    and arrival_airport = a.airport_name
    and a.city = @depart_city
    and (CONVERT(depart_date_time, date) = @return_d_t or @return_d_t is NULL);
#   b. see status based on airline name, flight num, arrival/depart date
select status
from future_flight
where airline_name = @line_name 
    and flight_num = @f_num 
    and depart_date_time = @depart_d_t 
    and arrival_date_time = @arrival_d_t;

# 2. Register system for customers + airline staff
insert into customer values(@email, @name, @password, @b_num, @street, @city, @state, @phone, @pass_country, @pass_exp, @birth_d);
# 3. Login for customers + staff


#Customer requirements
# 1. View flights (future + specify date range, destination, and/or depart airport)
select flight_num, depart_date_time, airplane_ID, airline_name, depart_airport, arrival_airport, arrival_date_time, base_price, delay_status,
from tickets natural join future_flight
where email = @email;

# 2. Search for flights (depart airport, arrival port)
select *
from future_flight
where depart_airport = @depart_port and arrival_airport = @arrival_port and CONVERT(depart_date_time, date) = @depart_d_t;

    # For return flights
select *
from future_flight
where depart_airport = @arrival_port 
    and arrival_airport = @depart_port 
    and (CONVERT(depart_date_time, date) = @return_d_t or @return_d_t is NULL);

# 3. Purchase tickets (choose flight and purchase; build with flight search together)
with overFilled(value) as (
    select count(flight_num)/seating_capacity
    from tickets
    where flight_num = f_num 
        and depart_date_time = depart_d_t 
        and exists(email);
)
update tickets
    set sold_price = case 
        when  fill
        email = c_email, card_type = c_type, card_name = c_name, expire_date = exp_date, purchase_date_time = purchase_d_t
    where ticket_ID = @t_id;
# 4. Cancel trip (more than 24 hrs from depart, ticket free to other customers)
update tickets
    set email, sold_price, card_type, card_number, card_name, expire_date, purchase_date_time = null
    where ticket_ID = @t_id 
        and (TIMESTAMPDIFF(HOUR, NOW(), depart_date_time) > 24);

# 5. rate + comment on flights (previous they took)
insert into rates values(@email, @f_num, @depart_d_t, @rating_lvl, @comment);
# 6. Track spending (total spent in past year and bar graph/table of monthly spending for past 6 months. Can specify date range)
    # total spent Past year (default view)
select sum(sold_price)
from tickets
where email = c_email 
    and CONVERT(depart_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE();
    # total spent (specify)
select sum(sold_price)
from tickets
where email = c_email 
    and CONVERT(depart_date_time, date) between @date1 and @date2;

    # Monthly spending Past 6 months (default view)
select sum(sold_price)
from tickets
where email = @c_email 
    and CONVERT(depart_date_time, date) between (DATE_SUB(DATE_ADD(CURDATE(), INTERVAL -6 MONTH), INTERVAL DAYOFMONTH(DATE_ADD(CURDATE(), INTERVAL -6 MONTH))-1)) and CURDATE()
group by date_format(depart_date_time, '%M');

    # Monthly spending specified
select sum(sold_price)
from tickets
where email = @c_email 
    and CONVERT(depart_date_time, date) between @date1 and @date2
group by date_format(depart_date_time, '%M');

# 7. Logout

/*Airline requirements
1. View flights: Defaults will be showing all the future flights operated by the airline he/she works for 
the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline 
he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see 
all the customers of a particular flight.
*/
#default view
select *
from future_flight
where airline_name = @line_name 
    and depart_date_time between CURDATE() and DATE_ADD(CURDATE(), INTERVAL 30 DAY); 

#filter flights by airport
select *
from flights natural
where airline_name = @line_name 
    and (depart_airport = @depart_port or @depart_port is NULL) 
    and (arrival_airport = @arrival_port or @arrival_port is NULL)
    and (CONVERT(depart_date_time, date) between @date1 and @date2);

#view customers from specific flight 
select email, name
from tickets
where flight_num = @f_num and depart_date_time = @depart_d_t;

/*
2. Create new flights: He or she creates a new flight, providing all the needed data, via forms. The 
application should prevent unauthorized users from doing this action. Defaults will be showing all the 
future flights operated by the airline he/she works for the next 30 days.
3. Change Status of flights: He or she changes a flight status (from on-time to delayed or vice versa) via 
forms. 
4. Add airplane in the system: He or she adds a new airplane, providing all the needed data, via forms. 
The application should prevent unauthorized users from doing this action. In the confirmation page, 
she/he will be able to see all the airplanes owned by the airline he/she works for.
5. Add new airport in the system: He or she adds a new airport, providing all the needed data, via 
forms. The application should prevent unauthorized users from doing this action.
6. View flight ratings: Airline Staff will be able to see each flight’s average ratings and all the comments 
and ratings of that flight given by the customers.
7. View frequent customers: Airline Staff will also be able to see the most frequent customer within 
the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has 
taken only on that particular airline.
8. View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month 
wise tickets sold in a bar chart/table.
9. View Earned Revenue: Show total amount of revenue earned from ticket sales in the last month and 
last year
*/

