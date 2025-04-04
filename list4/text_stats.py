import sys
import csv
from collections import Counter

def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    all_text = ''.join(lines)
    all_words = all_text.split()
    
    char_count = len(all_text)
    word_count = len(all_words)
    line_count = len(lines)
    most_common_char = Counter(all_text).most_common(1)[0][0] if all_text else ''
    most_common_word = Counter(all_words).most_common(1)[0][0] if all_words else ''

    return [
        file_path,
        char_count,
        word_count,
        line_count,
        most_common_char,
        most_common_word
    ]

if __name__ == '__main__':
    input_path = sys.stdin.readline().strip()
    stats = analyze_file(input_path)

    writer = csv.writer(sys.stdout)
    writer.writerow(['file_path', 'char_count', 'word_count', 'line_count', 'most_common_char', 'most_common_word'])
    writer.writerow(stats)
