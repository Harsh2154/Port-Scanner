import socket
import threading
import sys
import ssl

# ANSI escape sequences for colors
RED = "\033[91m"
RESET = "\033[0m"

# Thread-safe print function with color
def thread_safe_print(message, lock):
    with lock:
        print(message)

# Function to attempt to grab banners for services running on common ports
def grab_banner(ip, port):
    try:
        # Create socket and set a timeout for the connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Increase timeout to 2 seconds

        # If it's an HTTPS port (443), establish an SSL/TLS connection first
        if port == 443:
            sock = ssl.wrap_socket(sock, keyfile=None, certfile=None)

        # Connect to the server
        sock.connect((ip, port))

        # Send an HTTP request (GET) for banner grabbing
        if port == 443:
            # For HTTPS, send a simple GET request over the SSL/TLS connection
            request = "GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n".format(ip)
        else:
            # For HTTP, send a simple GET request
            request = "GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n".format(ip)
        
        sock.send(request.encode())

        # Receive the banner (first 1024 bytes)
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

        # Close the socket connection
        sock.close()

        # Return the banner if it exists, otherwise None
        return banner if banner else None
    except socket.timeout:
        return None  # Connection timed out
    except ssl.SSLError:
        return None  # SSL/TLS error (this can happen with HTTPS)
    except Exception as e:
        return None  # Any other exceptions (e.g., connection errors, malformed responses)

# Function to check if a port is open and grab service version if possible
def scan_port(ip, port, lock, result_file=None):
    try:
        # Create a socket object and set a timeout
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        # Try to connect to the port
        result = sock.connect_ex((ip, port))
        
        # If result is 0, the port is open
        if result == 0:
            msg = f"{RED}Port {port} is open{RESET}"
            banner = grab_banner(ip, port)

            # Checking for common services on known ports
            if port == 22:
                msg += " (SSH)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 80:
                msg += " (HTTP)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 443:
                msg += " (HTTPS)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 21:
                msg += " (FTP)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 3306:
                msg += " (MySQL)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 5432:
                msg += " (PostgreSQL)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 6379:
                msg += " (Redis)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 27017:
                msg += " (MongoDB)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 110:
                msg += " (POP3)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 143:
                msg += " (IMAP)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 25:
                msg += " (SMTP)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 8080:
                msg += " (HTTP Alt)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 9000:
                msg += " (PHP-FPM or Other)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port == 4444:
                msg += " (Metasploit or Open Web Proxy)"
                if banner:
                    msg += f" - Banner: {banner}"
            elif port >= 6660 and port <= 6669:
                msg += " (IRC)"
                if banner:
                    msg += f" - Banner: {banner}"
            else:
                if banner:
                    msg += f" - Banner: {banner}"

            thread_safe_print(msg, lock)
            if result_file:
                result_file.write(msg + "\n")
        
        sock.close()
    except socket.error as e:
        # If the connection fails, just pass (no output)
        pass
    except Exception as e:
        thread_safe_print(f"Error scanning port {port}: {e}", lock)

# Function to scan ports in a specified range with threading
def scan_ports(ip, start_port, end_port, lock, result_file=None):
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, lock, result_file))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def validate_port_range(start_port, end_port):
    # Validate the port range to ensure start < end and within valid port range (0–65535)
    if start_port < 0 or end_port > 65535 or start_port > end_port:
        print("Invalid port range. Valid range is 0-65535, and start_port must be <= end_port.")
        sys.exit(1)

def main():
    # Input: Target IP and port range
    ip = input("Enter the target IP: ")
    if not ip:
        print("IP address cannot be empty.")
        sys.exit(1)

    # Ask user if they want to scan a specific port or a range
    scan_type = input("Do you want to scan a specific port or a range of ports? (specific/range): ").strip().lower()

    # Validate scan type
    if scan_type == 'specific':
        try:
            port = int(input("Enter the port you want to scan: "))
            if port < 0 or port > 65535:
                print("Invalid port. Valid range is 0-65535.")
                sys.exit(1)
        except ValueError:
            print("Please enter a valid integer for the port.")
            sys.exit(1)
        start_port = port
        end_port = port
    elif scan_type == 'range':
        try:
            start_port = int(input("Enter start port: "))
            end_port = int(input("Enter end port: "))
        except ValueError:
            print("Please enter valid integers for ports.")
            sys.exit(1)

        # Validate port range
        validate_port_range(start_port, end_port)
    else:
        print("Invalid choice. Please enter 'specific' or 'range'.")
        sys.exit(1)

    # Ask user if they want to store results in a file
    result_choice = input("Do you want to store open ports in a file? (yes/no): ").strip().lower()
    result_file = None
    if result_choice == 'yes':
        result_filename = input("Enter the filename (e.g., open_ports.txt): ")
        result_file = open(result_filename, "a")

    # Thread lock for thread-safe print
    lock = threading.Lock()

    print(f"Scanning ports {start_port}-{end_port} on {ip}... Please wait.")
    
    # Scan the specified port range or single port using threading
    scan_ports(ip, start_port, end_port, lock, result_file)

    if result_file:
        result_file.close()
        print(f"Results stored in {result_filename}")
    else:
        print("Scan complete. No results saved.")

if __name__ == "__main__":
    main()
