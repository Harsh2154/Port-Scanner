# Port Scanner

A simple, multithreaded Python port scanner that allows you to scan a single port or a range of ports for open services. The tool attempts to grab banners for services running on common ports like HTTP, HTTPS, SSH, MySQL, PostgreSQL, and more.

Open ports are highlighted in red, and you can optionally save the results in a text file.

## Features

- Scans a single port or a range of ports.
- Supports common ports like SSH (22), HTTP (80), HTTPS (443), MySQL (3306), PostgreSQL (5432), and more.
- Attempts to grab banners for known services.
- Outputs results in color (red for open ports).
- Optionally saves the results to a file.

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
