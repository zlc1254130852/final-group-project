import pandas as pd
from urlextract import URLExtract
from fuzzywuzzy import fuzz
import pdfplumber
import re
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table, _Row
from docx.text.paragraph import Paragraph
import docx
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))



def pdf_to_text(file_path):
    # read the PDF
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    # Cleaning text
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    name_regex = r'^\s*([A-Z][a-z]+)(([\s\'\-][A-Z][a-z]+)+)?$'
    text = re.sub(name_regex, '<PERSON>', text)
    text = re.sub(email_regex, '<EMAIL ADDRESSS>', text)
    phone_regex = "\\+?[1-9][0-9]{7,14}"
    text = re.sub(phone_regex, '', text)

    return text


def getText_docx(filename):

    doc = docx.Document(filename)

    fullText = []

    for block in iter_block_items(doc):
        # read Paragraph
        if isinstance(block, Paragraph):
            fullText.append(block.text)
        # read table
        elif isinstance(block, Table):
            for row in block.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        fullText.append(para.text)

    return '\n'.join(fullText)
