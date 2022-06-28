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

# Generic view for future flights
create view future_flight as
select *
from flight
where depart_date_time > CURDATE();

# 1. View Public Info
#   a. search future flight based on depart airport, arrival airport, and departure date (+ return for round trip)
select *
from future_flight
where depart_airport = depart and arrival_airport = arrival and depart_date_time = ddatetime;

#   b. see status based on airline name, flight num, arrival/depart date

select status
from future_flight
where airline_name = airline and flight_num = num and depart_date_time = ddatetime;

# 2. Register system for customers + airline staff

insert into customer values('sya@gmail.com', 'Swanyee', '1234', '20', 'Jacobs St', 'NYC', 'NY', '917-345-9381', 'USA', '2009-12-20', '2000-04-18');
# 3. Login for customers + staff


#Customer requirements
# 1. View flights (future + specify date range, destination, and/or depart airport)

# 2. Search for flights (depart airport, arrival port)
# 3. Purchase tickets (choose flight and purchase; build with flight search together)
# 4. Cancel trip (more than 24 hrs from depart, ticket free to other customers)
# 5. rate + comment on flights (previous they took)
# 6. Track spending (total spent in past year and bar graph/table of monthly spending for past 6 months. Can specify date range)
# 7. Logout

/*Airline requirements
the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline 
he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see 
all the customers of a particular flight.
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

