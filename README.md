# Building a Domain Name Monitor with Python and Verisign's RDAP API

Have you ever wanted to snag a specific domain name that's already taken? I created a Python script that monitors domain names and alerts you when they become available. Let's break down how it works!

## What Does It Do?

This script continuously monitors a list of domain names using Verisign's RDAP (Registration Data Access Protocol) API. It checks each domain's status at regular intervals and sends desktop notifications when a domain's status changes – particularly when it becomes available for registration.

<Image
  src="screenshot.png"
  alt="OpenGraph image"
  width={640}
  height={500}
/>

## Key Features

- Real-time domain availability monitoring
- Desktop notifications for status changes
- Detailed domain information including:
  - Registration dates
  - Expiration dates
  - Current registrar
- Error handling and logging
- Configurable checking intervals

## Requirements

- Python 3.7+
- Required packages:
  ```
  requests>=2.28.0
  plyer>=2.1.0
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/GeekAbderrahmen/Domains-Real-Time-Tracker.git
   cd domain-monitor
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Edit the `domains_to_monitor` list to include the domains you want to monitor:
   ```
    domains_to_monitor = [
        "example1.com",
        "example2.com",
        "example3.com"
    ]
   ```

2. _[optional]_ Edit the `interval` of polling if needed:
   ```
   def monitor_domains(self, domains: List[str], check_interval: int = 60):
   ```

3. Run the script:
   ```bash
   python domain_monitor.py
   ```

## How It Works

The script is built around the `VerisignDomainMonitor` class, which handles three main tasks:

1. **Status Checking**: The `check_domain_status()` method queries Verisign's RDAP API for each domain. A 404 response means the domain is available, while a 200 response provides detailed registration information.

2. **State Management**: The script maintains a record of each domain's previous state, allowing it to detect changes in availability or status.

3. **Notifications**: When a domain's status changes (especially when it becomes available), the script sends a desktop notification and prints the update to the console.


## Practical Applications

This tool is particularly useful for:
- Domain name investors
- Business owners waiting for specific domains
- Marketing teams monitoring brand-related domains
- Developers needing specific domain names for projects

The script runs continuously until interrupted, checking domains at regular intervals (default: 60 seconds) and keeping you informed of any changes in their status.

## Technical Notes

The script uses several Python libraries:
- `requests` for API calls
- `plyer` for desktop notifications
- Built-in `logging` for error tracking
- `datetime` for timestamp management

Remember that while this script is powerful, it should be used responsibly and in accordance with Verisign's API usage policies.

---

This code provides a practical solution for anyone needing to monitor domain availability without constantly checking manually. It's both efficient and user-friendly, making domain monitoring a hands-off process.