# -parking-control-system
<h2>一个小型的物联网系统——基于蓝牙的停车入口控制系统。依赖了互联网通信和蓝牙通信。
<p>物联网的核心在于物与物以及人与物之间的信息交互。物联网要实现的主要功能有：一、全面感知。利用各种感知手段，对物体进行信息采集和获取。二、可靠传送。将物体接入信息网络，依靠通信网络，实现信息交互和共享。三、智能处理。对数据和信息进行分析并处理，实现智能化控制.

<h2>设计Web服务器的WebAPI
<p>API与用户的通信协议，使用HTTPs协议。HTTP是一个基于请求与响应模式的、无状态的、应用层的协议，常基于TCP的连接方式。客户向服务器请求服务时，只需传送请求方法和路径，在接受和解释请求消息后，服务器返回一个HTTP响应消息。REST（Representational State Transfer）是一种Web服务器架构风格,它从资源的角度看待整个网络。REST设计中，将所有事物都抽象为资源并为每个资源定义唯一的资源标识符URI，使用统一的接口对资源进行操作

<h3>WebAPI接口
<p>接口功能:    发送公钥     |获取公钥|获取令牌|  判断令牌       |判断结果<br/>
请求参数	beacon_id, pubkey|	无	 |client_id|beacon_id,pubkey|client_id<br/>
URL示例	beacon/pubkey/?beacon_id=123&pubkey=123 <br/>
HTTP请求方式	GET
<h3>数据交互格式	JSON

<h3>本课题中选择将服务器的运行环境定为Linux+Nginx+MySQL+Python
