import os
import re
import time
import logging
import subprocess
import getpass

class SSHMonitor:
    def __init__(self):
        self.logfile = self.detect_logfile()
        self.offset = 0
        self.username = getpass.getuser()

        self.logfile_local = f"/home/{self.username}/.ssh_login.log"
        self.setup_logging()

        # Regex (portable)
        self.accepted_re = re.compile(
            r"Accepted password for (\S+) from ([\d.]+)"
        )
        self.failed_re = re.compile(
            r"Failed password for (\S+) from ([\d.]+)"
        )

    def detect_logfile(self):
        if os.path.exists("/var/log/auth.log"):
            return "/var/log/auth.log"
        elif os.path.exists("/var/log/secure"):
            return "/var/log/secure"
        else:
            raise FileNotFoundError("No SSH auth log found")

    def setup_logging(self):
        logging.basicConfig(
            filename=self.logfile_local,
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
        )

    def send_notification(self, message):
        try:
            subprocess.Popen(
                ["notify-send", "SSH Login Monitor", message, "-u", "critical"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except:
            pass  # Safe on servers

    def monitor(self):
        with open(self.logfile, "r") as f:
            f.seek(0, os.SEEK_END)
            self.offset = f.tell()

        print(f"[+] Monitoring SSH log: {self.logfile}")

        while True:
            with open(self.logfile, "r") as f:
                f.seek(self.offset)
                lines = f.readlines()
                self.offset = f.tell()

            for line in lines:
                acc = self.accepted_re.search(line)
                fail = self.failed_re.search(line)

                if acc:
                    user, ip = acc.groups()
                    msg = f"Successful SSH login: {user} from {ip}"
                    print(msg)
                    logging.info(msg)
                    self.send_notification(msg)

                elif fail:
                    user, ip = fail.groups()
                    msg = f"Failed SSH login: {user} from {ip}"
                    print(msg)
                    logging.warning(msg)
                    self.send_notification(msg)

            time.sleep(1)


if __name__ == "__main__":
    os.system("clear")
    print("SSH Monitoring started...\n")

    try:
        monitor = SSHMonitor()
        monitor.monitor()
    except Exception as e:
        print(f"[!] Error: {e}")
