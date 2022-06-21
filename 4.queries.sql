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
select 

#   b. see status based on airline name, flight num, arrival/depart date
