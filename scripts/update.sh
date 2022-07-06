cd /mnt/c/Users/Evelyn/Documents/tonk/fund-vis-v2
message=$(date '+%Y-%m-%d %H:%M:%S')
git push heroku main
echo "cron update at ${message}" >> scripts/cronlog.txt
