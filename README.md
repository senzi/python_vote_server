# Python 局域网投票系统 #
----------
## 使用方法： ##
1. 修改list文件，确定可以投票人的名单
2. 使用vote_server.py搭建投票服务器
3. 客户端使用`telnet 172.31.200.53 4567` 命令连接服务器
4. (具体连接哪个ip，服务器会显示出来，端口默认为：4567)

## 功能： ##

- 可以对10个东西进行投票
- 投票结果即时显示，回车键可以刷新
- 投票结果自动排序，降序显示 
- 投票结果显示支持率
- 只有`list`上有学号的人才能投票
- 每人只能投票一次
- `quit`命令可以退出

<a href="http://panjiansen.com/wp-content/uploads/2014/06/voteserver.png"><img src="http://panjiansen.com/wp-content/uploads/2014/06/voteserver.png" alt="voteserver" width="553" height="492" class="aligncenter size-full wp-image-183" /></a>

<a href="http://panjiansen.com/wp-content/uploads/2014/06/voting.png"><img src="http://panjiansen.com/wp-content/uploads/2014/06/voting.png" alt="voting" width="589" height="636" class="aligncenter size-full wp-image-184" /></a>

<a href="http://panjiansen.com/wp-content/uploads/2014/06/result.png"><img src="http://panjiansen.com/wp-content/uploads/2014/06/result.png" alt="result" width="589" height="600" class="aligncenter size-full wp-image-185" /></a>


