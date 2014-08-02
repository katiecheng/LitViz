#!/bin/bash
for file in /Volumes/Backup_Katie_MacAir/Scraper4/*.pdf; do 
	pub_id=${file%.*};
	echo $pub_id;
	text=$(pdf2txt.py ${pub_id}.pdf);
	if [[ $text == *the* ]]
	then
		echo $text>${pub_id}.txt;
	fi
done