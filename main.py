from flask import Flask, render_template, request, url_for, redirect

import data_manager

app = Flask(__name__)
CITIES = ["Bucharest", "Budapest", "Kraków", "Miskolc", "Warsaw"]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mentors')
def mentors_list():
    mentor_last_name = request.args.get('mentor-last-name')
    mentor_city = request.args.get('city-name')

    if mentor_last_name:
        mentors = data_manager.get_mentors_by_last_name(mentor_last_name)
    elif mentor_city:
        mentors = data_manager.get_mentors_by_city(mentor_city)
    else:
        mentors = data_manager.get_mentors()

    # We get back a list of dictionaries from the data_manager (for details check 'data_manager.py')
    return render_template('mentors.html', mentors=mentors, cities = CITIES)

@app.route('/applicants-phone', methods=['GET', 'POST'])
def applicants_phone():
    column_names = ['Full name', 'Phone number']
    applicant_name = request.form.get('applicant-name')
    applicant_email = request.form.get('email-ending')
    if applicant_name:
        applicants = data_manager.get_applicants_by_name(applicant_name)
    elif applicant_email:
        applicants = data_manager.get_applicant_data_by_email_ending(applicant_email)
    else:
        applicants = data_manager.get_applicants()
    return render_template('applicants_phone.html', applicants_details=applicants, column_names=column_names)

@app.route('/applicants', methods=['GET', 'POST'])
def applicants_list():
    column_names = ['First name', 'Last name', 'Phone number', 'Email', 'Application code']
    if request.method == 'POST':
        domain_to_delete = request.form.get('email-ending')
        data_manager.delete_by_domain(domain_to_delete)
        redirect('/applicants')

    applicants = data_manager.get_full_applicants()
    return render_template('applicants.html', applicants_details=applicants, table_headers=column_names)

@app.route('/applicants/<code>', methods=['GET', 'POST'])
def display_applicant(code):
    applicant = data_manager.get_applicant_by_code(code)
    if request.method == "POST":
        new_phone = request.form.get("new-phone")
        data_manager.update_phone(code, new_phone)

    return render_template('applicant.html', applicant_details=applicant)

@app.route('/applicants/<code>/delete')
def delete_applicant(code):
    data_manager.delete_applicant(code)
    return redirect('/applicants')

@app.route('/add-applicant', methods = ["GET","POST"])
def add_applicant():
    if request.method == "POST":
        applicant = request.form
        data_manager.add_applicant(applicant)
        return redirect('/applicants')
    return render_template('add_applicant.html')

if __name__ == '__main__':
    app.run(debug=True)
