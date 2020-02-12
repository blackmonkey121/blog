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
>static : `theme/default/static`
>
>templates: `theme/default/templates`

## Part 2 Setting

*settings path：`/blog/djangoBlog/djangoBlog/settings/`*

- base : consistent config
- develop: develop config
- product: product config



## Part 3 THEMES

#### Default theme files PATH

`/theme`

#### 1 Default theme files

`/theme/default`

#### 2 Add New Theme

- Create a new theme directory under the `/theme/`   eg:_`/theme/milk`_
- There should be template directory and static files directory in the new directory `/theme/milk/` eg:`/theme/milk/static/` & `/theme/milk/templates/`
- Use newly created theme in settings  eg:`settings.develop.THEME_NAME = 'milk'`

## Part 4 Environment and installation and deployment

### 1. environment
- Mysql 8.0.15
- redis 5.0.4
- Python 3.6.5
- django 1.11

### 2. Complete dependency information: [requirements.txt](https://github.com/blackmonkey121/blog/blob/master/requirements.txt)
* Django~=1.11.26
* PyMySQL~=0.9.3
* celery~=3.1.18
* celery-with-redis~=3.0
* django-redis~=3.8.4
* django-redis-sessions~=0.5.6
* redis~=2.10.6
* itsdangerous==1.1.0 
* xadmin==0.6.1
* Pillow==7.0.0
* django-rest-framework==0.1.0 
* coreapi==2.3.3  
* django-ckeditor==5.4.0 
* mistune==0.8.4

### 3. Install & running
*Make sure MySQL Redis and Python3.6.x are installed.*

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
