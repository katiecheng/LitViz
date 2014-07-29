import pdf2txt

for pdf in test_pdf_folder:
	txt = pdf2txt(pdf)
	eric_txt_parse(txt)