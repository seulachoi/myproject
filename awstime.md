# AWS 시간대를 서울로 맞추기 

##EC2에서 디폴트 시간대는 한국 시간이 아닌, 미국 시간일 수 있음. Linux에서 미국 태평양 시간 PST-> 한국 표준시 KST로 변경

```
$ sudo rm /etc/localtime
$ sudo ln -s /usr/share/zoneinfo/Asia/Seoul /etc/localtime
$ date
Mon Aug  1 16:49:06 KST 2019
```
