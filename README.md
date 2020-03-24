
## 安装xadmin
安装过程中可能报decode错误，解决方法参考：https://blog.csdn.net/qingche456/article/details/58279692
```python
pip install xadmin-master.zip
```


## 安装debug_toolbar
安装过程参考：https://blog.csdn.net/Intro_z/article/details/81948065


## 安装djdt_flamegraph
* 安装过程参考：https://www.cnpython.com/pypi/djdt_flamegraph
* 注意必须使用`python manage.py runserver --nothreading --noreload`启动项目，因为flame图只能在单线程服务器中生成。
* 在windows上启动django项目时可能会抛`AttributeError: module 'signal' has no attribute 'SIGALRM'`异常，这是因为
windows不支持**SIGALRM**信号，详情参考：https://blog.csdn.net/polyhedronx/article/details/81988335?utm_source=blogxgwz6