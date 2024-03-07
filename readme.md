
# Windows Service Status Automation using Python, Dynamically

WindowsService-Status-Automation is a Python-based project designed to automate the monitoring and management of Windows Services. This project aims to simplify the process for system administrators, IT professionals, and developers who need to keep an eye on the status of various services running on Windows operating systems. By automating routine checks and actions, this project helps in ensuring that critical services are always up and running, thus minimizing downtime and enhancing system reliability.


## Features

- Automated Monitoring: Continuously checks the status of specified Windows Services and logs their current state, providing real-time monitoring capabilities.
- Email Notifications: Sends automated email alerts whenever a service stops running, encounters an error, or changes its status unexpectedly, ensuring that you are always informed about the health of your services.
- Service Management: Allows for automated start, stop, pause, and resume actions on services based on predefined rules or schedules, facilitating proactive management and maintenance.
- Logging and Reporting: Generates detailed logs and reports on the status and health of monitored services, aiding in troubleshooting and analysis.
- Customizable Monitoring Intervals: Configurable monitoring intervals to balance between real-time responsiveness and system resource optimization.
- User-Friendly Configuration: Easy-to-use configuration files for setting up monitored services, notification preferences, and other parameters without the need for extensive coding knowledge.


## Run Locally

Prerequisites
- Python 3.x installed on your system
- Access to a Windows environment with administrative privileges
- An SMTP server for sending email notifications, in our case we will be using smtp.gmail.com

Clone the project

```python
  git clone https://github.com/methedjangoguy/WindowsService-Status-Automation.git
```

Go to the project directory

```python
  cd WindowsService-Status-Automation
```

Install dependencies

```python
  pip install -r requirements.txt
```
Configure the .Config/config.json file
```json
{
   "jsonfile": "service_checks.json",
   "services": ["your", "service","names"],
   "monitoring_interval":30,
   "receiver_emails": ["list","of","receipent","emails"],
   "cc_emails": ["list","of","cc","emails"],
   "host": "smtp.gmail.com",
   "sender_email": "your@gmail.com",
   "password":"yourapppassword"
}
```

Start the application

```python
  python main.py
```


## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repository and create a pull request. You can also simply open an issue with the tag "enhancement".

- Fork the Project
- Create your Feature Branch (git checkout -b feature/AmazingFeature)
- Commit your Changes (git commit -m 'Add some AmazingFeature')
- Push to the Branch (git push origin feature/AmazingFeature)
- Open a Pull Request


## Authors

- [@methedjangoguy](https://github.com/methedjangoguy)

