# Mymg 我的管理系统
**不再维护,计划使用Golang重写**
## 开发环境
Python3.6+Flask
默认使用Sqlite3,如需使用Mysql可修改weapp下的config.py文件
## 数据功能
微言、时间、计划、朋友 总共4个功能
### 微言
你可以发一些牢骚，也可以写一些自由自己可以看到的星系
### ~~时间~~
~~反馈自己每天都干了些什么，记录进程~~
### ~~计划~~
~~有计划？想要执行？利用计划可以控制自己的节奏~~
### 朋友
朋友模块可以记录朋友的基本信息，对了，还有生日提醒功能，想要实现生日提醒或计划任务提醒？那一定要配置邮件和计划任务哦。

## 配置文件
在配置文件中配置数据库
在配置文件中配置邮箱
在界面中修改自己的资料，修改自己的的邮箱作为接收提醒邮件的邮箱
为了触发邮件发送，需要添加计划任务来访问 {你的站点/mail}的地址哦

## Windows
windows先下载Python3.6然后再点击一键安装就ok了

**时间和计划功能并不常用，所以，在后面的版本去除**
## 功能截图
![avatar](./img/01.JPG)
![avatar](./img/fr.JPG)
![avatar](./img/sr.JPG)
![avatar](./img/user.JPG)
