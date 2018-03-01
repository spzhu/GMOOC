### problems

#### makemigrations后migrate报错django.db.migrations.exceptions.InconsistentMigrationHistory
```
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency users.0001_initial on database 'default'.
```
执行语句与已有数据库产生冲突，删除数据库表重新migrate

#### model 中出现的循环引用

> A import B ; B import A 产生死循环

**解决方法： APP models分层**

采用分层的app设计方式，使用更高层次的operation app操作model

#### models.ForeginKey报错
> TypeError: __init__() missing 1 required positional argument: 'on_delete'

django1.11以上ForeignKey有两个必需的参数to，on_delete  [django2.0_ForeignKey](https://docs.djangoproject.com/en/2.0/ref/models/fields/#foreignkey)
```
class ForeignKey(to, on_delete, **options)
```
#### xadmin的兼容性问题
> python3.6+Django2.0 从github下载django2版本的源码安装

