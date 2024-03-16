import re
import sys
import csv
from collections import Counter
from datetime import datetime

def digest_report_of(file_path):
    syscall_pattern = re.compile(r"\s(\w+)\(")
    syscall_counter = Counter()

    with open(file_path, 'r') as file:
        for line in file:
            match = syscall_pattern.search(line)
            if match:
                syscall_name = match.group(1)
                syscall_counter[syscall_name] += 1

    return syscall_counter

def export_to_csv(syscall_counts, filename):
    timestamp = datetime.now().strftime('%d%b%Y-%I:%M:%S%p')
    csv_file_name = f'digest_report_of_{filename}.csv'

    with open(csv_file_name, 'w', newline='') as csvfile:
        fieldnames = ['Syscall', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for syscall, count in syscall_counts.items():
            writer.writerow({'Syscall': syscall, 'Count': count})

    print(f"Syscall counts exported to {csv_file_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 counter.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    filename = file_path.split('/')[-1].split('.')[0]
    syscall_counts = digest_report_of(file_path)

    for syscall, count in syscall_counts.items():
        print(f"{syscall}: {count}")

    export_to_csv(syscall_counts, filename)
