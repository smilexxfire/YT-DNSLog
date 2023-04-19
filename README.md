# YT-DNSLog
一款轻量级、无依赖, 支持自定义的DNSLOG程序

## 安装
```
git clone https://github.com/smilexxfire/YT-DNSLog.git
```

## 运行
```
python3 main.py
```
发起DNS查询试试，成功接收到请求

![image-20230419183227801](https://qiniu.xxf.world/pic/2023/04/19/6301e205-2019-470c-998f-eaed2237dfed.png)

![image-20230419171443292](https://qiniu.xxf.world/pic/2023/04/19/0b568262-403f-4d35-859b-41127c4dcb8c.png)

## 备注
运行前需自行配置好NS记录和A记录，如1个域名和1个公网IP的典型配置如下

![image-20230419170802234](https://qiniu.xxf.world/pic/2023/04/19/b07851fc-a53e-4d03-b0d3-3318005ee16e.png)

检查53端口，程序会占用53端口

默认所有DNS查询都返回127.0.0.1，如设置返回指定IP可修改module/message.py 65行

![image-20230419171039691](https://qiniu.xxf.world/pic/2023/04/19/d6285c2e-5d1d-4956-80e2-86ad8d16320d.png)