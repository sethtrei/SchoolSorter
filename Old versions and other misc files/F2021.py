#!/usr/bin/env python3
# to install pdfminer, do pip3 install pdfminer.six
# you may have to update pip/pip3 for it to work
# to install docx you need to do pip3 install python-docx
import glob
import os
import docx2txt
from pdfminer.high_level import extract_text
from PyPDF2 import PdfFileWriter, PdfFileReader
import docx
import shutil

global courses
global codes
courses = ["CMSC330", "CMSC351", "CMSC131", "STAT400", "MUSC210"]


def main():
    list_of_files = glob.glob('/Users/sethtreiman/Downloads/*')
    file_path = max(list_of_files, key=os.path.getctime)
    time = os.stat(list_of_files[0]).st_birthtime
    for path in list_of_files:
        if os.stat(path).st_birthtime > time :
            time = os.stat(path).st_birthtime
            file_path = path

    file_name = file_path[29:]
    print(file_name)
    class_name = get_name(file_name)

    if ((file_path[-4:] == '.pdf' or ".docx" in file_path) and class_name == ""):

        class_name = get_name(file_path[29:])



        if file_path[-4:] == '.pdf' :

            file = PdfFileReader(file_path)

            if file.isEncrypted:
                os.system("qpdf --password=uuddlrlrBA --decrypt --replace-input " + file_path)

            if (class_name == ""):
                data = extract_text(file_path)
                class_name = get_name(data)

        else:
            if (class_name == ""):
                data = docx2txt.process(file_path)
                class_name = get_name(data)

    notif = "/Users/sethtreiman/Library/Mobile\ Documents/com\~apple\~CloudDocs/Projects/Python\ Projects/SchoolSorter/School\ Sorter -appIcon \'/Users/sethtreiman/Pictures/School-Sorter-Icon.icns\' -timeout 5 -actions Open -ignoreDnD -title ' " + file_name + " 📁 ' -message "
    if (class_name != ""):
        notif += "\'Found! The course is " + class_name + ".\' "
        class_name += '/'
        new_path = '/Users/sethtreiman/Documents/School/Junior Year/Fall/' + class_name + file_name
        shutil.move(file_path, new_path)
        file_path = new_path
    else:
        notif += "\'Not found!\' "

    notif += " >> /Users/sethtreiman/.last_ss_output.txt"

    print(notif)
	
   

    os.system(notif)

    #open text file in read mode
    text_file = open("/Users/sethtreiman/.last_ss_output.txt", "r")

    #read whole file to a string
    data = text_file.read()

    #close file
    text_file.close()
    os.system("rm /Users/sethtreiman/.last_ss_output.txt")


    if (data == "Open"):
        os.system("open " + file_path.replace(" ", "\ "))

def get_name(file_name) :
    file_name = file_name.upper()
    name = ""
    times_found = 0
    for course in courses:
        if (course in file_name):
            name = course
            times_found += 1

    if (times_found > 1 or times_found == 0):
        for course in courses:
            with_space = course[:4] + " " + course[-3:]
            if (course in file_name or with_space in file_name):
                name = course


    return name;






main()
