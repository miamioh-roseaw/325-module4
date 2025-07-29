import paramiko
import time
import os  # For reading environment variables securely

# Get credentials from Jenkins environment variables
username = os.environ.get('CISCO_CREDS_USR')
password = os.environ.get('CISCO_CREDS_PSW')

if not username or not password:
    raise ValueError("Missing credentials: Make sure Jenkins is injecting CISCO_CREDS_USR and CISCO_CREDS_PSW.")

# Define devices to connect to
devices = [
    {'ip': '10.10.10.1', 'hostname': 'mgmt-rtr'},
    {'ip': '10.10.10.2', 'hostname': 'reg-rtr'},
    {'ip': '10.10.10.3', 'hostname': 'ham-rtr'},
    {'ip': '10.10.10.4', 'hostname': 'mid-rtr'}
]

# Loop through each device and capture output
for device in devices:
    try:
        print(f"[INFO] Connecting to {device['hostname']} at {device['ip']}...")

        # Create SSH client and accept unknown host keys
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=device['ip'], username=username, password=password)

        # Start an interactive shell session
        shell = ssh.invoke_shell()
        time.sleep(1)

        # Send commands
        shell.send('terminal length 0\n')  # Disable paging
        shell.send('show version\n')
        time.sleep(2)
        output_version = shell.recv(65535).decode()

        shell.send('show run\n')
        time.sleep(3)
        output_run = shell.recv(65535).decode()

        # Combine and save outputs
        full_output = f"--- SHOW VERSION ({device['hostname']}) ---\n{output_version}\n\n--- SHOW RUN ---\n{output_run}"

        with open(f"{device['hostname']}_output.txt", "w") as file:
            file.write(full_output)

        print(f"[SUCCESS] Saved output for {device['hostname']}")
        ssh.close()

    except Exception as e:
        print(f"[ERROR] Failed to connect to {device['hostname']} at {device['ip']}: {e}")
