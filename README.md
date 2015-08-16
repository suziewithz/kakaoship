#kakaoship

Installation
--------------
You will need to install the following

  - python 2.7.9
  - konlpy
  ```
  $ sudo pip install konlpy
  ```
  - Java 7
  ```
  $ sudo apt-get install g++ openjdk-7-jdk
  ```
  
Getting Started
--------------

  - Run analyzer.py
```
[kakaoship] $ python analyzer.py [log_path]
ex) python analyzer.py kakaotalk.txt
```

Functions
--------------
  - number of messages by sender.
  - bytes by sender.
  - count "ㅋ" used in chatroom by sender.
  - messages sent by time.
  - number of emoticons sent by sender.
  - (Undeveloped) response time (easy to calculate in 1:1 chat room)
  - calculate intimacy between members (by counting replies. there can be another way to show intimacy between members)
  - analyze most frequently used keywords -> need to improve. so many unimportant keywords.
  
Things to consider
--------------
  - None yet.
