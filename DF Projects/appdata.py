import subprocess 
import os
import time

# Function to run adb commands
def run_adb_command(command):
    adb_path = "/usr/bin/adb"  # Modify this path based on your system's adb path
    full_command = f"{adb_path} {command}"
    result = subprocess.run(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return result.stdout.strip(), result.stderr.strip()

# Function to extract WhatsApp media and data
def extract_whatsapp_data():
    print("Extracting WhatsApp data...")
    
    # Common directories to check for WhatsApp's public files
    whatsapp_paths = {
        "Media": "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media",
        "Photos": "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images",
        "Videos": "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Video/",
        "Audio": "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Audio/",
        "Documents": "/storage/emulated/0/WhatsApp/Media/WhatsApp Documents/",
        "Databases": "/storage/emulated/0/WhatsApp/Databases/",
        "Backups": "/storage/emulated/0/WhatsApp/Backups/"
    }
    
    extracted_files = {}
    
    for data_type, folder_path in whatsapp_paths.items():
        print(f"Checking {data_type} at {folder_path}...")
        output, error = run_adb_command(f"shell ls {folder_path}")
        if error:
            print(f"Error accessing {data_type}: {error}")
            extracted_files[data_type] = []
        else:
            print(f"Found {data_type}: {output.splitlines()}")
            extracted_files[data_type] = output.splitlines()
        time.sleep(1)  # To avoid overloading adb commands
    
    return extracted_files, whatsapp_paths

# Function to download data to a local folder
def download_data(whatsapp_paths, folder_name="WhatsApp_Data"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")
    else:
        print(f"Folder already exists: {folder_name}")
    
    for data_type, folder_path in whatsapp_paths.items():
        local_path = os.path.join(folder_name, data_type)
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        
        print(f"Downloading {data_type} files...")
        output, error = run_adb_command(f"pull {folder_path} {local_path}")
        if error:
            print(f"Error downloading {data_type}: {error}")
        else:
            print(f"Downloaded {data_type} to {local_path}")

# Main function
def main():
    print("Starting WhatsApp data extraction...")
    
    # Extract data
    whatsapp_data, whatsapp_paths = extract_whatsapp_data()
    
    # Download data to local folder
    download_data(whatsapp_paths)

if __name__ == "__main__":
    main()
