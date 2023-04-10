import pdfplumber
from pdfminer.converter import XMLConverter
import re

doc1_path = "./Files/esccrpqpl005iss235.pdf"
change_descriptions = ["extension", "extension with new Remark", "extension with re-scope", "editorial", "removal"]
change_descriptions_dictionary = {}
change_notice_page = 3


def get_content(doc_1, doc_page):
    doc1_reader = pdfplumber.open(doc_1)
    change_notice_page_content = doc1_reader.pages[doc_page - 1].extract_table()
    content = change_notice_page_content[1][1]



    for line in content.split('\n'):
        for description in change_descriptions:
            if(description == line.lower().replace(":", "")):
                current_desc = description
                print("---")
        if(current_desc):
            change_descriptions_dictionary[current_desc] = line 
    
    print(change_descriptions_dictionary)
        
        



get_content(doc1_path, change_notice_page)