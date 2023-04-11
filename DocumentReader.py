import pdfplumber
from collections import namedtuple
import pandas as pd
import re

doc1_path = "./Files/esccrpqpl005iss235.pdf"
change_descriptions = ["Extension", "Extension with new Remark",
                       "Extension with re-scope", "Editorial", "Removal", "Revision"]
change_notice_pages = 3


#patron para devolver este formato "140R, C&K (France)" en forma de grupos
data_re = re.compile(
    r'(\d{2,3}[a-zA-Z])([rev]{3}\d)?,\s(\d{3}[a-zA-Z])?([rev]{3}\d)?([a-zA-Z!@#$&()\\-`+,\’ ]+)\(([a-zA-Z]+)\)')

# patron para devolver este fromato "140R, C&K (France)" sin formatear lo 
data_raw = re.compile(r'(\d{2,3}[A-Z], [a-zA-Z!@#$&()\\-`+,\’ ]+\([a-zA-Z]+\))')




def get_content(doc_1, doc_page):
    doc1_reader = pdfplumber.open(doc_1)
    change_notice_page_content = doc1_reader.pages[doc_page -1].extract_table()
    content = change_notice_page_content[1][1]
    return content


def filter_content(content):
    change_descriptions_dictionary = {}

    for line in content.split('\n'):
        for description in change_descriptions:
            if (line.lower().startswith(description.lower()+":")):
                current_desc = description
                if not current_desc in change_descriptions_dictionary:
                    change_descriptions_dictionary[current_desc] = ""
        if (current_desc):
            change_descriptions_dictionary[current_desc]+=  "_" + line
    
    return change_descriptions_dictionary



def create_table(filter_content):
    table = namedtuple('table','Certificate Revision Munifacturer Action Extra')
    content = []
    # Devolver los certificates y Manufacturers
    for key in filter_content:
        for line in filter_content[key].split("_"):
            line_match = data_re.search(line)
            if line_match:
                cert = line_match.group(1)
                rev = line_match.group(2)
                mun = line_match.group(5) +" "+ line_match.group(6)
                content.append(table(cert, rev, mun, key, cert))
    return content

                

    
table = get_content(doc1_path, change_notice_pages)
filter_table = filter_content(table)
table_content = create_table(filter_table)

df = pd.DataFrame(table_content)
print(df)

