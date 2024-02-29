import subprocess
import re
import time
import logging
import os

class Monitor:
    def __init__(self):
        self.ip = []
        self.logfile = "/var/log/auth.log"
        self.sent_notifications = set() 
        self.last_timestamp = None
        self.log_setup()
        
    def log_setup(self):
        logging.basicConfig(filename=f'/home/{os.getlogin()}/.ssh_login.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    def log_fetch(self):
        try:
            with open(self.logfile, 'r') as file:
                last_lines = file.readlines()[-3:]  
                return last_lines
        except Exception as e:
            print(f"Error fetching log: {e}")
            return []

    def extract_username(self):
        try:
            command = subprocess.Popen(['ls', '/home/'], stdout=subprocess.PIPE)
            output, _ = command.communicate()
            users = output.decode().strip().split("\n")
            return users
        except Exception as e:
            print(f"Error extracting username: {e}")
            return []

    def check(self):
        regex_accepted = r"(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\w+)-(\d+)\s(\w+)\[(\d+)\]:\sAccepted\spassword\sfor\s(\w+)\sfrom\s([\d\.]+)\sport\s(\d+)\sssh(\d+)"
        regex_failed = r"(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\w+)-(\d+)\s(\w+)\[(\d+)\]:\sFailed\spassword\sfor\s(\w+)\sfrom\s([\d\.]+)\sport\s(\d+)\sssh(\d+)"
        try:
            last_logs = self.log_fetch()
            for last_log in last_logs:
                if last_log:
                    match = re.match(r'(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}).*', last_log)
                    if match:
                        timestamp = match.group(1)
                        if timestamp not in self.sent_notifications:
                            self.sent_notifications.add(timestamp)
                            accepted = re.match(regex_accepted, last_log)
                            rejected = re.match(regex_failed, last_log)
                            if accepted:
                                username = accepted.group(6)
                                ip_address = accepted.group(7)
                                # print(f"Successful login: {username} from {ip_address}")
                                self.send_notification(f"{username} logged in from {ip_address}")
                                self.log_activity(f"Successful login: {username} from {ip_address}")
                            elif rejected:
                                username = rejected.group(6)
                                ip_address = rejected.group(7)
                                # print(f"Failed login attempt: {username} from {ip_address}")
                                self.send_notification(f"{username} is trying to SSH into your system")
                                self.log_activity(f"Failed login attempt: {username} from {ip_address}")
        except Exception as e:
            print(f"Error checking log: {e}")

    def send_notification(self, message):
        try:
            subprocess.Popen(['notify-send', 'SSH Login Monitor', message,'-u','critical'])
        except Exception as e:
            print(f"Error sending notification: {e}")

    def log_activity(self, message):
        try:
            logging.info(message)
        except Exception as e:
            print(f"Error logging activity: {e}")


monitor_instance = Monitor()
os.system('cls' if os.name == 'nt' else 'clear')
print("SSH Monitoring started.")
while True:
    monitor_instance.check()
    time.sleep(1)
