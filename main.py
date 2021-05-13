# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
bashCommand = "du /home/dgraper/colossus_share0/Work-related/ -d 2 | sort -k 2"

import subprocess
import csv

process = subprocess.Popen(['du', '/home/dgraper/colossus_share0/Movies', '-d', '2' ], stdout=subprocess.PIPE)
stdout, stderr = process.communicate()

reader = csv.DictReader(stdout.decode('ascii').splitlines(),
                        delimiter='\t', skipinitialspace=True,
                        fieldnames=['space', 'name'])

dict1 = {}

for row in reader:
    dict1.items.
    print(row)

print(sorted(reader, key='name'))

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
