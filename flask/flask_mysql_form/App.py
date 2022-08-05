from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


# Configure MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey' # Tell how our session will be configured (this starts the sessions)
# Defining our Routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall() # To obtain data from our query above
    return render_template('index.html', contacts = data) # Pass data to tbody in index.html

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        mysql.connection.commit()    
        # Request is a function from flask
        # Here we're getting data from the request made in the website
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']    
        # MySQL, working with a cursor
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()   
        flash('Contact Added Successfully')        
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts where id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0]) # 0 just to get the right array we need

@app.route('/update/<id>', methods = ['POST'])
# We'll get value here through URL parameters coming thanks to 'name' attribute in form
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone= %s
        WHERE id= %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact Successfully Updated')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>') # This route receive a parameter, to delete specific id
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id)) # In position 0 we'll pass id, similar to %s
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))
 
if __name__ == '__main__':
    app.run(port = 3000, debug = True)   