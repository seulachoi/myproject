# EC2 서버 연결 끊겼을 때 재시작
1. EC2 인스턴스 재부팅 : 상태 2개 모두 패스해야함 
2. GIT BASH `$ ssh -i /c/Users/sara/Desktop/sparta/sparta.pem ubuntu@3.34.49.195` 접속
3. `~$ sudo service mongod start`: 몽고 DB 시작   
`~$ cd ~/my_projects`  
`:~/my_projects$ sudiptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5000` : 5000 포트 떼어줘야 함 
`~/my_projects$ python app.py`  app.py 재시작
