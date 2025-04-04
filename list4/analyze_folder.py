import os
import sys
import csv
import subprocess
from collections import Counter

def run_text_stats(file_path):
    result = subprocess.run(
        ['python', 'text_stats.py'],
        input=f'{file_path}\n',
        text=True,
        capture_output=True,
        check=True
    )
    lines = result.stdout.strip().splitlines()
    reader = csv.DictReader(lines)
    return next(reader)

def summarize_results(results):
    total_files = len(results)
    total_chars = sum(int(r['char_count']) for r in results)
    total_words = sum(int(r['word_count']) for r in results)
    total_lines = sum(int(r['line_count']) for r in results)

    all_chars = Counter()
    all_words = Counter()
    for r in results:
        all_chars[r['most_common_char']] += 1
        all_words[r['most_common_word']] += 1

    most_common_char = all_chars.most_common(1)[0][0] if all_chars else ''
    most_common_word = all_words.most_common(1)[0][0] if all_words else ''

    summary = {
        'files_processed': total_files,
        'total_characters': total_chars,
        'total_words': total_words,
        'total_lines': total_lines,
        'most_common_char': most_common_char,
        'most_common_word': most_common_word
    }
    return summary

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_folder.py <directory>")
        sys.exit(1)

    folder_path = sys.argv[1]
    text_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".txt")]

    results = []
    for path in text_files:
        try:
            stats = run_text_stats(path)
            results.append(stats)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {path}: {e.stderr}")
        except Exception as e:
            print(f"Unexpected error processing {path}: {e}")

    summary = summarize_results(results)

    print('files_processed,total_characters,total_words,total_lines,most_common_char,most_common_word')
    print(','.join(str(summary[k]) for k in summary))

if __name__ == "__main__":
    main()
