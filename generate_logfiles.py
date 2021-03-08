import random
from random_username.generate import generate_username

__author__ = "Christoffer Nielsen"
__credits__ = ["Christoffer Nielsen", "Thomas Cellerier", "Natan Abolafya", "Camilla Alexandersson"]
__version__ = "1.0.0"
__maintainer__ = "Christoffer Nielsen"
__email__ = "nielsenchristoffer93@gmail.com"
__status__ = "Production"

# This is just a python script for generating many logfiles with different usernames, ips and dates.


middle_text = " 09:06:41 vm5 [4f8a7f94:533e22a3] "
dates = []
ips = []

usernames = generate_username(1000)

for j in range(1, 4):
    for i in range(1, 28):
        if j == 3 and i == 6:
            break
        for _ in range(1, 50):
            if i < 10:
                date_str = "2021" + "0" + str(j) + "0" + str(i)
            else:
                date_str = "2021" + "0" + str(j) + str(i)

            dates.append(date_str)

for a in range(1, 11):
    for _ in range(5):
        # random_ip = str(random.randint(100, 255)) + "." + str(random.randint(100, 255)) + "." + \
        #            str(random.randint(100, 255)) + "." + str(random.randint(100, 255))
        random_ip = "192.168.128." + str(random.randint(100, 110))
        ips.append(random_ip)

    log_file = ""
    for _ in range(1):
        for date in dates:

            username = random.choice(usernames)
            ip = random.choice(ips)
            random_computer = random.choice(ips)
            for i in range(1, 6):
                log_file += date + middle_text
                if i == 1:
                    log_file += "sshd Failed password for " + username + " from " + ip + " port 57795 shh2\n"
                elif i == 2:
                    log_file += "sshd Accepted password for " + username + " from " + ip + " port 57795 shh2\n"
                elif i == 3:
                    log_file += "login " + username + " from " + ip + " (password)\n"
                elif i == 4:
                    log_file += f"ag_stated Client attribute: 'login.client_ip' = '{ip}'\n"
                elif i == 5:
                    log_file += f"ag_stated Client attribute: 'login.client_name' = '{random_computer}'\n"

    f = open(f"log_file_{a}.txt", mode="w")
    f.write(log_file)
    f.close()
