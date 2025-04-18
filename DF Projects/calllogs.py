import subprocess
import json
from fpdf import FPDF

def is_device_connected():
    """Check if any device is connected via adb."""
    print("Checking device connection...")
    command = "adb devices"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if "device" in result.stdout:
            print("Device is connected.")
            return True
    except subprocess.TimeoutExpired:
        print("ADB command timed out while checking connected devices.")
    except Exception as e:
        print(f"Error checking device connection: {e}")
    return False

def get_call_logs():
    """Retrieve call logs from the connected device."""
    print("Fetching call logs...")
    command = "adb shell content query --uri content://call_log/calls"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        call_logs = []
        for line in result.stdout.splitlines():
            log_entry = {}
            for item in line.split(", "):
                key_value = item.split("=")
                if len(key_value) == 2:
                    log_entry[key_value[0].strip()] = key_value[1].strip()
            call_logs.append(log_entry)
        print(f"Fetched {len(call_logs)} call logs.")
        return call_logs
    except subprocess.TimeoutExpired:
        print("ADB command timed out while fetching call logs.")
    except Exception as e:
        print(f"Error fetching call logs: {e}")
    return []

def get_sms():
    """Retrieve SMS logs from the connected device."""
    print("Fetching SMS logs...")
    command = "adb shell content query --uri content://sms"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        sms_logs = []
        for line in result.stdout.splitlines():
            sms_entry = {}
            for item in line.split(", "):
                key_value = item.split("=")
                if len(key_value) == 2:
                    sms_entry[key_value[0].strip()] = key_value[1].strip()
            sms_logs.append(sms_entry)
        print(f"Fetched {len(sms_logs)} SMS logs.")
        return sms_logs
    except subprocess.TimeoutExpired:
        print("ADB command timed out while fetching SMS logs.")
    except Exception as e:
        print(f"Error fetching SMS logs: {e}")
    return []

def save_to_pdf(call_logs, sms_logs, filename="call_sms_logs.pdf"):
    """Save the call and SMS logs into a PDF file."""
    print(f"Saving logs to {filename}...")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Call Logs:", ln=True)
    pdf.ln(5)  # Line break

    # Add call logs to PDF in chunks
    for i, log in enumerate(call_logs):
        if i % 50 == 0:  # Process 50 entries per chunk
            print(f"Processing call log entry {i+1}/{len(call_logs)}")
        log_text = json.dumps(log, indent=4)
        if pdf.get_y() + 10 > pdf.page_break_trigger:
            pdf.add_page()
        pdf.multi_cell(0, 10, log_text)
        pdf.ln(5)

    pdf.add_page()
    pdf.cell(200, 10, txt="SMS Logs:", ln=True)
    pdf.ln(5)

    # Add SMS logs to PDF in chunks
    for i, sms in enumerate(sms_logs):
        if i % 50 == 0:  # Process 50 entries per chunk
            print(f"Processing SMS log entry {i+1}/{len(sms_logs)}")
        sms_text = json.dumps(sms, indent=4)
        if pdf.get_y() + 10 > pdf.page_break_trigger:
            pdf.add_page()
        pdf.multi_cell(0, 10, sms_text)
        pdf.ln(5)

    pdf.output(filename)
    print("Logs saved to PDF successfully.")

if __name__ == "__main__":
    # Check if the device is connected
    if is_device_connected():
        print("Device connected. Fetching call logs and SMS...")
        
        # Extract call logs and SMS
        call_logs = get_call_logs()
        sms_logs = get_sms()

        # Check if logs were fetched
        if call_logs or sms_logs:
            # Save the logs to a PDF file
            save_to_pdf(call_logs, sms_logs)
            print("Call logs and SMS have been saved to call_sms_logs.pdf")
        else:
            print("No logs found or failed to retrieve logs.")
    else: 
        print("No device connected. Please connect your phone via USB.")
