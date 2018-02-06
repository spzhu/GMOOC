# GMOOC 实战设计文档

### APP 设计

- courses 课程管理
- organization 机构和教师管理
- users 用户管理
- operation 操作管理

### models 设计

#### user model

继承django后台内置auth_user的model类AbstractUser

```
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    ...

```

### problems

#### makemigrations后migrate报错django.db.migrations.exceptions.InconsistentMigrationHistory
```
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency users.0001_initial on database 'default'.
```
执行语句与已有数据库产生冲突，删除数据库表重新migrate
