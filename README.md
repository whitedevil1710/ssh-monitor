# SSH Login Monitor

This Python script monitors SSH login activities on a system by parsing the authentication logs (`/var/log/auth.log`). It sends notifications for both successful and failed login attempts and logs these activities to a file for future reference.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/whitedevil1710/ssh-monitor.git
   ```

2. Navigate to the directory:
   ```bash
   cd ssh-login-monitor
   ```

3. Run the script:
   ```bash
   python ssh_login_monitor.py
   ```

## Requirements

- Python 3.x
- Linux environment (tested on Ubuntu)

## Usage

The script runs indefinitely, continuously monitoring the SSH login activities. Notifications are sent for both successful and failed login attempts. Successful logins are logged as "Successful login" and failed attempts as "Failed login attempt" in the `.ssh_login.log` file in the user's home directory.

## Customization

You can customize the following parameters in the script:

- Log file path: Modify the `logfile` attribute in the `Monitor` class to specify a different log file path if needed.
- Notification settings: Adjust the notification settings in the `send_notification` method to customize the appearance or behavior of notifications.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests with any improvements, bug fixes, or feature enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
