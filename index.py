import requests
import time
from datetime import datetime
from typing import List, Dict
import logging
from plyer import notification

class VerisignDomainMonitor:
    def __init__(self):
        self.base_url = "https://rdap.verisign.com/com/v1/domain"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.domain_states = {}

    def check_domain_status(self, domain: str) -> Dict:
        """
        Check domain status using Verisign RDAP API
        Returns: Dictionary with domain status info
        """
        try:
            url = f"{self.base_url}/{domain}"
            response = requests.get(url)
            
            if response.status_code == 404:
                return {"available": True, "status": "available"}
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", [])
                events = data.get("events", [])
                
                # Get registration and expiration dates
                registration_date = next((e["eventDate"] for e in events if e["eventAction"] == "registration"), None)
                expiration_date = next((e["eventDate"] for e in events if e["eventAction"] == "expiration"), None)
                
                return {
                    "available": False,
                    "status": status,
                    "registrar": data.get("entities", [{}])[0].get("vcardArray", [[],[]])[1][1][3] if data.get("entities") else None,
                    "registration_date": registration_date,
                    "expiration_date": expiration_date
                }
            
            return {"available": False, "status": "error", "error": f"Status code: {response.status_code}"}
            
        except Exception as e:
            self.logger.error(f"Error checking {domain}: {str(e)}")
            return {"available": False, "status": "error", "error": str(e)}

    def send_notification(self, domain: str, message: str):
        """Send desktop notification"""
        try:
            notification.notify(
                title=f"Domain Status: {domain}",
                message=message,
                app_icon=None,
                timeout=10,
            )
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {message}")
        except Exception as e:
            print(f"Failed to send notification: {str(e)}")

    def monitor_domains(self, domains: List[str], check_interval: int = 60):
        """
        Monitor domains for status changes
        """
        print("Starting domain monitoring using Verisign RDAP API...")
        
        # Initialize domain states
        for domain in domains:
            initial_status = self.check_domain_status(domain)
            self.domain_states[domain] = initial_status
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Initial status for {domain}:")
            print(f"Available: {initial_status['available']}")
            print(f"Status: {initial_status.get('status', 'unknown')}")
            if not initial_status['available']:
                print(f"Registrar: {initial_status.get('registrar', 'unknown')}")
                print(f"Registration Date: {initial_status.get('registration_date', 'unknown')}")
                print(f"Expiration Date: {initial_status.get('expiration_date', 'unknown')}")

        active_domains = domains.copy()

        while active_domains:
            for domain in active_domains[:]:
                current_time = datetime.now().strftime('%H:%M:%S')
                previous_status = self.domain_states[domain]
                current_status = self.check_domain_status(domain)
                
                status_changed = (
                    previous_status.get('available') != current_status.get('available') or
                    previous_status.get('status') != current_status.get('status')
                )
                
                if status_changed:
                    if current_status['available']:
                        message = f"🎉 {domain} is now AVAILABLE for registration!"
                        self.send_notification(domain, message)
                    elif previous_status['available'] and not current_status['available']:
                        message = (f"❌ {domain} has been REGISTERED by "
                                 f"{current_status.get('registrar', 'someone')}")
                        self.send_notification(domain, message)
                    
                    print(f"\n[{current_time}] Status change for {domain}:")
                    print(f"Previous: {previous_status.get('status', 'unknown')}")
                    print(f"Current: {current_status.get('status', 'unknown')}")
                else:
                    print(f"[{current_time}] Checking {domain}: No change")
                
                self.domain_states[domain] = current_status
            
            if active_domains:
                time.sleep(check_interval)

def main():
    domains_to_monitor = [
        "example1.com",
        "example2.com",
        "example3.com"
    ]
    
    monitor = VerisignDomainMonitor()
    try:
        monitor.monitor_domains(domains_to_monitor)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()