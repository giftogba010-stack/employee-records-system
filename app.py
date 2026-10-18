from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

employees = []

<!DOCTYPE html>
<html><head><title>Employee Records System</title>
<style>body{font-family:Arial;padding:20px;background:#f4f4f4} .box{background:white;padding:20px;border-radius:10px;max-width:600px;margin:auto} input{width:95%;padding:10px;margin:5px 0} button{padding:10px 20px;background:#5b2c6f;color:white;border:none;border-radius:5px} table{width:100%;margin-top:20px} th,td{border:1px solid #ddd;padding:8px}</style>
</head><body><div class="box">
<h2>Employee Records System</h2>
<form method="POST" action="/add">
<input name="name" placeholder="Full Name" required>
<input name="position" placeholder="Position" required>
<input name="email" placeholder="Email" required>
<input name="department" placeholder="Department" required>
<button type="submit">Add Employee</button>
</form>
<table><tr><th>Name</th><th>Position</th><th>Department</th><th>Email</th></tr>
{% for e in employees %}
<tr><td>{{e.name}}</td><td>{{e.position}}</td><td>{{e.department}}</td><td>{{e.email}}</td></tr>
{% endfor %}
</table>
</div></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, employees=employees)

@app.route('/add', methods=['POST'])
def add():
    employees.append({
        'name': request.form['name'],
        'position': request.form['position'],
        'email': request.form['email'],
        'department': request.form['department']
    })
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
