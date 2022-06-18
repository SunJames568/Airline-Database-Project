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