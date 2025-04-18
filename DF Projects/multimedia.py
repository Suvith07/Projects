import subprocess
import os
import shlex
from fpdf import FPDF

# Function to extract and download media files
def extract_media_files(media_type): 
    # Define the ADB command based on media type
    folder_paths = {
        'photos': '/storage/emulated/0/DCIM/Camera/',
        'videos': '/storage/emulated/0/DCIM/Camera',
        'audio': '/storage/emulated/0/Music/'
    }
    valid_extensions = {
        'photos': ['.jpg', '.jpeg', '.png', '.gif'],
        'videos': ['.mp4', '.mkv', '.avi', '.mov'],
        'audio': ['.mp3', '.wav', '.flac', '.aac']
    }

    if media_type not in folder_paths or media_type not in valid_extensions:
        print(f"Invalid media type: {media_type}")
        return []

    folder_path = folder_paths[media_type]
    extensions = valid_extensions[media_type]

    # Check if adb device is connected
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if "device" not in result.stdout:
            print("No device connected or adb is not properly set up.")
            return []
    except Exception as e:
        print(f"Error checking adb device: {str(e)}")
        return []

    # List files in the media directory
    try:
        command = ['adb', 'shell', 'ls', folder_path]
        media_files = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8').split('\n')
        media_files = [file.strip() for file in media_files if file.strip()]

        # Debug: Print files found
        print(f"Files found in {folder_path}: {media_files}")

        # Filter files by valid extensions
        filtered_files = [file for file in media_files if any(file.lower().endswith(ext) for ext in extensions)]

        if not filtered_files:
            print(f"No {media_type} files found in {folder_path}.")
            return []

        # Create a local directory for the media type
        local_dir = os.path.join(os.getcwd(), 'Extracted_Media', media_type)
        os.makedirs(local_dir, exist_ok=True)

        local_files = []

        for file in filtered_files:
            if file:
                # Escape special characters
                remote_file = shlex.quote(os.path.join(folder_path, file))
                local_file = os.path.join(local_dir, os.path.basename(file))

                print(f"Attempting to pull: {remote_file} to {local_file}")

                # Pull the file using adb
                pull_command = ['adb', 'pull', remote_file, local_file]
                result = subprocess.run(pull_command, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"Error pulling {file}: {result.stderr}")
                else:
                    print(f"Successfully pulled {file}")
                    local_files.append(local_file)

        return local_files

    except subprocess.CalledProcessError as e:
        print(f"Error extracting {media_type}: {e.output.decode('utf-8')}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []

# Function to create a PDF summary
def create_pdf_summary(extracted_data, output_folder):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Media Extraction Summary", ln=True, align='C')

    for media_type, files in extracted_data.items():
        pdf.cell(200, 10, txt=f"{media_type.capitalize()}:", ln=True, align='L')
        if files:
            for file in files:
                pdf.cell(200, 10, txt=f"- {os.path.basename(file)}", ln=True, align='L')
        else:
            pdf.cell(200, 10, txt=f"No {media_type} files found.", ln=True, align='L')

    pdf_output_path = os.path.join(output_folder, "Extraction_Summary.pdf")
    pdf.output(pdf_output_path)
    print(f"PDF summary created at: {pdf_output_path}")

# Main function
def main():
    print("Extracting media files...")

    # Directory to save extracted files
    output_folder = os.path.join(os.getcwd(), "Extracted_Media")
    os.makedirs(output_folder, exist_ok=True)

    # Extract photos, videos, and audio
    extracted_data = {
        'photos': extract_media_files('photos'),
        'videos': extract_media_files('videos'),
        'audio': extract_media_files('audio')
    }

    # Print success messages
    for media_type, files in extracted_data.items():
        if files:
            print(f"{media_type.capitalize()} extracted and saved in '{media_type}' folder.")

    # Generate a PDF summary
    create_pdf_summary(extracted_data, output_folder)

if __name__ == "__main__":
    main()
