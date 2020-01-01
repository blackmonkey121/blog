# DjangoBlog
&emsp;&emsp;*Multiplayer Online Blog System Based on Django Framework*

## Part 1 Project Overview
### 1. Entity

- User
- Article
- Category
- Tag
- Link
- Comment
- Sidebar

### 2. applications

##### &emsp;&emsp;1 user
##### &emsp;&emsp;2 blog
##### &emsp;&emsp;3 config
##### &emsp;&emsp;4 comment

### 3. databases

##### &emsp;&emsp;1 MySQL
##### &emsp;&emsp;2 Redis

### 4. themes
##### &emsp;&emsp;eg:default :
>&emsp;&emsp;Templates:`/blog/themes/default`  
>&emsp;&emsp;STATIC:`/static/themes/default`

##### &emsp;&emsp;eg:milk :
>&emsp;&emsp;Templates:`/blog/themes/milk`  
>&emsp;&emsp;STATIC:`/static/themes/milk`


## Part 2 Environment and installation and deployment
### environment
- Mysql 8.0.15
- redis 5.0.4
- Python 3.6.5
- django 1.11

### Complete dependency information: [requirements.txt](https://github.com/blackmonkey121/blog/blob/master/requirements.txt)
* Django~=1.11.26
* PyMySQL~=0.9.3
* celery~=3.1.18
* celery-with-redis~=3.0
* django-redis~=3.8.4
* django-redis-sessions~=0.5.6
* redis~=2.10.6

### install & running
1 Make sure MySQL Redis and Python3.6.x are installed.
>1. MySQL install &emsp;&emsp; __[Windows](https://jingyan.baidu.com/article/cbcede0753155b02f40b4d17.html)__ &emsp;&emsp;&emsp; __[Linux](https://blog.csdn.net/weixin_44198965/article/details/91891985)__ &emsp;&emsp;&emsp; __[macOS](https://blog.csdn.net/qq_36004521/article/details/80637886)__
>2. Redis install &emsp;&emsp; __[Windows](https://jingyan.baidu.com/article/0f5fb099045b056d8334ea97.html)__ &emsp;&emsp;&emsp; __[Linux](https://www.cnblogs.com/gaojingya/p/10600418.html)__ &emsp;&emsp;&emsp; __[macOS](https://www.cnblogs.com/monkey-code/p/11345217.html)__
>3. Python install &emsp;&emsp; __[Windows](https://blog.csdn.net/cx55887/article/details/88911266)__ &emsp;&emsp;&emsp; __[Linux](https://www.cnblogs.com/yimiflh/p/9542439.html)__ &emsp;&emsp;&emsp; __[macOS](https://www.jianshu.com/p/98a19215ade6)__
>> Tips: *These links are No Q/A*
>4. In the same directory as the requirements.txt file  
`pip install -r requirements.txt`
>> Tips: *If you want to make the project working in your virtual environment,I
think you should make sure the virtual environment is already running.*

>5. In the same directory as the manage.py file  
`./manage.py runserver 127.0.0.1:8000`


## Part 3 Development Log

- [x] Create project.
- [x] Init project configuration.
- [x] Create Model Class.
- [x] Init admin views for apps.
- [x] Init user module.
- [x] Finish blog views based on functions views FIXME: based on class views.
- [x] User email registration with Celery redis.
- [x] Submit FormData using AJAX.
- [x] Complete base demands.
- [x] Optimize the code structure and overwrite blog views based on class views.
- [x] Optimize the registration.
- [x] Complete private visitor public view and data separation.
- [x] Complete the default theme!
- [x] Adjust project structure and separate topics and optimize code.


## Part 4 Setting
*settings path：`/blog/djangoBlog/djangoBlog/settings/`*
- base : consistent config
- develop: develop config
- product: product config


## Part 5 THEMES

#### 1 Default theme files
&emsp;&emsp;*static path : /static/themes/default*  
&emsp;&emsp;*templates path : /themes/default/*

#### 2 Add New Theme
**eg: milk**  
&emsp;&emsp;/static/themes/milk  
&emsp;&emsp;/themes/milk
