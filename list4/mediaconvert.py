# LOGGING KOLEJNOSC ATRYBUTOW I PODWÓJNA KROPA

import os
import sys
import json
import subprocess
from datetime import datetime
from utils import find_media_files, find_image_files, get_output_directory, log_conversion

def convert_media(input_dir, output_format):
    ''''
    Converts media and image files in the given directory to the specified format.
    
    Args:
        input_dir (str) = path to the directory containing media or image files.
        output_format (str) = desired output format.
    '''
    media_files = find_media_files(input_dir)
    image_files = find_image_files(input_dir)
    output_dir = get_output_directory()
    os.makedirs(output_dir, exist_ok=True)
    
    for file in media_files:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename, _ = os.path.splitext(os.path.basename(file))
        output_file = os.path.join(output_dir, f'{timestamp}-{filename}.{output_format}')
        
        try:
            subprocess.run([
                'ffmpeg', '-i', file, output_file
            ], check=True)

            print(f"Converted: {file} -> {output_file}")

            log_conversion(timestamp, file, output_format, output_file, 'ffmpeg')

            print(f'logged: {file} -> {output_file}')

        except subprocess.CalledProcessError as e:
            print(f"Error converting {file}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    for file in image_files:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename, _ = os.path.splitext(os.path.basename(file))
        output_file = os.path.join(output_dir, f"{timestamp}-{filename}.{output_format}")
        
        print(filename)

        try:
            subprocess.run([
                'magick', file, output_file
            ], check=True)
            
            print(f"Converted: {file} -> {output_file}")

            log_conversion(file, output_format, output_file, 'ImageMagick')

            print(f'logged: {file} -> {output_file}')

        except subprocess.CalledProcessError as e:
            print(f"Error converting {file}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python mediaconvert.py <input_directory> <output_format>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_format = sys.argv[2]
    if output_format.startswith('.'):
        output_format = output_format[1:]
    convert_media(input_dir, output_format)
