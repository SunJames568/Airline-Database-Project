#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import hashlib
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='ticketSys',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

def require_customer_login():
    if not "username" not in session:
        return redirect(url_for("login"))
    elif session["userType"] != "Customer":
        return redirect(url_for("staffHome"))
def require_staff_login():
    if "username" not in session:
        return redirect(url_for("login"))
    elif session["userType"] != "Staff":
        return redirect(url_for("customerHome"))

#Define a route to hello function
@app.route('/')
def start():
    return render_template('index.html')

@app.route('/publicSearch')
def publicSearch():

    return render_template('publicSearch.html')

@app.route('/publicSearch/port', methods=['GET', 'POST'])
def publicSearchPort():
    depAirport = request.form['depAirport']
    arrAirport = request.form['arrAirport']
    date1 = request.form['date1']
    date2 = request.form['date2']
    data2 = []
    rt = False
    cursor = conn.cursor();
    query1 = 'SELECT *\
            FROM future_flight\
            WHERE depart_airport = %s \
                and arrival_airport = %s \
                and CONVERT(depart_date_time, date) = %s'
    cursor.execute(query1, (depAirport, arrAirport, date1))
    data1 = cursor.fetchall()

    if (date2 != ""):
        rt = True
        query2 = 'SELECT *\
                FROM future_flight\
                WHERE depart_airport = %s \
                    and arrival_airport = %s \
                    and (CONVERT(depart_date_time, date) = %s'
        cursor.execute(query2, (arrAirport, depAirport, date2))
        data2 = cursor.fetchall()
    cursor.close()
    return render_template('publicSearchResults.html', post1=data1, post2=data2, rt=rt)

@app.route('/publicSearch/city', methods=['GET', 'POST'])
def publicSearchCity():
    depCity = request.form['depCity']
    arrCity = request.form['arrCity']
    date1 = request.form['dateC1']
    date2 = request.form['dateC2']
    data2 = []
    rt = False
    cursor = conn.cursor();
    query1 = "SELECT flight_num, airline_name, airplane_id, depart_date_time, depart_airport, arrival_date_time, arrival_airport, base_price, delay_status\
            FROM future_flight, airport as d, airport as a\
            WHERE depart_airport = d.airport_name\
                and d.city = %s\
                and arrival_airport = a.airport_name\
                and a.city = %s\
                and CONVERT(depart_date_time, date) =  %s"
    cursor.execute(query1, (depCity, arrCity, date1))
    data1 = cursor.fetchall()

    if (date2 != ""):
        rt = True
        query2 = "SELECT flight_num, airline_name, airplane_id, depart_date_time, depart_airport, arrival_date_time, arrival_airport, base_price, delay_status\
            FROM future_flight, airport as d, airport as a\
            WHERE depart_airport = d.airport_name\
                and d.city = %s\
                and arrival_airport = a.airport_name\
                and a.city = %s\
                and CONVERT(depart_date_time, date) =  %s"
        cursor.execute(query2, (arrCity, depCity, date2))
        data2 = cursor.fetchall()
    cursor.close()
    return render_template('publicSearchResults.html', post1=data1, post2=data2, rt=rt)

@app.route('/publicSearch/status', methods=['GET', 'POST'])
def publicSearchStatus():
    airlineName = request.form['airlineName']
    flightNumber = request.form['flightNumber']
    date1 = request.form['retDate']
    date2 = request.form['arrDate']
    status = ""
    cursor = conn.cursor();
    query1 = 'SELECT delay_status\
            FROM future_flight\
            WHERE airline_name = %s \
                and flight_num = %s \
                and CONVERT(depart_date_time, date) = %s \
                and CONVERT(arrival_date_time, date) = %s'
    cursor.execute(query1, (airlineName, flightNumber, date1, date2))
    status = cursor.fetchone()['delay_status']
    cursor.close()
    return render_template('publicSearch.html', status=status)

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for customer register
@app.route('/registerCustomer')
def registerCustomer():
    return render_template('registerCustomer.html')

