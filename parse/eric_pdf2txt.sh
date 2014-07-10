#!/bin/bash
for pub_id in `cat eric_pub_ids.txt`; do 
	text = `env/bin/pdf2txt.py ${pub_id}.pdf`
	echo $text > ${pub_id}.txt
done