#!/usr/bin/env python

"""RESTFUL RISK API, parsing log files on POST request and add/update user data with data from log file.
Can then later be used to send GET request based on username, ip, hostname etc and return the risk.
"""

from threading import Thread

from flask import Flask, request, jsonify
from risk_service import RiskService

__author__ = "Christoffer Nielsen"
__credits__ = ["Christoffer Nielsen", "Thomas Cellerier", "Natan Abolafya", "Camilla Alexandersson"]
__version__ = "1.0.0"
__maintainer__ = "Christoffer Nielsen"
__email__ = "nielsenchristoffer93@gmail.com"
__status__ = "Production"

# I've been using postman for testing the GET and POST requests. Just add the data from generated log_file as raw
# data to a POST request to http://localhost:5000/log.

app = Flask(__name__)
risk_svc = RiskService()


# Has the user ever logged in. return true/false
@app.route('/risk/isuserknown')
def is_user_known():
    username = request.args.get('username')
    return_bool = risk_svc.is_user_known(username)

    return jsonify(return_bool)


# Has the computer/client been seen before. return true/false
@app.route('/risk/isclientknown')
def is_client_known():
    host_name = request.args.get('hostname')
    return_bool = risk_svc.is_host_known(host_name)

    return jsonify(return_bool)


# Has the connecting ip ever been seen before. return true/false
@app.route('/risk/isipknown')
def is_ip_known():
    ip = request.args.get('ip')
    return_bool = risk_svc.is_ip_known(ip)

    return jsonify(return_bool)


# Is the connecting ip internal or external, return true/false
@app.route('/risk/isipinternal')
def is_ip_internal():
    ip = request.args.get('ip')
    return_bool = risk_svc.is_ip_internal(ip)

    return jsonify(return_bool)


# Last successful login date for given user. Return a Datetime object.
@app.route('/risk/lastsuccessfullogindate')
def last_successful_login_date():
    username = request.args.get('username')
    date = risk_svc.get_successful_login_date(username)

    return jsonify(date)


# Last failed login date for given user. Return a Datetime object.
@app.route('/risk/lastfailedlogindate')
def last_failed_login_date():
    username = request.args.get('username')
    date = risk_svc.get_failed_login_date(username)

    return jsonify(date)


# Failed login counts for given user. Return a Integer object.
@app.route('/risk/failedlogincountlastweek')
def failed_login_counts_last_week():
    return jsonify(risk_svc.count_failed_logons_for_a_week())


# Post route, all posts
@app.route("/log", methods=['POST'])
def get_log_data():
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        risk_svc.add_to_queue(data)

        # Start a new thread parsing the data, so we don't hang the post requests.
        worker = Thread(target=risk_svc.parse_log_files, daemon=True)
        worker.start()

    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
