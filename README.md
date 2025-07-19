# 🛒 网上商城系统

一个基于 Tkinter 和 MySQL 的简单网上商城系统 Demo，支持用户注册、登录、商品查询与增删、订单查询与修改。适合学习 GUI 开发和数据库操作。

## 📌 项目简介

本项目通过 Tkinter 实现图形界面，连接 MySQL 数据库（`shopping` 数据库），提供以下功能：
- 用户注册与登录
- 商品查询、添加、删除
- 订单查询与修改

代码结构清晰，适合初学者学习 Tkinter、MySQL 和 GUI 应用程序开发。

## 📂 项目结构

```bash
├── demo.py          # 主程序（GUI 和数据库逻辑）
├── welcome.jpg      # 登录界面背景图片
├── logo.ico         # 窗口图标
├── report.pdf       # 项目详细报告
└── README.md        # 项目文档
```

## 📦 安装与配置

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置 MySQL 数据库**：
   - 创建 `shopping` 数据库，包含以下表：
     - `user`：存储用户名和密码（`name`, `password`）
     - `product`：存储商品信息（`cid`, `cname`, `cprice`, `cbrand`）
     - `orders`：存储订单信息（`oid`, `id`, `type`, `cid`, `price`, `calls`, `btime`）
   - 更新 `demo.py` 中的数据库连接参数（默认：`host="localhost"`, `user="root"`, `password="123456"`, `database="shopping"`）。

3. **运行程序**：
   ```bash
   python demo.py
   ```

## 🎯 项目目标

提供一个简单的 Tkinter + MySQL Demo，帮助开发者：
- 学习 GUI 界面开发（Tkinter 和 ttkbootstrap）
- 实践数据库操作（MySQL 增删改查）
- 快速搭建类似的管理系统

## 📮 联系方式

如有问题或反馈，请联系：
📧 [HELLOLE_369@126.com]