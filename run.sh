if [ ! -d "./pidfile.txt" ]; then
  kill -9 `cat pidfile.txt`
fi

nohup python main.py > /dev/null 2>&1 & echo $! > pidfile.txt
