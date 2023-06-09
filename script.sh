#GET A PARTICULAR FOLDER ALL CONTENT IN TXT FOR UPLOAD ALL TELEGRAM WITH FULL PATH OF EACH FILE AS CAPTION OF THE FILE
find '/path/to/parent-folder' -type f -printf "%P\n" | sort --version-sort > full.txt  #REPLACE ME BETWEEN ''

rm -rf thumb.jpg
fold='/path/to/parent-folder' #REPLACE ME BETWEEN ''

split_video() {
echo "$COUNT. >2GB SO SPLITING $nm"
rm -rf tmp*
mkdir tmp
va="mkvmerge --split 1800M -o 'tmp/%01d.mp4' '$fold/$nm'"
eval $va

c=1
# GETTING HOW MANY LINES IN URL FILE
s=$(ls -l tmp | grep "^-" | wc -l)
#STOP=1
while [ $c -le $s ]
do

echo "$COUNT. >2GB UPLOADING USING PYROGRAM PART$c OF $nm"
python3 upload.py me "tmp/$c.mp4" "$COUNT. $nm PART$c"
echo -e "\n$COUNT. DONE UPLOADING PART$c of $nm\n"

c=$(($c+1))
done

echo -e "$COUNT. DONE UPLOADING TOTAL $s PARTS OF $nm\n"
rm -rf tmp*
}

single_video() {
echo "$COUNT. <2GB UPLOADING USING PYROGRAM $nm"
python3 upload.py me "$fold/$nm" "$COUNT. $nm"
echo -e "\n$COUNT. DONE UPLOADING $nm\n"

}


COUNT=1
# GETTING HOW MANY LINES IN URL FILE
STOP=$(wc -l 'full.txt' | awk '{ print $1 }')
#STOP=1

while [ $COUNT -le $STOP ]
do

nm=$(sed "$COUNT!d" 'full.txt')
fn=$(echo "$nm" | sed 's:.*/::')

# Get the MIME type of the file
mime_type=$(file -b --mime-type "$fold/$nm")

# Check if the MIME type indicates a video
if [[ $mime_type == video/* ]];
then
echo "$COUNT. VIDEO FILE TYPE IS $mime_type"

if [ $(wc -c "$fold/$nm" | awk '{ print $1 }') -le 2000000000 ]; then
single_video
else
split_video
fi

else
echo "$COUNT. FILE TYPE IS $mime_type"
if [ $(wc -c "$fold/$nm" | awk '{ print $1 }') -le 2000000000 ]; then
echo "$COUNT. $mime_type <2GB"
telegram-upload --to me --caption "$COUNT. $nm" "$fold/$nm"
else
echo "$COUNT. $mime_type >2GB SPLITING"
telegram-upload --to me --large-files split --caption "$COUNT. $nm" "$fold/$nm"
fi
fi

COUNT=$(($COUNT+1))
done
echo "ALL DONE UPLOADING"
