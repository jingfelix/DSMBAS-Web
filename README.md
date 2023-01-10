# DSMBAS-Web

[DSMBAS](https://github.com/jingfelix/DSMBAS)的前后端部分

## 1 Structure

本仓库包含除Injector外的所有部分，包括前端，后端，虚拟机内的Exacutor

![structure-1](https://felix-bucket-0.s3.ladydaily.com/structure-1.png)

## 2 User Interface

使用[MDUI](https://mdui.org)作为前端框架

![ui-2](https://felix-bucket-0.s3.ladydaily.com/ui-2.png)

![ui-1](https://felix-bucket-0.s3.ladydaily.com/ui-1.png)

实现了基本的移动端适配

<div>
    <img src="https://felix-bucket-0.s3.ladydaily.com/ui-3.png" alt="ui-3" width="44.5%" />
    <img src="https://felix-bucket-0.s3.ladydaily.com/ui-4.png" alt="ui-4" width="44%" />
</div>

## 3 Details

### 3.1 后端实现

后端采用flask作为主要web框架，使用flask_login插件实现用户相关的API，使用flask_sqlalchemy实现与数据库交互的ORM模型。

#### 3.1.1 Web框架

Flask框架是最流行的Python Web框架之一，其具有轻量化，易上手，可拓展的特点，可以快速搭建起所需的Web服务。强大的Flask插件生态也为实现更高级的功能提供了便利。在本项目中，实现了一个提供多功能模块，提供14个API的完整，强健的后端。

后端API与用途如下所示：

| 路由名          | HTTP方法 | 用途                      |
| ------------ | ------ | ----------------------- |
| /            | GET    | 响应返回登录界面                |
| /u/login     | POST   | 用户登录                    |
| /u/logout    | POST   | 用户登出                    |
| /u/register  | POST   | 用户注册                    |
| /u/delete    | POST   | 用户注销                    |
| /u/dashboard | GET    | 响应返回控制台界面；渲染已执行和未执行任务列表 |
| /u/upload    | POST   | 为前端提供上传文件的接口            |
| /u/msg       | GET    | 获取当前用户的未读信息             |
| /t           | POST   | 执行器通过该API上报执行信息         |
| /e/gettask   | GET    | 执行器获取分配的目标的id           |
| /e/download  | GET    | 执行器下载指定目标的可执行文件         |
| /e/endtask   | POST   | 执行器运行完毕后标识结束任务          |
| /e/errortask | POST   | 执行器运行出错                 |
| /e/report    | GET    | 返回已完成目标的运行报告            |

flask_login为 Flask 提供对用户 session 的管理。它能够处理登录，注销和长时间记住用户 session 等常用任务。在本项目中，使用该插件管理用户登录和页面权限控制。

#### 3.1.2 数据库

flask_sqlalchemy是一个为Flask应用提供Sqlalchemy支持的插件。在ORM模型下，数据库中的表和项被映射为Python对象，从而可以使用Python函数和方法进行操作，极大简化了后端CRUD效率。本项目使用该插件创建了一个具有两张表的数据库，数据库表的具体结构如下：

User

| 列名            | 类型  | 用途               |
| ------------- | --- | ---------------- |
| id            | 整数  | 主键，作为区分不同用户的唯一标识 |
| name          | 字符串 | 用户名，可重复          |
| password_hash | 字符串 | 密码的哈希值，避免明文保存密码  |
| msg           | 字符串 | 用户未查看的通知         |

Target

| 列名          | 类型  | 用途               |
| ----------- | --- | ---------------- |
| id          | 整数  | 主键，作为区分不同目标的唯一标识 |
| name        | 字符串 | 目标名，可重复          |
| status      | 布尔型 | 状态，标识当前目标是否完成执行  |
| finish_time | 时间  | 记录目标的完成时间        |
| user_id     | 整数  | 该目标所属的用户的id      |
| args        | 字符串 | 执行该目标所需的命令行参数    |
| assigned    | 整数  | 该目标在任务分配阶段的状态    |
| warning     | 整数  | 警告数量             |
| error       | 整数  | 错误数量             |
| api_count   | 整数  | 截获的API数量         |
| info        | 字符串 | 截获的API的具体参数信息    |

### 3.2 前端实现

#### 3.2.1 UI实现

前端页面使用了两种不同的UI框架进行设计和实现。交互层使用jQuery进行搭建。

登录，注册和登出界面选用MVP.css进行搭建。MVP.css是一个最小化的CSS样式表，支持所有基本的HTML元素。只需要引入CSS文件，即可直接使用原生HTML元素构建网页，适合快速构建网站主页和博客。本项目中参照MVP.css的官方样例实现了具有两个输入框，提示信息和提交按钮的的登陆页面，按照后端API适配后即可直接使用。

控制台和运行报告界面使用了MDUI进行构建。MDUI是一个遵循Material Design设计规范的前端UI框架。MDUI具有轻量化，无依赖，高性能，易上手，支持响应式布局的特点。Material Design是由谷歌提出和推广的设计语言，适用于各类网站与移动端应用。MDUI是Material Design的一个极简前端实现，通过引入必须的CSS和JS文件，即可快速在HTML文件中通过修改元素的类来生成不同的样式和组件。

本项目中使用MDUI构建了大部分UI和控件。为了遵循MD设计规范，尽可能不修改样式规范。总体布局上，仿照Cloudflare的站点控制台和阿里云的安全仪表盘。采用侧边栏+工具栏+主体的方式进行布局。配色上选取了和Cloudflare一致的白色主色，橙色主题色和蓝色强调色。

交互层方面，本项目引入了jQuery，以实现比原生JavaScript更方便的HTML访问。从而实现更美观易用的空间。同时，使用jQuery中封装的Ajax请求，也能够更好地与后端交互。

#### 3.2.2 文件构建

需要承认，本分析系统的Web部分没有实现完全的前后端分离。受限于本人Web开发水平，前端页面的部分构建是由后端完成的。优点：减少了后端API的数量，作为单人开发的项目，能够保证开发者对全局有充分的控制。缺点：前端页面依赖后端控制，开发流程中需要兼顾前端布局界面和后端的数据处理，项目越复杂，进行进一步开发添加新功能就越困难。

后端对HTML的代码生成采用了Flask内置的jinja2引擎，通过自定义字符串的方式进行匹配替换，从而实现对指定内容的自定义修改。

## 4 Deployment

Web部分可以部署于Linux或Windows服务器上

在项目文件目录下编写必要的.env文件，以下为一个例子：

```bash
FLASK_DEBUG=True
FLASK_APP=core
SECRET_KEY=secret
SERVER_NAME=0.0.0.0
```

准备阶段，可在项目文件目录下执行以下命令：

```bash

// 初始化数据库并清除原数据库
flask initdb --drop

// 初始化管理员账户
flask admin

// 完全重新开始服务，将执行以上两条命令的内容
flask restart
```

运行服务器：

```bash
flask run

// 或
python ./main.py
```

在本项目中推荐使用第二种，以避免复杂的环境变量设置问题

## 5 License

本项目采用MIT License，但请不要直接抄袭
