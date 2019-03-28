file=8KLifFpoUdbxXB5noGIG.zip
while(true); do
	echo "$file"
	fcrackzip -D -p rockyou.txt -u $file >> tmp.pw
	unzip -P $(tail -n1 tmp.pw | cut -d' ' -f5) $file >> tmp.file
	#sed -i '/^/\s*$/d' tmp.file
	file=$(tail -n1 tmp.file | cut -d':' -f2 | sed 's/ //g')
	echo $file >> tmp.history
done
