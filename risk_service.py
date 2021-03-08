import queue
import datetime
from netaddr import IPNetwork, IPAddress

from user import User

__author__ = "Christoffer Nielsen"
__credits__ = ["Christoffer Nielsen", "Thomas Cellerier", "Natan Abolafya", "Camilla Alexandersson"]
__version__ = "1.0.0"
__maintainer__ = "Christoffer Nielsen"
__email__ = "nielsenchristoffer93@gmail.com"
__status__ = "Production"


def get_username(log_status, remaining_text_list):
    """ Get the username from remaining_text_list based on log status string.

        Parameters:
        log_status (string): The log status from parsed log file.
        remaining_text_list (list): The remaining text after splitting logfile.

        Returns:
        string: Username
    """
    if log_status == "sshd":
        return remaining_text_list[3]
    elif log_status == "login":
        return remaining_text_list[0]


def get_ip(log_status, remaining_text_list):
    """ Get the IP from remaining_text_list based on log status string.

        Parameters:
        log_status (string): The log status from parsed log file.
        remaining_text_list (list): The remaining text after splitting logfile.

        Returns:
        string: IP-address
    """
    if log_status == "login":
        return remaining_text_list[2]
    elif log_status == "ag_stated" and "'login.client_ip'" in remaining_text_list:
        # Remove ' from string since the string are compared later on.
        return remaining_text_list[4].replace("'", "")


def get_hostname(log_status, remaining_text_list):
    """ Get the hostname from remaining_text_list based on log status string.

        Parameters:
        log_status (string): The log status from parsed log file.
        remaining_text_list (list): The remaining text after splitting logfile.

        Returns:
        string: Hostname
    """
    if log_status == "ag_stated" and "'login.client_name'" in remaining_text_list:
        # Remove ' from string since the string are compared later on.
        return remaining_text_list[4].replace("'", "")


def check_for_failed_logins(log_status, remaining_text_list):
    """ Check whether the login has failed or not.

        Parameters:
        log_status (string): The log status from parsed log file.
        remaining_text_list (list): The remaining text after splitting logfile.

        Returns:
        bool: True if login has failed, otherwise return False.
    """
    if log_status == "sshd":
        if remaining_text_list[0].lower() == "failed":
            return True
        else:
            return False


