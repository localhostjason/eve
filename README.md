# Eve restful api脚手架框架

eve教程：https://docs.python-eve.org/en/stable

changeLog: https://docs.python-eve.org/en/stable/changelog.html

目前暂时不维护，理由：
1. 不主流
1. eve相关插件都停止维护，使用的人太少。

场景：
1. 自己搭建简单的服务器
1. 不使用大型且逻辑复杂的应用


部署一：
1. python manage.py start|stop

不支持 windows. 仅支持Linux daemon

部署二：
搭配其他中间件，比如：apache、nginx部署 ，配置wsgi


DEBUG调试:
python manage.py runserver

-h ip
-p 端口
-db init db创建
-upgrade_db db升级
- deploy 初始化数据