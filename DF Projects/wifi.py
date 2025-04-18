import subprocess
from fpdf import FPDF

# Function to extract Wi-Fi logs
def extract_wifi_logs():
    try:
        # Run adb command to extract wifi logs
        wifi_logs = subprocess.check_output(['adb', 'shell', 'dumpsys', 'wifi']).decode('utf-8')
        print("Raw Wi-Fi Logs:", wifi_logs)  # Debugging: print the raw logs to check format
        wifi_logs = wifi_logs.split('\n')
        wifi_logs = [log for log in wifi_logs if 'connected' in log or 'disconnected' in log]
        return wifi_logs
    except subprocess.CalledProcessError as e:
        print(f"Error extracting Wi-Fi logs: {e.output.decode('utf-8')}")
        return []

# Function to extract Bluetooth connections
def extract_bluetooth_connections():
    try:
        # Run adb command to extract bluetooth logs
        bluetooth_connections = subprocess.check_output(['adb', 'shell', 'dumpsys', 'bluetooth_manager']).decode('utf-8')
        print("Raw Bluetooth Logs:", bluetooth_connections)  # Debugging: print the raw logs to check format
        bluetooth_connections = bluetooth_connections.split('\n')
        bluetooth_connections = [conn for conn in bluetooth_connections if 'Connected' in conn or 'Disconnected' in conn]
        return bluetooth_connections
    except subprocess.CalledProcessError as e:
        print(f"Error extracting Bluetooth logs: {e.output.decode('utf-8')}")
        return []

# Function to create PDF file
def create_pdf_file(wifi_logs, bluetooth_connections):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)

    # Adding Wi-Fi Logs
    pdf.cell(200, 10, txt="Wi-Fi Logs", ln=True, align='C')
    pdf.ln(10)
    for log in wifi_logs:
        pdf.cell(200, 10, txt=log, ln=True, align='L')
    pdf.ln(20)

    # Adding Bluetooth Connections
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Bluetooth Connections", ln=True, align='C')
    pdf.ln(10)
    for conn in bluetooth_connections:
        pdf.cell(200, 10, txt=conn, ln=True, align='L')

    # Save PDF
    pdf.output("device_logs.pdf")
    print("PDF generated as 'device_logs.pdf'")

# Main function
def main():
    wifi_logs = extract_wifi_logs()
    bluetooth_connections = extract_bluetooth_connections()
    create_pdf_file(wifi_logs, bluetooth_connections)

if __name__ == "__main__":
    main()