#Define route for staff register
@app.route('/registerStaff')
def registerStaff():
    return render_template('registerStaff.html')

#Authenticates the login
@app.route('/loginCustomerAuth', methods=['GET', 'POST'])
def loginAuthCustomer():
    #grabs information from the forms
    username = request.form['customer_email']
    password = hashlib.md5(request.form['customer_pw'].encode()).hexdigest()

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        session['usertype'] = 'Customer'
        session['airline'] = ''
        return redirect(url_for('customerHome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or email'
        return render_template('login.html', error=error)

@app.route('/loginStaffAuth', methods=['GET', 'POST'])
def loginAuthStaff():
    #grabs information from the forms
    username = request.form['staff_uname']
    password = hashlib.md5(request.form['staff_pw'].encode()).hexdigest()

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT airline_name FROM airline_staff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        session['usertype'] = 'Staff'
        session['airline'] = data['airline_name']
        return redirect(url_for('staffHome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerCustomerAuth', methods=['GET', 'POST'])
def registerAuthCustomer():
    #grabs information from the forms
    email = request.form['email']
    name = request.form['name']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    birth_date = request.form['birth_date']

    print(type(building_number))
    
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This customer already exists"
        return render_template('registerCustomer.html', error = error)
    else:
        ins = 'insert into customer values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_expiration, passport_country, birth_date))
        conn.commit()
        cursor.close()
        return render_template('registerCustomer.html', regPass = True)

@app.route('/registerStaffAuth', methods=['GET', 'POST'])
def registerAuthStaff():
    #grabs information from the forms
    username = request.form['username']
    airline_name = request.form['airline_name']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birth_date = request.form['birth_date']
    phone_number = request.form['phone_number']
    email_address = request.form['email_address']

    p_list = phone_number.split(",")
    e_list = email_address.split(",")
    
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This username already exists"
        return render_template('registerStaff.html', error = error)
    else:
        ins = 'insert into airline_staff values(%s, %s, %s, %s, %s, %s)'
        p_ins = 'insert into staff_phone values(%s, %s)'
        e_ins = 'insert into staff_email values(%s, %s)'

        cursor.execute(ins, (username, airline_name, password, first_name, last_name, birth_date))
        for num in p_list:
            cursor.execute(p_ins, (username, num.strip()))
        for email in e_list:
            cursor.execute(e_ins, (username, email.strip()))

        conn.commit() 
        cursor.close()
        return render_template('registerStaff.html', regPass = True)

@app.route('/customerHome')
@require_customer_login
def customerHome(msg=None):
    
    email = session['username']
    cursor = conn.cursor();
    query = 'SELECT flight_num, airline_name, airplane_id, depart_date_time, depart_airport, arrival_date_time, arrival_airport, delay_status FROM ticket natural join future_flight WHERE email = %s'
    cursor.execute(query, (email))
    data1 = cursor.fetchall() 
    cursor.close()
    return render_template('customerHome.html', posts=data1, email=email, msg=msg)

@app.route('/customerSearch')
def customerSearch():
    return render_template('customerSearch.html')

@app.route('/customerHome/filter', methods=['GET', 'POST'])
def customerHomeFilter():
    username = session['username']
    depAirport = request.form['depAirport']
    arrAirport = request.form['arrAirport']
    date1 = request.form['date1']
    date2 = request.form['date2']

    cursor = conn.cursor();
    query = 'SELECT flight_num, airline_name, airplane_id, depart_date_time, depart_airport, arrival_date_time, arrival_airport, base_price, delay_status \
            FROM flight natural join ticket \
            WHERE email = %(name)s \
                and (depart_airport = %(dep)s or %(dep)s = "") \
                and (arrival_airport = %(arr)s or %(arr)s = "") \
                and (CONVERT(depart_date_time, date) between %(d1)s and %(d2)s);'
    paramFilter = {
        "name" : username,
        "dep" : depAirport,
        "arr" : arrAirport,
        "d1" : date1,
        "d2" : date2
    }
    cursor.execute(query, paramFilter)
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('customerHome.html',  username=username, posts=data1, filtered=True)


@app.route('/customerSearch/port', methods=['GET', 'POST'])
def pcustomerSearchPort():
    depAirport = request.form['depAirport']
    arrAirport = request.form['arrAirport']
    date1 = request.form['date1']
    date2 = request.form['date2']
    data2 = []
    rt = False
    cursor = conn.cursor();
    query1 = 'SELECT *\
            FROM future_flight\
            WHERE depart_airport = %s \
                and arrival_airport = %s \
                and CONVERT(depart_date_time, date) = %s'
    cursor.execute(query1, (depAirport, arrAirport, date1))
    data1 = cursor.fetchall()

    if (date2 != ""):
        rt = True
        query2 = 'SELECT *\
                FROM future_flight\
                WHERE depart_airport = %s \
                    and arrival_airport = %s \
                    and CONVERT(depart_date_time, date) = %s'
        cursor.execute(query2, (arrAirport, depAirport, date2))
        data2 = cursor.fetchall()
    cursor.close()
    return render_template('customerSearchResults.html', post1=data1, post2=data2, rt=rt)

@app.route('/customerSearch/city', methods=['GET', 'POST'])
def customerSearchCity():
    depCity = request.form['depCity']
    arrCity = request.form['arrCity']
    date1 = request.form['dateC1']
    date2 = request.form['dateC2']
    data2 = []
    rt = False
    cursor = conn.cursor();
    query1 = "SELECT flight_num, airline_name, airplane_id, depart_date_time, depart_airport, arrival_date_time, arrival_airport, base_price, delay_status\
            FROM future_flight, airport as d, airport as a\
            WHERE depart_airport = d.airport_name\
                and d.city = %s\
                and arrival_airport = a.airport_name\
                and a.city = %s\
                and CONVERT(depart_date_time, date) =  %s"
    cursor.execute(query1, (depCity, arrCity, date1))
    data1 = cursor.fetchall()

    if (date2 != ""):
        rt = True
        query2 = "SELECT flight_num, airline_name, airplane_id, depart_date_time, depart_airport, arrival_date_time, arrival_airport, base_price, delay_status\
            FROM future_flight, airport as d, airport as a\
            WHERE depart_airport = d.airport_name\
                and d.city = %s\
                and arrival_airport = a.airport_name\
                and a.city = %s\
                and CONVERT(depart_date_time, date) =  %s"
        cursor.execute(query2, (arrCity, depCity, date2))
        data2 = cursor.fetchall()
    cursor.close()
    return render_template('customerSearchResults.html', post1=data1, post2=data2, rt=rt)

@app.route('/customerSearch/status', methods=['GET', 'POST'])
def customerSearchStatus():
    airlineName = request.form['airlineName']
    flightNumber = request.form['flightNumber']
    date1 = request.form['retDate']
    date2 = request.form['arrDate']
    status = ""

    cursor = conn.cursor();
    query1 = 'SELECT delay_status\
            FROM future_flight\
            WHERE airline_name = %s \
                and flight_num = %s \
                and CONVERT(depart_date_time, date) = %s \
                and CONVERT(arrival_date_time, date) = %s'
    cursor.execute(query1, (airlineName, flightNumber, date1, date2))
    status = cursor.fetchone()['delay_status']
    cursor.close()
    return render_template('customerSearch.html', status=status)

@app.route('/customerCancel', methods=['GET', 'POST'])
def customerCancel():
    flight_num = request.form['flight_num']
    depart_date_time = request.form['depart_date_time']
    username = session['username']
    error = None
    c_pass = False

    # Check if flight is at least 24 hrs in the future
    cursor = conn.cursor();
    query1 = "SELECT * \
            FROM future_flight \
            WHERE flight_num = %s \
                and depart_date_time = %s \
                and (TIMESTAMPDIFF(HOUR, NOW(), depart_date_time) > 24)"
    cursor.execute(query1, (flight_num, depart_date_time))
    data1 = cursor.fetchone()

    # Flight is ineligible for cancelling
    if (not data1):
        cursor.close()
        error = "Flight is ineligible for cancellation."
        return render_template('customerPurchase.html', error=error)
    else:
        c_pass = "Flight successfully cancelled!"
        ins = "UPDATE ticket\
                SET sold_price = NULL, email = NULL, card_type = NULL, card_number = NULL, card_name = NULL, expire_date = NULL, depart_date_time=depart_date_time, purchase_date_time = NULL \
                WHERE flight_num = %s and email = %s"
        cursor.execute(ins, (flight_num, username))
        conn.commit()
        cursor.close()
        return (redirect(url_for("customerHome", msg=c_pass)))

@app.route('/customerRate', methods=['GET', 'POST'])
def customerRate():
    flight_num = request.form['flight_num']
    depart_date_time = request.form['depart_date_time']
    username = session['username']
    error = None
    rate_pass = False

    # Check if flight is in the past
    cursor = conn.cursor();
    query1 = "SELECT * \
            FROM future_flight \
            WHERE flight_num = %s \
                and depart_date_time = %s \
                and (TIMESTAMPDIFF(HOUR, NOW(), depart_date_time) < 0)"
    cursor.execute(query1, (flight_num, depart_date_time))
    data1 = cursor.fetchone()

    # Check if rating was already made
    query2 = "SELECT * \
            FROM rate \
            WHERE flight_num = %s \
                and depart_date_time = %s \
                and email = %s"
    cursor.execute(query2, (flight_num, depart_date_time, username))
    data2 = cursor.fetchone()

    # Flight is ineligible for rating
    if data1 or data2:
        cursor.close()
        error = "Flight is ineligible for rating."
        return render_template('customerRate.html', error=error)
    else:
        cursor.close()
        return render_template('customerRate.html', f_num=flight_num, depart_dt = depart_date_time)

@app.route('/customerRateAuth', methods=['GET', 'POST'])
def customerRateAuth():
    flight_num = request.form['flight_num']
    depart_date_time = request.form['depart_date_time']
    rating = request.form['rating']
    comment = request.form['comment']
    username = session['username']
    rate_pass = False

    cursor = conn.cursor();
    rate = "Rating submitted! Thank you!"
    ins = "INSERT into rate values(%s, %s, %s, %s, %s)"
    cursor.execute(ins, (username, flight_num, depart_date_time, rating, comment))
    conn.commit()
    cursor.close()
    return (redirect(url_for("customerHome", msg=rate)))

@app.route('/customerPurchase', methods=['GET', 'POST'])
def customerPurchase():
    flight_num = request.form['flight_num']
    depart_date_time = request.form['depart_date_time']

    #Check if flight is full
    cursor = conn.cursor();
    query1 = "SELECT *\
                FROM open_flight\
                WHERE flight_num = %s and depart_date_time = %s"
    cursor.execute(query1, (flight_num, depart_date_time))
    data1 = cursor.fetchall()

    if(not data1):
        cursor.close()
        error = "This flight has no seats remaining."
        return render_template('customerPurchase.html', error=error)
    else:
        # Determine if over %60 seat capacity
        query2 = "SELECT count(email)/seating_capacity as ratio\
                    FROM ticket natural join open_flight natural join airplane\
                    WHERE flight_num = %s \
                        and depart_date_time = %s"
        cursor.execute(query2, (flight_num, depart_date_time))
        cursor.close()
        data2 = float(cursor.fetchone()['ratio'])
        price = float(data1[0]['base_price'])
        if data2 >= 0.6:
            price *= 1.2

        return render_template('customerPurchase.html', line=data1[0], price=price)  

@app.route('/customerPurchaseAuth', methods=['GET', 'POST'])
def customerPurchaseAuth():
    username = session['username']
    cardtype = request.form['cardtype']
    cardname = request.form['cardname']
    cardnumber = request.form['cardnumber']
    expdate = request.form['expdate']
    flight_num = request.form['flight_num']
    depart_date_time = request.form['depart_date_time']
    price = request.form['price']

    # Find a vaccant ticket and its ID
    cursor = conn.cursor();
    query = "SELECT ticket_id\
            FROM ticket\
            WHERE flight_num = %s and depart_date_time = %s"
    cursor.execute(query, (flight_num, depart_date_time))
    data1 = cursor.fetchone()

    # Fill it with customer data
    ins = "UPDATE ticket\
            SET sold_price = %s, email = %s, card_type = %s, card_number = %s, card_name = %s, expire_date = %s, depart_date_time=depart_date_time \
            WHERE ticket_id = %s"
    cursor.execute(ins, (price, username, cardtype, cardnumber, cardname, expdate, data1['ticket_id']))
    conn.commit()
    cursor.close()
    msg = "Successfully purchased ticket for flight ", flight_num
    return (redirect(url_for("customerHome", msg=msg)))

@app.route('/customerSpend')
def customerSpend():
    username = session['username']

   # Find total spending in past year
    cursor = conn.cursor();
    query1 = "SELECT sum(sold_price) as total\
            FROM ticket\
            WHERE email = %s \
                and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE();"
    cursor.execute(query1, (username))
    data1 = cursor.fetchone()

    # Find monthly spending
    query2 = "SELECT date_format(purchase_date_time, '%%M') as month, sum(sold_price) as m_spend \
            FROM ticket WHERE email = %s \
                and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -6 MONTH) and CURDATE() \
            GROUP by date_format(purchase_date_time, '%%M')"
    cursor.execute(query2, (username))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('customerSpend.html', t_spend=data1['total'], posts=data2)  

@app.route('/customerSpend/filter', methods=['GET', 'POST'])
def customerSpendFilter():
    username = session['username']
    date1 = request.form['date1']
    date2 = request.form['date2']

   # Find total spending in past year
    cursor = conn.cursor();
    query1 = "SELECT sum(sold_price) as total\
            FROM ticket\
            WHERE email = %s \
                and CONVERT(purchase_date_time, date) between %s and %s;"
    cursor.execute(query1, (username, date1, date2))
    data1 = cursor.fetchone()

    # Find monthly spending
    query2 = "SELECT date_format(purchase_date_time, '%%M') as month, sum(sold_price) as m_spend \
            FROM ticket WHERE email = %s \
                and CONVERT(purchase_date_time, date) between %s and %s \
            GROUP by date_format(purchase_date_time, '%%M')"
    cursor.execute(query2, (username, date1, date2))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('customerSpend.html', t_spend=data1['total'], posts=data2)  

@app.route('/staffHome')
def staffHome():
    username = session['username']
    airline = session['airline']
    cursor = conn.cursor();
    query = 'SELECT * FROM future_flight WHERE airline_name = %s'
    cursor.execute(query, (airline))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('staffHome.html', username = username, posts=data1, filtered = False)

@app.route('/staffHome/rating', methods=['GET', 'POST'])
def staffRate():
    flight_num = request.form['flight_num']
    depart_date_time = request.form['depart_date_time']

    cursor = conn.cursor();
    query1 = 'SELECT avg(rating_level) as avg\
                    FROM rate\
                    WHERE flight_num = %s and depart_date_time = %s'
    cursor.execute(query1, (flight_num, depart_date_time))
    data1 = cursor.fetchone()

    query2 = 'SELECT name, email, rating_level, comment\
            FROM customer natural join rate\
            WHERE flight_num = %s and depart_date_time = %s;'
    cursor.execute(query2, (flight_num, depart_date_time))
    data2 = cursor.fetchall()

    cursor.close()
    return render_template('staffRate.html', avg=data1, posts=data2, flight_num=flight_num)

@app.route('/staffHome/seating', methods=['GET', 'POST'])
def staffSeat():
    flight_num = request.form['flight_num']
    depart_date_time = request.form['depart_date_time']

    cursor = conn.cursor();
    query1 = 'SELECT name, email\
                from customer natural join ticket\
                where flight_num = %s\
                    and depart_date_time = %s'
    cursor.execute(query1, (flight_num, depart_date_time))
    data1 = cursor.fetchall()

    cursor.close()
    return render_template('staffSeat.html', posts=data1, flight_num=flight_num)

@app.route('/staffHistory', methods=['GET', 'POST'])
def staffHistory():
    name = request.form['name']
    email = request.form['email']
    airline = session['airline']

    cursor = conn.cursor();
    query1 = 'SELECT ticket_id, flight_num, depart_date_time, depart_airport, arrival_date_time, arrival_airport, purchase_date_time\
                FROM ticket natural join flight\
                WHERE email = %s\
                    and airline_name = %s'
    cursor.execute(query1, (email, airline))
    data1 = cursor.fetchall()

    cursor.close()
    return render_template('staffHistory.html', posts=data1, name=name)

@app.route('/staffHome/status', methods=['GET', 'POST'])
def staffStatus():
    username = session['username']
    flight_num = request.form['flight_num']
    depart_date_time = request.form['depart_date_time']
    statusVal = request.form['statusVal']

    cursor = conn.cursor();
    ins = 'UPDATE flight \
            SET delay_status = %s, depart_date_time = depart_date_time\
            WHERE flight_num = %s and depart_date_time = %s'
    cursor.execute(ins, (statusVal, flight_num, depart_date_time))
    conn.commit()
    displayQuery = 'SELECT * \
                FROM flight WHERE flight_num = %s and depart_date_time = %s'
    cursor.execute(displayQuery, (flight_num, depart_date_time))
    data1 = cursor.fetchall()

    cursor.close()
    return render_template('staffHome.html', username = username, posts=data1, filtered=True, statChange=True)


@app.route('/staffHome/filter', methods=['GET', 'POST'])
def staffHomeFilter():
    username = session['username']
    airline = session['airline']
    depAirport = request.form['depAirport']
    arrAirport = request.form['arrAirport']
    date1 = request.form['date1']
    date2 = request.form['date2']

    cursor = conn.cursor();
    query = 'SELECT * \
            FROM flight \
            WHERE airline_name = %(name)s \
                and (depart_airport = %(dep)s or %(dep)s = "") \
                and (arrival_airport = %(arr)s or %(arr)s = "") \
                and (CONVERT(depart_date_time, date) between %(d1)s and %(d2)s);'
    paramFilter = {
        "name" : airline,
        "dep" : depAirport,
        "arr" : arrAirport,
        "d1" : date1,
        "d2" : date2
    }
    cursor.execute(query, paramFilter)
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('staffHome.html',  username = username, posts=data1, filtered = True)

@app.route('/staffAdd')
def staffAdd():
    airline = session['airline']

    cursor = conn.cursor();
    query = 'SELECT airplane_id, seating_capacity, manufacturing_company, age \
            FROM airplane WHERE airline_name = %s'
    cursor.execute(query, (airline))
    data1 = cursor.fetchall()

    return render_template('staffAdd.html', posts=data1)

@app.route('/addFlight', methods=['GET', 'POST'])
def addFlight():
    airline = session['airline']

    flight_num = request.form['flight_num']
    depart_airport = request.form['depart_airport']
    airplane_id = request.form['airplane_id']
    depart_date_time = request.form['depart_date_time']
    arrival_airport = request.form['arrival_airport']
    arrival_date_time = request.form['arrival_date_time']
    base_price = request.form['base_price']
    delay_status = request.form['delay_status']

    cursor = conn.cursor();
    query1 = 'SELECT * FROM flight WHERE flight_num = %s and depart_date_time = %s'
    cursor.execute(query1, (flight_num, depart_date_time))
    data1 = cursor.fetchone()
    error = None
    if(data1):
        #If the previous query returns data, then flight exists
        error = "This flight already exists"
        return render_template('staffAdd.html', error=error)
    else:
        ins1 = 'INSERT into flight values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins1, (flight_num, depart_date_time, airplane_id, airline, depart_airport, arrival_airport, arrival_date_time, base_price, delay_status))
        
        # Must insert tickets based on seating capacity of plane
        query2 = 'SELECT seating_capacity \
                FROM airplane WHERE airplane_id = %s'
        cursor.execute(query2, (airplane_id))
        data2 = int(cursor.fetchone()['seating_capacity'])
        query3 = 'SELECT ticket_id \
                FROM ticket\
                ORDER BY ticket_id DESC\
                LIMIT 1'
        cursor.execute(query3)
        data3 = int(cursor.fetchone()['ticket_id'])
        data3 += 1
        for i in range(data3, data3+data2):
            ins2 = 'INSERT into ticket values(%s, NULL, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL)'
            cursor.execute(ins2, (i, flight_num, depart_date_time))

        conn.commit()
        cursor.close()
        return render_template('staffAdd.html', flight_added=True)

@app.route('/addPort', methods=['GET', 'POST'])
def staffPort():
    name = request.form['name']
    city = request.form['city']
    country = request.form['country']
    port_type = request.form['type']

    cursor = conn.cursor();
    query = 'SELECT * FROM airport WHERE name = %s'
    cursor.execute(query, (name))
    data = cursor.fetchone()
    error = None
    if(data):
        #If the previous query returns data, then airport exists
        error = "This airport already exists"
        return render_template('staffAdd.html', error=error)
    else:
        query1 = 'INSERT into aiport values(%s, %s, %s, %s)'
        cursor.execute(query1, (name, city, country, port_type))
        conn.commit() 
        cursor.close()
        return render_template('staffAdd.html', port_added=True)

@app.route('/addPlane', methods=['GET', 'POST'])
def staffPlane():
    airline = session['airline']

    airplane_id = request.form['airplane_id']
    seat_capacity = request.form['seat_capacity']
    manufacturing_company = request.form['manufacturing_company']
    age = request.form['age']

    cursor = conn.cursor();
    query = 'SELECT * FROM airplane WHERE airplane_id = %s and airline_name = %s'
    cursor.execute(query, (airplane_id, airline))
    data = cursor.fetchone()
    error = None
    if(data):
        #If the previous query returns data, then airport exists
        error = "This airplane already exists"
        return render_template('staffAdd.html', error=error)
    else:
        ins = 'INSERT into airplane values(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (airplane_id, airline, seat_capacity, manufacturing_company, age))
        conn.commit() 
        cursor.close()
        return redirect('/staffPlaneList')

@app.route('/staffPlaneList')
def staffPlaneList():
    airline = session['airline']

    cursor = conn.cursor();
    query = 'SELECT airplane_id, seating_capacity, manufacturing_company, age \
        FROM airplane WHERE airline_name = %s'
    cursor.execute(query, (airline))
    data1 = cursor.fetchall()

    return render_template('staffPlanes.html', posts=data1, airline=airline)

@app.route('/staffAddFlight')
def staffAddFlight():
    airline = session['airline']

    cursor = conn.cursor();
    query = 'SELECT airplane_id, seating_capacity, manufacturing_company, age \
                FROM airplane WHERE airline_name = %s'
    cursor.execute(query, (airline))
    data1 = cursor.fetchall()

@app.route('/staffReport', methods=['GET', 'POST'])
def staffReport():
    airline = session['airline']

   # Find total in past year
    cursor = conn.cursor();
    query1 = "SELECT count(ticket_ID) as total\
                FROM ticket natural join flight\
                WHERE airline_name = %s\
                    and email is not null\
                    and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE()"
    cursor.execute(query1, (airline))
    data1 = cursor.fetchone()

    # Find monthly amount
    query2 = "SELECT date_format(purchase_date_time, '%%M') as month, count(ticket_ID) as m_sold\
                FROM ticket natural join flight\
                WHERE airline_name = %s\
                    and email is not null\
                    and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE()\
                GROUP BY date_format(purchase_date_time, '%%M');"
    cursor.execute(query2, (airline))
    data2 = cursor.fetchall()

    # Find revenue from last year
    query3 = "SELECT sum(sold_price) as rev\
                FROM ticket natural join flight\
                WHERE airline_name = %s\
                    and email is not null\
                    and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE();"
    cursor.execute(query3, (airline))
    data3 = cursor.fetchone()

    # last month
    query4 = "SELECT sum(sold_price) as rev\
                FROM ticket natural join flight\
                WHERE airline_name = %s\
                    and email is not null\
                    and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 MONTH) and CURDATE();"
    cursor.execute(query4, (airline))
    data4 = cursor.fetchone()

    # most frequent customer within the year
    query5 = "WITH flightCount(email, amount) as (\
                    SELECT email, count(ticket_ID)\
                    FROM ticket natural join flight\
                    WHERE airline_name = %s \
                        and email is not NULL\
                        and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 YEAR) and CURDATE() \
                    GROUP by email  ),\
                mostFlights(flights) as (\
                    SELECT max(amount)\
                    FROM flightCount)\
                SELECT name, flights\
                FROM (customer natural join flightCount), mostFlights\
                WHERE flightCount.amount = mostFlights.flights"
    cursor.execute(query5, (airline))
    data5 = cursor.fetchone()

    cursor.close()
    return render_template('staffReport.html', t_sold=data1['total'], posts=data2, y_rev=data3['rev'], m_rev=data4['rev'], y_cust = data5)  

   


@app.route('/staffReport/month', methods=['GET', 'POST'])
def staffReportMonth():
    airline = session['airline']

   # Find total in past year
    cursor = conn.cursor();
    query1 = "SELECT count(ticket_ID) as total\
                FROM ticket natural join flight\
                WHERE airline_name = %s\
                    and email is not null\
                    and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 MONTH) and CURDATE()"
    cursor.execute(query1, (airline))
    data1 = cursor.fetchone()

    # Find monthly amount
    query2 = "SELECT date_format(purchase_date_time, '%%M') as month, count(ticket_ID) as m_sold\
                FROM ticket natural join flight\
                WHERE airline_name = %s\
                    and email is not null\
                    and CONVERT(purchase_date_time, date) between DATE_ADD(CURDATE(), INTERVAL -1 MONTH) and CURDATE()\
                GROUP BY date_format(purchase_date_time, '%%M');"
    cursor.execute(query2, (airline))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('staffReport.html', t_sold=data1['total'], posts=data2)  

@app.route('/staffReport/filter', methods=['GET', 'POST'])
def staffReportFilter():
    airline = session['airline']
    date1 = request.form['date1']
    date2 = request.form['date2']
    
    cursor = conn.cursor();
    query1 = "SELECT count(ticket_ID) as total\
                FROM ticket natural join flight\
                WHERE airline_name = %s\
                    and email is not null\
                    and CONVERT(purchase_date_time, date) between %s and %s;"
    cursor.execute(query1, (airline, date1, date2))
    data1 = cursor.fetchone()

    # Find monthly spending
    query2 = "SELECT date_format(purchase_date_time, '%%M') as month, count(ticket_ID) as m_sold\
                FROM ticket natural join flight\
                WHERE airline_name = %s\
                    and email is not null\
                    and CONVERT(purchase_date_time, date) between %s and %s\
                GROUP BY date_format(purchase_date_time, '%%M');"
    cursor.execute(query2, (airline, date1, date2))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('staffReport.html', t_sold=data1['total'], posts=data2)  


@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('airline')
    session['usertype'] = "Guest"
    return redirect('/')
        
app.secret_key = "please don't find this"
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
