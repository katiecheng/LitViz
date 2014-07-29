#!/bin/bash
for file in `../test/*.pdf`; do 
	pub_id = ${file%.*}
	text = `env/bin/pdf2txt.py ${pub_id}.pdf`
	echo $text > `../test/txt/${pub_id}.txt`
done