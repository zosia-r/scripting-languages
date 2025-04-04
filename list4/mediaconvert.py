import os
import sys
import subprocess
from datetime import datetime
from utils import find_media_files, find_image_files, get_output_directory, log_conversion

def file_loop(file_list, output_dir, output_format, subprocess_tool):
    for file in file_list:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename, _ = os.path.splitext(os.path.basename(file))
        output_file = os.path.join(output_dir, f'{timestamp}-{filename}.{output_format}')
        
        match subprocess_tool:
            case 'ffmpeg':
                subprocess_args = ['ffmpeg', '-i']
            case 'magick':
                subprocess_args = ['magick']
            case _:
                print(f"Unknown subprocess tool: {subprocess_tool}")
                return
        
        subprocess_args.append(file)
        subprocess_args.append(output_file)

        try:
            subprocess.run(subprocess_args, check=True)
            print(f"Converted: {file} -> {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {file}: {e}")

        try:
            log_conversion(timestamp, file, output_format, output_file, subprocess_args[0])
            print(f'logged: {file} -> {output_file}')
        except Exception as e:
            print(f"Error logging: {e}")


def convert_media(input_dir, output_format):

    media_files = find_media_files(input_dir)
    image_files = find_image_files(input_dir)
    output_dir = get_output_directory()
    os.makedirs(output_dir, exist_ok=True)

    file_loop(media_files, output_dir, output_format, 'ffmpeg')
    file_loop(image_files, output_dir, output_format, 'magick')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python mediaconvert.py <input_directory> <output_format>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_format = sys.argv[2]
    if output_format.startswith('.'):
        output_format = output_format[1:]
    convert_media(input_dir, output_format)
