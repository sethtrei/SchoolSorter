import glob
import os
import docx2txt
import pdfminer
from pdfminer.high_level import extract_text
from PyPDF2 import PdfFileWriter, PdfFileReader
import docx
import shutil

global courses
global codes
courses = ["CMSC216", "ENEE244", "ENES100", "INAG110", "MATH246"]


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
    class_name = ""

    if (file_path[-4:] == '.pdf' or ".docx" in file_path):

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

    notif = "terminal-notifier -appIcon \'/Users/sethtreiman/Pictures/School-Sorter-Icon.icns\' -ignoreDnD -group 'school-sorter' -title ' " + file_name + " 📁 ' -message "
    if (class_name != ""):
        notif += "\'Found! The course is " + class_name + ".\' "
        class_name += '/'
        new_path = '/Users/sethtreiman/Documents/School/Sophomore Year/Fall/' + class_name + file_name
        shutil.move(file_path, new_path)
        file_path = new_path
    else:
        notif += "\'Not found!\' "

    notif += "-execute \'open " + file_path.replace(" ", "\ ") + "\'"

    os.system(notif)

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
