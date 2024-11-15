# Port Scanner

A simple, multithreaded Python port scanner that allows you to scan a single port or a range of ports for open services. The tool attempts to grab banners for services running on common ports like HTTP, HTTPS, SSH, MySQL, PostgreSQL, and more.

Open ports are highlighted in red, and you can optionally save the results in a text file.

## Features

- Scans a single port or a range of ports.
- Supports common ports like SSH (22), HTTP (80), HTTPS (443), MySQL (3306), PostgreSQL (5432), and more.
- Attempts to grab banners for known services.
- Outputs results in color (red for open ports).
- Optionally saves the results to a file.

##Usage

When you run the script, the following prompts will appear:

    1.Target IP: Enter the IP address of the system you want to scan.
    2.Scan Type: Choose whether to scan a specific port or a range of ports.
    3.Port Range: If you choose "range", you'll need to provide a starting and ending port.
    4.File Output: You can choose whether to save the results to a file.


## Prerequisites

- Python 3.x (preferably Python 3.6 or higher).
- `ssl` and `socket` libraries are required (both are part of the Python standard library, so no additional installation is needed).

## Installation

1. **Clone the repository:**

   Open your terminal and run the following command:

   ```bash
   git clone https://github.com/yourusername/Port-Scanner.git
   cd Port-Scanner
   python ports_scanner.py

Sample Input:
```bash
   Enter the target IP: 192.168.1.1
   Do you want to scan a specific port or a range of ports? (specific/range): range
   Enter start port: 20
   Enter end port: 80
   Do you want to store open ports in a file? (yes/no): yes
   Enter the filename (e.g., open_ports.txt): scan_results.txt
```

Sample Output:
 ```bash
   Scanning ports 20-80 on 192.168.1.1... Please wait.
   Port 22 is open (SSH) - Banner: SSH-2.0-OpenSSH_8.0
   Port 80 is open (HTTP) - Banner: Apache/2.4.41 (Ubuntu)
   Results stored in scan_results.txt

