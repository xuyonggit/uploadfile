web端一键上传文件到服务器
=========================

# 环境安装
```
pip install -r requirements
```

# 运行
```
cd uploadfile
python uploadfile.py
```

# 配置文件config 解析
## option <filetypes>
支持文件格式
默认：gz bz2 zip tar tgz txz 7z war txt zip
### 新增文件格式
配置：filetypes 空格隔开
## option <file_dir>
服务器文件存储目录
* 注意：windows 系统要用双反斜杠'\\'
## option <app_bind_ip>
绑定IP
## option <app_bind_port>
绑定端口
## option <file_limit_size>
文件上传大小限制 MB
## clear_key
页面清理文件口令
