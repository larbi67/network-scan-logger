#!/usr/bin/env python3
"""
Network Scanner Logger
Author : Larbi OUIYZME
Version: 1.0
Description: Passive script to log public IP and devices from ARP table into a timestamped log file.
MIT License: which is open, permissive, and widely accepted.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import socket
import subprocess
import requests
from datetime import datetime

# Log file path (in the same folder as the script)
LOG_FILE = os.path.join(os.path.dirname(__file__), "network_scan.log")

def get_public_ip():
    print("Getting public IP...")
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        print(f"Public IP found: {ip}")
        return ip
    except Exception as e:
        print(f"Error getting public IP: {e}")
        return "Unavailable"

def get_arp_table():
    print("Getting ARP table...")
    entries = []
    try:
        # Decode using 'cp1252' to support Windows character encoding
        output = subprocess.check_output("arp -a", shell=True).decode('cp1252')
        for line in output.splitlines():
            if "-" in line or ":" in line:
                parts = line.split()
                if len(parts) >= 3:
                    ip = parts[0].strip("()")
                    mac = parts[1] if '-' in parts[1] or ':' in parts[1] else parts[2]
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        hostname = "Unknown"
                    entries.append((ip, mac, hostname))
        print(f"Found {len(entries)} ARP entries.")
    except Exception as e:
        print(f"Error reading ARP table: {e}")
        entries.append(("Error", "", ""))
    return entries

def log_results():
    print(f"Writing results to {LOG_FILE}")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n[{timestamp}] Network Scan\n")
            
            public_ip = get_public_ip()
            f.write(f"Public IP: {public_ip}\n")

            f.write("Local ARP Table:\n")
            arp_entries = get_arp_table()
            for ip, mac, hostname in arp_entries:
                f.write(f" - IP: {ip}\tMAC: {mac}\tHostname: {hostname}\n")

            f.write("-" * 60 + "\n")
        print("Log written successfully.")
    except Exception as e:
        print(f"Failed to write log file: {e}")

if __name__ == "__main__":
    print("Starting network scan...")
    log_results()
    print("Scan finished.")
