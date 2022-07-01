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

#Define a route to hello function
@app.route('/')
def start():
    return render_template('index.html')

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
def customerHome():
    
    email = session['username']
    cursor = conn.cursor();
    query = 'SELECT flight_num, airline_name, airplane_ID, depart_date_time, depart_airport, arrival_date_time, arrival_airport, delay_status FROM ticket natural join future_flight WHERE email = %s'
    cursor.execute(query, (email))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('customerHome.html', posts=data1)


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

@app.route('/staffHome/filter', methods=['GET', 'POST'])
def staffHomeFilter():
    username = session['username']
    depAirport = request.form['depAirport']
    arrAirport = request.form['arrAirport']
    date1 = request.form['date1']
    date2 = request.form['date2']
    print(date1, "\n", date2)
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

@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('airline')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
