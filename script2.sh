max=1

for in `cat numbers.txt`
do
	if [[ $1 > "$max" ]]; then
		max=$1
	echo "$max" >> res.txt
fi
done
