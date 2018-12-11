echo "Running..."
ps aux | grep Chrome | awk ' { print $2 } ' | xargs sudo kill -9
ps aux | grep chrome | awk ' { print $2 } ' | xargs sudo kill -9