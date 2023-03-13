> 代码无特别之处，只是简单实现，已开源，github地址：，可根据需求进行二次开发；
> **需要至少了解python环境的搭建，python中依赖包的安装等操作**；
> **需要注意：openai免费账号响应速度时快时慢，而微信公众号要求回复速度必须在5秒内，因此会有失败的概率，付费版账号没使用过，响应速度暂时未知**。

<a name="FvpIp"></a>
# 1.环境说明

- 运行此python程序，需python3环境，并应确保使用pip3安装其运行所需的所有依赖，具体命令如下：
```shell
# xxx为依赖包名
pip3 install xxx
```
<a name="TlmOi"></a>
# 2.配置说明
具体配置含义见下方代码块，需按需自行配置调整，需要说明的：

1. 中括号`[]`中的内容（如`[server]`），称为`**section**`，不了解编程的话，不要改动其内容，否则会使程序因读取配置失败而奔溃；
2. `;`后的内容为注释，即会被程序忽略的文字，用于备注代码含义等，与配置无关的内容，必须在其每行文字最前面加上`;`号；
3. 代码中中间件的配置及使用（如redis），需对其有基本的了解，在此不做细述；
4. 因为暂时没有做动态刷新配置，所以对配置文件做了改动，需要重启程序。
```properties
;以下配置请根据实际情况更改
[server]
;服务器地址,默认localhost(本地)
host=localhost
;端口号,微信对接必须使用80或443端口,如果想使用其他端口,可以使用nginx转发
port=8008
;会话时间(秒),超过时间,上下文将过期,开启新的openai会话
session_time=300
;已回答问题缓存时间(秒),建议比session_time大
answer_cache_time=600
;是否需要控制提问间隔,可选:True/False
interval_flag=True
;提问间隔(秒),interval_flag为True时生效
interval=10
;过于频繁提问,提示信息
too_many_question='太多问题了,请稍后再试...'

[openai]
;openai的key
key=xxxxxxx

[weixin]
;以下信息都可以在微信公众平台查到
;微信公众号id
appId=xxxxxxx
;密钥
appSecret=xxxxxxx
;连接token
token=xxxxxxx
;加密key
encodingAesKey=xxxxxxx

[redis]
;使用了redis进行缓存和提问频率限制,一定程度上保证服务可用性
;redis的服务地址
host=127.0.0.1
;redis的端口号,通常默认是:6379
port=6379
;redis的密码
password=123456
;本服务使用的redis数据库号(0~16),默认0
db=0
```
<a name="D86H0"></a>
# 3.后续
另外还有一个Java版本的，可以做到动态调整配置参数而不需要重启应用，但其设计稍微复杂了些，不适合快速部署使用，暂时就不出文档了，可以扫码试用：<br />![qrcode_for_gh_1b0487915597_258.jpg](https://cdn.nlark.com/yuque/0/2023/jpeg/12707100/1678673894720-da6b19db-8bb1-47d9-a5a7-9e9a2a60055f.jpeg#averageHue=%23a1a0a0&clientId=uafd4398d-be80-4&from=ui&id=ue98d3a9b&name=qrcode_for_gh_1b0487915597_258.jpg&originHeight=258&originWidth=258&originalType=binary&ratio=1&rotation=0&showTitle=true&size=28026&status=done&style=stroke&taskId=ue6728ca6-782c-413a-a72a-f00d588f2e4&title=%E4%BD%93%E9%AA%8C%E7%89%88wechatGPT "体验版wechatGPT")<br />后续可能会将此python版也集成docker，更易管理，时间有限，暂时就先做到这里。
