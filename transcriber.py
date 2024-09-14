import subprocess
import sys
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
required_packages = ['openai-whisper', 'youtube-dl']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        install(package)

# Now import the required modules
import whisper
import os
from urllib.parse import urlparse

# Function to check if FFmpeg is installed
def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, text=True)
        version = result.stdout.split('version')[1].split()[0]
        print(f"FFmpeg version {version} is installed and accessible.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg check failed with error: {e}")
        return False
    except FileNotFoundError:
        print("FFmpeg not found in system PATH. Please install FFmpeg and add it to your system PATH.")
        return False

# Function to download the video from a URL
def download_video_from_url(url):
    print(f"Downloading video from {url}...")
    video_path = urlparse(url).path.split('/')[-1]
    try:
        # Using youtube-dl to download video
        subprocess.run(['youtube-dl', url, '-o', video_path])
        return video_path
    except Exception as e:
        print(f"Error downloading the video: {e}")
        return None

# Function to transcribe video file using Whisper
def transcribe_video(video_path):
    if not check_ffmpeg():
        print("FFmpeg is not installed or not in PATH. Please install FFmpeg and add it to your system PATH.")
        return None

    model = whisper.load_model("base")
    print(f"Transcribing video: {video_path}")
    try:
        result = model.transcribe(video_path)
        
        # Print the transcription
        print(result["text"])
        
        # Save the transcription to a file
        transcription_path = video_path.rsplit('.', 1)[0] + "_transcription.txt"
        with open(transcription_path, "w", encoding='utf-8') as f:
            f.write(result["text"])
        print(f"Transcription saved to: {transcription_path}")
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

# Main function to handle local file or web link
def handle_transcription(input_source):
    if os.path.isfile(input_source):
        # If it's a local file, transcribe it directly
        transcription = transcribe_video(input_source)
    elif input_source.startswith("http"):
        # If it's a URL, download and then transcribe
        video_path = download_video_from_url(input_source)
        if video_path:
            transcription = transcribe_video(video_path)
    else:
        print("Invalid input source. Please provide a valid file path or URL.")

if __name__ == "__main__":
    # Easily changeable input source: local file or web link
    # Example of a local file
    input_source = r"C:\Users\Property Partner\Downloads\I heard you like riddles 7k of Mecca on the line. #makeup #storytime #shopping.mp4"
    
    # Example of a web link (uncomment the line below to use this)
    # input_source = "https://www.example.com/path_to_video.mp4"
    
    handle_transcription(input_source)
