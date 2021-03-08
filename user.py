__author__ = "Christoffer Nielsen"
__credits__ = ["Christoffer Nielsen", "Thomas Cellerier", "Natan Abolafya", "Camilla Alexandersson"]
__version__ = "1.0.0"
__maintainer__ = "Christoffer Nielsen"
__email__ = "nielsenchristoffer93@gmail.com"
__status__ = "Production"


class User:

    def __init__(self, username):
        self.username = username
        self.known_hostnames = []
        self.known_ips = []
        self.last_successful_login_date = None
        self.last_failed_login_date = None
        self.failed_login_count = 0

    def increment_failed_login(self):
        """Increase users failed login count by 1.
        """
        self.failed_login_count += 1

    def add_hostname_to_known_hosts(self, hostname):
        """Add hostname to users known hostnames.

            Parameters:
            hostname (string): The hostname to add.
        """
        if not self.is_hostname_known(hostname):
            self.known_hostnames.append(hostname)

    def add_ip_to_known_ips(self, ip):
        """Add IP to users known IPs.

            Parameters:
            ip (string): The IP to add.
        """
        if not self.is_ip_known(ip):
            self.known_ips.append(ip)

    def is_hostname_known(self, hostname):
        """Check if supplied hostname exist in users known hostnames.

            Parameters:
            hostname (string): The hostname to check.

            Returns:
            bool: True if it does exist, False if it doesn't.
        """
        for known_host in self.known_hostnames:
            if known_host == hostname:
                return True
        return False

    def is_ip_known(self, ip):
        """Check if supplied IP exist in users known IPs.

            Parameters:
            ip (string): The IP to check.

            Returns:
            bool: True if it does exist, False if it doesn't.
        """
        for known_ip in self.known_ips:
            if known_ip == ip:
                return True
        return False

    def add_last_successful_login_date(self, date):
        """Add last successful login date to user.

            Parameters:
            date (datetime): The date to add.
        """
        if self.last_successful_login_date is None:
            self.last_successful_login_date = date
        elif date >= self.last_failed_login_date:
            self.last_successful_login_date = date

    def add_last_failed_login_date(self, date):
        """Add last failed login date to user.

            Parameters:
            date (datetime): The date to add.
        """
        if self.last_failed_login_date is None:
            self.last_failed_login_date = date
        elif date >= self.last_failed_login_date:
            self.last_failed_login_date = date
