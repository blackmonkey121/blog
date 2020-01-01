# DjangoBlog
New technology training ground for Python3.x (Django Blogs)！

# 基于 Django 框架实现的多人博客项目
### 项目介绍：


## 环境：

    Mysql 8.0.15
    redis 5.0.4
    Python 3.6.5
    django 1.11

### 其他详细环境配置 同 requirements.txt 文件
    Django~=1.11.26
    PyMySQL~=0.9.3
    celery~=3.1.18
    celery-with-redis~=3.0
    django-redis~=3.8.4
    django-redis-sessions~=0.5.6
    redis~=2.10.6

# 项目介绍


# 业务流程


# 开发日志


# 部署与使用

## 关于环境

## 关于主题

### 创建新的模版主题
Themes由前端来构建（HTML、CSS、JavaScript）
其中 CSS JS 插件等静态文件都放在static目录下

#### 1 静态文件（引入的外部插件框架文件等）
>/static

>例如 小图标文件 /static/fontawesome

> 通知插件 /static/toastr

#### 2 默认的主题构成
>通用样式: /static/css/theme/default/default.css
>页面顶部导航栏: /static/css/theme/default/navbar

>HTML: /themes/default/template

#### 3 新增主题
>尽可能的不修改HTML文件，这样所有的修改都不会涉及的themes文件只是修改JS和CSS文件即可。
>如需要修改，应改在themes目录下新增一个单独的和default目录同级的目录存放新的主题HTML。
>注意：需要到设置中即/djangoBlog/settings/base.py 或 develop 或 product中修改 
>THEME 变量的值。当前的THEME为 THEME = 'default'



