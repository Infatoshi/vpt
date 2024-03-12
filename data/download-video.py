import json
import requests
import os
from pathlib import Path
from tqdm import tqdm

# Load the data from the JSON file
with open("video-contents.json", "r") as f:
    data = json.load(f)

# Create a directory to store the downloaded files
output_dir = Path("downloaded_videos")
output_dir.mkdir(exist_ok=True)

# Download each video file
for rel_path in data["relpaths"]:
    url = data["basedir"] + rel_path
    file_name = rel_path.split("/")[-1]
    output_path = output_dir / file_name

    # Check if the file already exists
    if output_path.exists():
        file_size = output_path.stat().st_size
    else:
        file_size = 0

    # Send a HEAD request to get the total file size
    response = requests.head(url)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))

        # Skip the file if it has already been downloaded
        if file_size == total_size:
            print(f"{file_name} already downloaded, skipping.")
            continue

        # Partial download
        if file_size > 0:
            print(f"Resuming download of {file_name}")
            headers = {"Range": f"bytes={file_size}-"}
            mode = "ab"  # Append mode
        # New download
        else:
            print(f"Downloading {file_name}")
            headers = None
            mode = "wb"  # Write mode

        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200 or response.status_code == 206:  # 206 for partial content
            block_size = 1024
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, initial=file_size)
            with open(output_path, mode) as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        progress_bar.update(len(chunk))
                        f.write(chunk)
            progress_bar.close()
            print(f"Downloaded {file_name}")
        else:
            print(f"Failed to download {file_name}. Error: {response.status_code}")
    else:
        print(f"Failed to download {file_name}. Error: {response.status_code}")