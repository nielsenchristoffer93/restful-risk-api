import queue
from user import User


class RiskService:

    def __init__(self):
        self.q1 = queue.Queue()
        self.users = []

    def add_to_queue(self, log_text):
        self.q1.put(log_text)  # this will additem 10 to the queue.
        self.parse_log_file()

    def add_20_items_to_queue(self, log_text):
        for i in range(20):
            self.q1.put(log_text)  # this will additem from 0 to 20 to the queue.

    def get_all_queued_items(self):
        while not self.q1.empty():
            print(f"The value is {self.q1.get()}")  # get() will remove the item from the queue.

    def parse_log_file(self):
        log_data = self.q1.get()
        log_data_list = log_data.splitlines()
        for line in log_data_list:
            date = line[:17]  # get date for each line.
            remaining_line = line[42:]  # get everything after for example [4f8a7f94:533e229f]
            self.check_string_for_type(remaining_line)
            # print(remaining_line)


    # def check_string_for_type(self, remaining_line):
    #     user = ""
    #     ip = ""
    #     client = ""
    #     if "sshd" in remaining_line:
    #         if "Failed password" in remaining_line:
    #             user = remaining_line[25:].split()[0]
    #             #print(f"FAILED LOGIN FOR USER {user}, INCREASE FAIL COUNTER FOR USER!")
    #         elif "Accepted password" in remaining_line:
    #             user = remaining_line[27:].split()[0]
    #             #print(f"SUCCESSFUL LOGIN FOR USER {user}")
    #     elif "ag_stated" in remaining_line:
    #         print("login.client_ip" in remaining_line)
    #         if "login.client_ip" in remaining_line:
    #             ip = remaining_line[48:].replace("'", "")
    #             print(f"user: {user} with ip {ip}")
    #         elif "login.client_name" in remaining_line:
    #             client = remaining_line[50:].replace("'", "")
    #             print(f"user: {user} with client-name {client}")
    #     elif "login" in remaining_line:
    #         user = remaining_line[6:].split()[0]
    #         print(f"USER {user}")
