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
where depart_airport = 

#   b. see status based on airline name, flight num, arrival/depart date

# 2. Register system for customers + airline staff

# 3. Login for customers + staff


#Customer requirements
# 1. View flights (future + specify date range, destination, and/or depart airport)
# 2. Search for flights (depart airport, arrival port)
# 3. Purchase tickets (choose flight and purchase; build with flight search together)
# 4. Cancel trip (more than 24 hrs from depart, ticket free to other customers)
# 5. rate + comment on flights (previous they took)
# 6. Track spending (total spent in past year and bar graph/table of monthly spending for past 6 months. Can specify date range)
# 7. Logout

#Airline requirements
# 1. 

