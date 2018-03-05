## problems

### makemigrations后migrate报错django.db.migrations.exceptions.InconsistentMigrationHistory
```
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency users.0001_initial on database 'default'.
```
执行语句与已有数据库产生冲突，删除数据库表重新migrate

### model 中出现的循环引用

> A import B ; B import A 产生死循环

**解决方法： APP models分层**

采用分层的app设计方式，使用更高层次的operation app操作model

### models.ForeginKey报错
> TypeError: __init__() missing 1 required positional argument: 'on_delete'

django1.11以上ForeignKey有两个必需的参数to，on_delete  [django2.0_ForeignKey](https://docs.djangoproject.com/en/2.0/ref/models/fields/#foreignkey)
```
class ForeignKey(to, on_delete, **options)
```
### xadmin的兼容性问题

> python3.6+Django2.0 从github下载django2版本的源码安装

formtools导入出现错误，使用pip install -U django-formtools更新到最新版本

### xadmin管理页面点击邮箱验证码出现IndexError: list index out of range

> 参考[django2.0 分支 AdminSplitDateTime 里render()方法处理错误](https://github.com/sshwsfc/xadmin/issues/499)

AdminSplitDateTime.render()传入的input_html没有'\n',
修改xadmin源码widget.py文件的AdminSplitDateTime.render(),如下：

```
    ...
    input_html = [ht for ht in super(AdminSplitDateTime, self).render(name, value, attrs).split('/><') if ht != '']
    if (len(input_html) > 1):
        input_html[0] = input_html[0] + "/>"
        input_html[1] = "<" + input_html[1]
    ...
```

### CRSF验证失败，禁止访问
Django的安全机制，为了防止跨域的提交，会进行CSRF token验证
在form中加入csrf_token
```
<form>
    ...
    {% csrf_token %}
</form>
```

### urls分发，include

> include()namespace报错Specifying a namespace in include() without providing an app_name

python3 Django 环境下，如果namespace没有注册以及在根目录下urls.py中的include方法的第二个参数namespace添加之后就出错的问题。
需要在[app_name]目录下的urls.py中的urlpatterns前面加上app_name='[app_name]'， [app_name]代表应用的名称。

django文档示例:

urls.py
```
from django.urls import include, path

urlpatterns = [
    path('author-polls/', include('polls.urls', namespace='author-polls')),
    path('publisher-polls/', include('polls.urls', namespace='publisher-polls')),
]
```
polls/urls.py
```
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    ...
]
```
