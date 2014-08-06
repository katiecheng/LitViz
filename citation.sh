#!/bin/bash
gscholar_query_result=$(python scholar.py -c 1 -t -p "$1" --csv 2>&1);
num_citations=$(echo $gscholar_query_result | cut -d '|' -f4);
echo $num_citations;