from flask import Flask, request, jsonify
import datetime


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

# Has the user ever logged in. return true/false
@app.route('/IsUserKnown')
def is_user_known():
    # if key doesn't exist, returns None
    username = request.args.get('username')
    return_bool = False

    if username == "UserA":
        return_bool = True

    return jsonify(return_bool)

# Has the computer/client been seen before. return true/false
@app.route('/IsClientKnown')
def is_client_known():
    # if key doesn't exist, returns None
    host_name = request.args.get('hostname')
    return_bool = False

    if host_name == "computer1":
        return_bool = True

    return jsonify(return_bool)

# Has the connecting ip ever been seen before. return true/false
@app.route('/IsIPKnown')
def is_ip_known():
    # if key doesn't exist, returns None
    ip = request.args.get('ip')
    return_bool = False

    if ip == "192.168.1.1":
        return_bool = True

    return jsonify(return_bool)

# Is the connecting ip internal or external, return true/false
@app.route('/IsIPInternal')
def is_ip_internal():
    # if key doesn't exist, returns None
    ip = request.args.get('ip')
    return_bool = False

    if ip == "192.168.1.2":
        return_bool = True

    return jsonify(return_bool)

# Last successful login date for given user. Return a Datetime object.
@app.route('/LastSuccessfulLoginDate')
def last_successful_login_date():
    # if key doesn't exist, returns None
    username = request.args.get('username')
    date = datetime.datetime.now()

    return jsonify(date)

# Last failed login date for given user. Return a Datetime object.
@app.route('/LastFailedLoginDate')
def last_failed_login_date():
    # if key doesn't exist, returns None
    username = request.args.get('username')
    date = datetime.datetime.now()

    return jsonify(date)

# Failed login counts for given user. Return a Integer object.
@app.route('/FailedLoginCountLastWeek')
def failed_login_counts_last_week():
    failed_logon_attempts = 4
    return jsonify(failed_logon_attempts)


@app.route("/log", methods=['POST'])
def get_log_data():
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        print(data)

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)


