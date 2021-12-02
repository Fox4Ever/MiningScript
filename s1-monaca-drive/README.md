# Introduction

持续挂机可以让你**迅速增长 following，因为好多人是自动回关的**，所以你懂得。

# Usage

本脚本基于 `selenium` 实现，由于需要钱包环境，所以建议大家用 chrome App 在本地开一个 debug port ，使用真实的浏览器环境来做。启动方式如下（macOS 系统）：

```shell
$ export PATH="/Applications/Google Chrome.app/Contents/MacOS:$PATH"
$ alias chromedev="Google\ Chrome --remote-debugging-port=9222 --user-data-dir='~/ChromeProfile'"
$ chromedev
```

另外你需要去 chromedriver [官网下载](https://chromedriver.chromium.org/)一个你的设备可用的 `chromedriver` 并丢在脚本的同级目录下。

最后就是运行脚本代码，这里简单的用 bfs 实现了一个 N 度好友的遍历，用随机数来保证页面停留时间的变化，防止风控。

```shell
$ python3 run.py
```

最后简单放一下成功运行的图：

![](https://raw.githubusercontent.com/Desgard/img/master/img/%E6%88%AA%E5%B1%8F2021-12-01%20%E4%B8%8A%E5%8D%889.46.32%20(2).png)

个人 twitter: https://twitter.com/defi_gua

有问题评论区可以随时回复我，一起赚钱。