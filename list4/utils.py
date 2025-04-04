import os
import csv
from datetime import datetime

def find_media_files(directory):
    media_extensions = {'.mp3', '.mp4', '.avi', '.mkv', 
                           '.wav', '.flac', '.aac', '.ogg', 
                           '.wma', '.mov', '.wmv', '.webm', 
                           '.mpeg', '.mpg', '.3gp'}

    return find_files_by_extensions(directory, media_extensions)


def find_image_files(directory):
    image_extensions = {'.gif', '.jpg' , '.jpeg' , '.jfif' , 
                           '.pjpeg' , '.pjp', '.png', '.tiff', 
                           '.bmp', '.webp', '.svg', '.raw'}

    return find_files_by_extensions(directory, image_extensions)

def find_files_by_extensions(directory, extensions):    
    files = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        _, extension = os.path.splitext(filename)
        
        if extension.lower() in extensions:
            files.append(filepath)

    return files

def get_output_directory():
    return os.environ.get("CONVERTED_DIR", os.path.join(os.getcwd(), "converted"))

def log_conversion(timestamp, input_file, output_format, output_file):

    history_file = os.path.join(get_output_directory(), 'history.csv')
    
    record = {
        'timestamp': timestamp,
        'input_file': input_file,
        'output_format': output_format,
        'output_file': output_file
    }
    
    fieldnames = record.keys()
    
    history_file_exists = os.path.exists(history_file)

    with open(history_file, "a", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not history_file_exists:
            writer.writeheader()
        writer.writerow(record)