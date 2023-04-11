import pdfplumber
from collections import namedtuple
import re

doc1_path = "./Files/esccrpqpl005iss224_jan22.pdf"
change_descriptions = ["Extension", "Extension with new Remark",
                       "Extension with re-scope", "Editorial", "Removal", "Revision"]
change_notice_pages = 3

data_re = re.compile(
    r'(\d{3}[a-zA-Z])([rev]{3}\d)?,\s(\d{3}[a-zA-Z])?([rev]{3}\d)?([a-zA-Z!@#$&()\\-`+,\’ ]+)\(([a-zA-Z]+)\)')

data_re2 = re.compile(
    r'((\d{3}[a-zA-Z])([rev]{3}\d)?,\s)*([a-zA-Z!@#$&()\\-`+\’ ]+)\(([a-zA-Z]+)\)')


def get_content(doc_1, doc_page):
    doc1_reader = pdfplumber.open(doc_1)
    change_notice_page_content = doc1_reader.pages[doc_page -1].extract_table()
    content = change_notice_page_content[1][1]
    return content


    # print(data_re.findall(
    #     change_descriptions_dictionary["Extension"]))

    # print(data_re.findall(
    #     "301Frev2, 300Drev3, Souriau (France)_365Arev2, Axon’ Cable (France)"))

def filter_content(content):
    change_descriptions_dictionary = {}

    for line in content.split('\n'):
        for description in change_descriptions:
            if (line.lower().replace(":", "").startswith(description.lower())):
                current_desc = description
                if not current_desc in change_descriptions_dictionary:
                    change_descriptions_dictionary[current_desc] = ""
        if (current_desc):
            change_descriptions_dictionary[current_desc] +=  "_" + line
    
    return change_descriptions_dictionary


table = get_content(doc1_path, change_notice_pages)
filter_table = filter_content(table)

for key in filter_table:
    print(data_re.findall(filter_table[key]))
