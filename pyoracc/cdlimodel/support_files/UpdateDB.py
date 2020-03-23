from __future__ import print_function
import requests
import re
import sys


def update(url):
    path = 'https://cdli.ucla.edu/atfchecker/'+url  # the url you want to POST
    header = {"Content-type": "application/x-www-form-urlencoded"}
    fetch = requests.post(path, headers=header)
    page = fetch.text

    if(page.find('Error:') != -1):
        print("Update Failed.\nPlease contact CDLI.")
        sys.exit()

    return page


def write_to_file(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()


def clean_qnumbers(text):
    qnumbers = re.findall(r'Q[0-9]{6}', text)
    return qnumbers


if __name__ == "__main__":
    # Updating ValidPnumbers.txt
    qnumber_string = ""
    write_to_file('ValidPnumbers.txt', update('update_pnumbers.php'))
    qnumbers = clean_qnumbers(update('update_qnumbers.php'))

    for element in qnumbers:
        qnumber_string = qnumber_string + element + "\n"

    write_to_file('ValidQnumbers.txt', qnumber_string)
    write_to_file('PeriodMap.txt', update('update_periodmap.php'))

    print("Support Content Updated")
