import subprocess
import csv
import datetime

def getdirectories2rsync(paths):

    lists = []
    for path in paths:

        print("Processing {0}".format(path))

        process = subprocess.Popen(['du', path, '-d', '1' ], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()

        reader = csv.reader(stdout.decode('ascii').splitlines(),
                        delimiter='\t', quotechar="'")

        list1 = []

        # isFirstRow = True
        for row in reader:
            if not(row[1] == path):
                list1.append((row[1], row[0]))
            # else:
            #     isFirstRow = False

        list1.sort()
        lists.append(list1)

        # For each list, read the entry and add it to a csv file
        storagesum = 0
        blockindicator = 0

        csvfile = open('directory_breakdown.csv', 'w', newline='')
        directory_breakdown = csv.writer(csvfile)

        for list2 in lists:
            for member in list2:
                directoryname = member[0]
                directorysize = int(member[1])

                try:

                # du returns size in K, so terabyte is adjusted downwards 1K
                # 8T = 8E9
                # 500G = 5E8
                # 465.76 = 4.65E8
                # 240G = 2.4E8
                # 223G = 2.2357E8 <= Correct size?

                    if (storagesum + directorysize) > 4.65E8:
                        print("465GB Breakpoint")
                        print("Storagesum = {0}, Directorysize = {1}. Directoryname = {2}".format(storagesum, directorysize,directoryname))
                        storagesum = directorysize
                        blockindicator += 1
                    else:
                        storagesum += directorysize

                    # print("{0}\t{1}\t({2}\t{3})".format(str(blockindicator), directoryname, directorysize, str(storagesum)))
                    directory_breakdown.writerow([blockindicator, directoryname, directorysize, storagesum])
                except:
                    print("error")

        print("Done")

# Get paths to backup -- mind the capitalization!!
paths2backup = [# '/home/dgraper/colossus_share0/Video',
                # '/home/dgraper/colossus_share0/Work-related',
                '/home/dgraper/colossus_share0/Movies',
                # '/home/dgraper/colossus_share0/Television',
                # '/home/dgraper/colossus_share0/House-related',
                # '/home/dgraper/colossus_share0/Audio/Music',
                ]

# Create work scheduling file
getdirectories2rsync(paths2backup)



#

# # print("Printing list1")
# #
# # list1.sort(reverse=True)
# #
# # print(list1)
#
# def print_hi(name):
#
#     # Use a breakpoint in the code line below to debug your script.
#
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
#
#
#
# # Press the green button in the gutter to run the script.
#
# if __name__ == '__main__':
#
#     print_hi('PyCharm')
#
#
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