class RiskService:

    VALID_IP_RANGES = ["192.168.1.1/24", "192.168.128.1/24", "112.112.112.1/24"]

    def __init__(self):
        self.q = queue.Queue()
        self.users = []  # List of user objects.
        self.latest_username = ""
        self.failed_logons_per_day = {}  # Dict of date (key) and failed logon count for that day (value)

    def add_to_queue(self, log_data):
        """ Add log data from POST request to a FIFO queue.

            Parameters:
            log_data (string): The log data from the POST request.
        """
        self.q.put(log_data)

    def count_failed_logons_for_a_day(self, date):
        """ Count the failed logons for the date supplied and increments it value if it already exist in dict.

            Parameters:
            date (date): The failed logon date.
        """
        date_today = datetime.date.today()
        date_1_week_ago = date_today - datetime.timedelta(days=7)

        if date_1_week_ago <= date <= date_today:
            if date not in self.failed_logons_per_day:
                self.failed_logons_per_day[date] = 1
            elif date in self.failed_logons_per_day:
                self.failed_logons_per_day[date] += 1

    def count_failed_logons_for_a_week(self):
        """ Count the failed logons for a week back in time (based on today's date).

            Returns:
            int: failed_logons
        """
        date_today = datetime.date.today()
        date_1_week_ago = date_today - datetime.timedelta(days=7)
        working_date = date_1_week_ago
        failed_logons = 0
        while working_date <= date_today:
            for date in self.failed_logons_per_day:
                if date == working_date:
                    failed_logons += self.failed_logons_per_day[date]

            working_date += datetime.timedelta(days=1)

        return failed_logons

    def get_failed_login_date(self, username):
        """ Get the failed login date for supplied username.

            Parameters:
            username (string): The username to check.

            Returns:
            datetime: user.last_failed_login_date
        """
        for user in self.users:
            if username == user.username:
                return user.last_failed_login_date
        # return False

    def get_successful_login_date(self, username):
        """ Get the successful login date for supplied username.

            Parameters:
            username (string): The username to check.

            Returns:
            datetime: user.last_successful_login_date
        """
        for user in self.users:
            if username == user.username:
                return user.last_successful_login_date
        # return False

    def is_ip_known(self, ip):
        """ Check if IP exist in users known_ips list.

            Parameters:
            ip (string): The IP to check.

            Returns:
            bool: True if IP exist, otherwise return False.
        """
        for user in self.users:
            for ip_number in user.known_ips:
                if ip_number == ip:
                    return True
        return False

    def is_host_known(self, hostname):
        """ Check if hostname exist in users known_hosts list.

            Parameters:
            hostname (string): The hostname to check.

            Returns:
            bool: True if hostname exist, otherwise return False.
        """
        for user in self.users:
            for host in user.known_hostnames:
                if host == hostname:
                    return True
        return False

    def is_user_known(self, username):
        """ Check if username exist in the list of all users.

            Parameters:
            username (string): The username to check.

            Returns:
            bool: True if username exist, otherwise return False.
        """
        for user in self.users:
            if username == user.username:
                return True
        return False

    def is_ip_internal(self, ip):
        """ Check if IP is internal or external.

            Parameters:
            ip (string): The IP to check.

            Returns:
            bool: True if ip is internal, False if it's external.
        """
        for network in self.VALID_IP_RANGES:
            if IPAddress(ip) in IPNetwork(network):
                return True

        return False



    def parse_log_files(self):
        """ Gets the first item in queue and parses it. Looping through every line in string creating Users
        and updating the users value if they already exist.
        """
        # start = time.time()
        while not self.q.empty():
            log_data = self.q.get()
            log_data_lines = log_data.splitlines()

            for line in log_data_lines:

                # Convert date string to datetime
                date_time_str = line[:17]
                date_time_str_date_only = line[:8]
                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y%m%d %H:%M:%S')

                remaining_text_list = line[18:].split()[2:]
                log_status = remaining_text_list.pop(0)

                # Get username from log
                username = get_username(log_status, remaining_text_list)
                if username is not None:
                    self.latest_username = username
                    if username not in (user.username for user in self.users):
                        new_user = User(username)
                        self.users.append(new_user)

                # Get ip from log
                ip = get_ip(log_status, remaining_text_list)
                if ip is not None:
                    for user in self.users:
                        if self.latest_username == user.username:
                            user.add_ip_to_known_ips(ip)

                # Get hostname/computer name from log
                hostname = get_hostname(log_status, remaining_text_list)
                if hostname is not None:
                    for user in self.users:
                        if self.latest_username == user.username:
                            user.add_hostname_to_known_hosts(hostname)

                # Check for failed logins and increments failed logons counter and adds failed/successful dates to user.
                failed_login = check_for_failed_logins(log_status, remaining_text_list)
                if failed_login is not None:
                    for user in self.users:
                        if self.latest_username == user.username:
                            if failed_login:
                                user.add_last_failed_login_date(date_time_obj)
                                user.increment_failed_login()
                                # count_failed_logons_for_a_day needs a date not a datetime object, so we must convert.
                                self.count_failed_logons_for_a_day(
                                    datetime.datetime.strptime(date_time_str_date_only, '%Y%m%d').date())
                            else:
                                user.add_last_successful_login_date(date_time_obj)

            # Loop through every user and print all items.
            # for user in self.users:
            #     print(f"Username: {user.username} Known IPs: {user.known_ips} Known hosts: {user.known_hostnames} "
            #           f"Last Successful Login: {user.last_successful_login_date} "
            #           f"Last Failed Login: {user.last_failed_login_date} "
            #           f" Failed login attempts: {user.failed_login_count}")

            # Done with this task in queue.
            self.q.task_done()

        # print("Elapsed Time: %s" % (time.time() - start))
