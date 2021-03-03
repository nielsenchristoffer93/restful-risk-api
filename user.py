class User:

    def __init__(self, username, last_ip_used, last_client_used,
                 last_successful_login_date, last_failed_login_date,
                 failed_login_count_last_week):
        self.username = username
        self.last_ip_used = last_ip_used
        self.last_client_used = last_client_used
        self.last_successful_login_date = last_successful_login_date
        self.last_failed_login_date = last_failed_login_date
        self.failed_login_count_last_week = failed_login_count_last_week
