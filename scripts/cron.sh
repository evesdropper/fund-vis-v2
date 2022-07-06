cd /mnt/c/Users/Evelyn/Documents/tonk/fund-vis-v2
cd fund
python3 fund.py cron
cd .. 
message=$(date '+%Y-%m-%d %H:%M:%S')
git add saved/temp.csv
git commit -m "add entry at ${message}"
echo "cron commit at ${message}" >> scripts/cronlog.txt
