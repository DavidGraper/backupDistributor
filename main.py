import subprocess
import csv
import datetime
import argparse
from os.path import exists
import sys


dryrun = False
pathstobackupfile = ""
outputfilename = ""
directorysearchdepth = 0
backupdevicesize = 0


def getdirectories2rsync(directorysearchdepth, pathstobackup, outputfilename, backupdevicesize):

    lists = []
    for path in pathstobackup:

        print("Processing {0}".format(path))

        # Run Linux "DU" command against path
        process = subprocess.Popen(['du', path, '-d', str(directorysearchdepth) ], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Parse "DU" output as CSV-compliant lines
        reader = csv.reader(stdout.decode('ascii').splitlines(),
                        delimiter='\t', quotechar="'")

        # Add sorted list of directories into master list
        list1 = []
        for row in reader:
            if not(row[1] == path):
                list1.append((row[1], row[0]))

        list1.sort()
        lists.append(list1)

        # For each list, read the entry and add it to a csv file
        storagesum = 0
        blockindicator = 0

        # csvfile = open('directory_breakdown.csv', 'w', newline='')
        csvfile = open(outputfilename, 'w', newline='')
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

                    if (storagesum + directorysize) > float(backupdevicesize):
                        storagesum = directorysize
                        blockindicator += 1
                    else:
                        storagesum += directorysize

                    directory_breakdown.writerow([blockindicator, directoryname, directorysize, storagesum])
                except e:
                    print("error")


def readpathstobackupfromfile(filename):
    if exists(filename):
        file = open(filename ,mode='r')

        returnlist = []
        for line in file:
            returnlist.append(line.rstrip())

        file.close()
    else:
        raise Exception("Backup file cannot be found")

    return returnlist

#
# Start
#
if __name__ == '__main__':

    # create parser
    parser = argparse.ArgumentParser(add_help=True)

    # add arguments to the parser
    parser.add_argument("--pathstobackup", help="Input filename with source paths to back up")
    parser.add_argument("--outputfile", help="Output filename to store size/names of directories in the specified source paths")
    parser.add_argument("--searchdepth", help="Depth that source paths will be searched")
    parser.add_argument("--backupdevicesize", help="Size of backup devices (exponential number okay)")
    parser.add_argument("--dryrun", action="store_true")

    # parse the arguments
    try:
        args = parser.parse_args()
    except:
        print("error 1")

    dryrun = args.dryrun
    directorysearchdepth = args.searchdepth
    pathstobackupfile = args.pathstobackup
    outputfilename = args.outputfile
    backupdevicesize = args.backupdevicesize

    # Get list of paths in backup file
    try:
        pathstobackup = readpathstobackupfromfile(pathstobackupfile)
    except Exception as e:
        print("Cannot read paths to backup: {0}".format(e))
        exit()

    if dryrun:
        print("Summary")
        print("=======")
        print("Program will get sizes and names of all directories under these paths:")
        for path in pathstobackup:
            print("\t{0}".format(path))
        print("\n* Output will be stored in file: '{0}'".format(outputfilename))
        print("* Directory search depth set at: {0}".format(directorysearchdepth))
        print("* Agent distribution will be based on a backup device size of:  {0}".format(backupdevicesize))
        exit()

    getdirectories2rsync(directorysearchdepth, pathstobackup, outputfilename, backupdevicesize)

    print("Done.")
