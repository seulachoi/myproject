
# mongodb ubuntu에 연결하기 실패 authorization 문제 

`$ mongo -u "sara" -p --authenticationDatabase "admin"`

1. mongodb app.py 실행 안되었던 문제 : 스파르타에서 배운대로 새로운 계정을 생성하려 했으나, command insert authentification / unauthroized 등의 문제로 실패 
```
# admin으로 계정 바꾸기
use admin;

# 계정 생성하기
db.createUser({user: "test", pwd: "test", roles:["root"]});
```

2. 기존에 만들어놓았던 sara admin 계정을 삭제하고, 1을 다시 해도 같은 오류 발생 
3. **mongo robo3T, 파이썬 터미널에서 실행하던 Mongodb 모두 끄고 -> mongodb다시 설치하고** (mongodb install.sh 는 filezilla ubuntu home에만 있어야 하나?)
4. sudo로 다시 mongod 시작 -> 상태를 조회 했더니 
` . installmongodb.sh`
`$ sudo service mongod start`
`$ netstat -tnlp`
5. 0.0.0.0:27017 로 조회됨. 0.0.0.0으로 해줘야 외부에서 접근이 가능하도록 허용! (초기화 되어서 127.0.0.0:27017 일 줄 알았는데 ;; 왜 지난주 수업에서 설정했던 0.0.0.0:27017 인지는 모르겠어)
`sudo vi /etc/mongod.conf`로 조회해도 #security 상태는 그대로... ㅇㅅㅇ 수업엔선 security authorizaion:enabled 로 했었는데...
```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:27017           0.0.0.0:*               LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN  
```

6. Robo3T로 mongodb 원격으로 접속! 접속 정보
adress: EC2 IP
Authentification 에서 user name/pwd 설정 
7. **pymongo에도 6에서 설정한 아이디/비번 넣어주기** 
- EC2 서버 DB에도 아이디/비번 추가했으니, `app.py`에 있는 pymongo에도 비번/아이디 넣어줘야함 
`client = MongoClient('mongodb://sara:sara@3.34.49.195', 27017)` 로 변경해줌 

8. 파일질라에서 실행하고자 하는 `app.py`등 폴더/파일을 옮겨 업로드 
```
cd ~
cd my_projects
python app.py
```
9. `app.py`가 실행 되면서 authorization 문제는 발생하지 않음. 다만 크롬브라우저 설치를 따로 해줘야 하는 문제 발생 
http:3.34.49.195:5000 하면 접속 가능해짐!! 
