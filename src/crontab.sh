# custom stocks
python dmonth.py BABA

# nasdaq 100 stocks
cat nasdaq100.txt | cut -d '	' -f1 | xargs python dmonth.py 
