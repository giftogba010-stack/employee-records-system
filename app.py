from flask import Flask, render_template_string, request, redirect, url_for
app = Flask(__name__)
employees = []
HTML = """<html><head><title>Employee Records System</title></head><body style="font-family:Arial;padding:20px"><h2>Employee Records System</h2><form method="POST" action="/add"><input name="name" placeholder="Full Name" required><br><br><input name="position" placeholder="Position" required><br><br><input name="email" placeholder="Email" required><br><br><input name="department" placeholder="Department" required><br><br><button>Add Employee</button></form><hr>{% for e in employees %}<p>{{e.name}} - {{e.position}} - {{e.department}} - {{e.email}}</p>{% endfor %}</body></html>"""
@app.route('/')
def home():
    return render_template_string(HTML, employees=employees)
@app.route('/add', methods=['POST'])
def add():
    employees.append({'name': request.form['name'], 'position': request.form['position'], 'email': request.form['email'], 'department': request.form['department']})
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run()
