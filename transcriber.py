import whisper
import os
import requests
from urllib.parse import urlparse
import subprocess

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
    model = whisper.load_model("base")
    print(f"Transcribing video: {video_path}")
    result = model.transcribe(video_path)
    
    # Print the transcription
    print(result["text"])
    
    # Save the transcription to a file
    transcription_path = video_path.rsplit('.', 1)[0] + "_transcription.txt"
    with open(transcription_path, "w") as f:
        f.write(result["text"])
    print(f"Transcription saved to: {transcription_path}")
    return result["text"]

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

    # Git operations
    try:
        subprocess.run(["git", "add", "transcriber.py"], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit with transcription script"], check=True)
        print("Changes committed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")
