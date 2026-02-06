import argparse
import subprocess
import re
import os
import sys

def kill_process_on_port(port):
    print(f"Checking for process on port {port}...")
    
    try:
        # Run netstat to find the PID listening on the port
        # -a: Displays all active connections/ports
        # -n: Displays address and port numbers numerically
        # -o: Displays the owning process ID
        output = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
        
        # Parse the output to find the PID
        # Expected format:   TCP    127.0.0.1:8000         0.0.0.0:0              LISTENING       1234
        lines = output.strip().split('\n')
        pids = set()
        
        for line in lines:
            if "LISTENING" in line:
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 5:
                    pid = parts[-1]
                    pids.add(pid)
        
        if not pids:
            print(f"No process found listening on port {port}.")
            return

        for pid in pids:
            if pid == "0":
                continue
                
            print(f"Found process with PID: {pid}")
            try:
                # Kill the process
                # /F: Forcefully terminate the process
                # /PID: Specify the PID of the process to be terminated
                subprocess.check_call(f"taskkill /F /PID {pid}", shell=True)
                print(f"Successfully killed process {pid} on port {port}.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to kill process {pid}: {e}")

    except subprocess.CalledProcessError:
        print(f"No active connections found on port {port}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kill process running on a specific port.")
    parser.add_argument("port", type=int, help="Port number to check and kill process.")
    args = parser.parse_args()
    
    kill_process_on_port(args.port)
