# 基本结构

Tornado 是一个网络应用框架，同时也是一个异步网络库。

编写网络应用程序,使用框架的时候我们需要做的就是编写对应的处理的类。

一般情况下，我们会编写一个通用的父类，然后所有的类都继承这个类。

如下：
```python

from tornado.web import RequestHandler

class Base(RequestHandler):

    def current_user(self):
        pass
    
    def other_methods(self):
        pass


class OtherProduceHandler(Base):

    def get(self, regex_args_1, regex_args_2, *args, **kwargs):
        
        self.render("template_name.html", **kwargs)
        # self.write("bytes or dict or list") 
```

处理类有了之后我们就需要启动这个应用。

Tornado同样有服务器，所以在我们不需要其他的服务器软件的，就可以启动应用。

我们需要创建app, 启动服务，启动循环。

如下：
```python

from tornado.web import Application
from tornado.ioloop import IOLoop

def make_app():
    return Application(
            [
                (r"/hello", HelloHandler)
            ]           
        )


def main():
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()


if __name__ == "__main__":
    main()

```

当然如果需要更多的用法可以看Application支持的参数。可以设置模板位置，静态文件位置，会话设置等。
也就是说通过app获取的一切配置都可以在这里进行设置。

# 模板

Tornado 和其他网络应用框架一样有自己的模板语法。他也支持自使用其他模板语言编译为模板字符串然后渲染。

模板语法主要有控制语句和表达式组成。同时还支持在`RequestHandler`命名空间下的一些方法或属性。例如：`current_user`, `static_url`。

控制语句主要是在`{% %}`并以`{% end %}`结尾， 表达式在`{{  }}`

模板同时支持继承，主要是用关键字 `extends` 和 `block` 语句实现

