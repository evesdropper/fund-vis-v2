cd /mnt/c/Users/Evelyn/Documents/tonk/fund-vis-v2
cd fund
python3 fund.py cron
cd .. 
message=$(date '+%Y-%m-%d %H:%M:%S')
git add saved/temp.csv
echo "cron commit at ${message}" >> scripts/cronlog.txt
git add scripts/cronlog.txt
git commit -m "add entry at ${message}"
git checkout flask-dev
python3 fund.py cron
git add saved/temp.csv
echo "(flask dev) cron commit at ${message}" >> scripts/cronlog.txt
git add scripts/cronlog.txt
git commit -m "add entry at ${message} - dev branch"
git checkout main