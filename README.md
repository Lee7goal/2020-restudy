# 2020新的一年对旧的一年一些项目的翻新，顺便巩固一下基础的知识

## 2020/06/12

### 从最基础的豆瓣250开始重做

写成了类的形式，还使用了单例模式，注释算是写的比较清楚，能够给新手非常清楚的思路

引入类使用
```python
from douban_250 import DouBan

# 实例化对象
db = DouBan()

# 爬取所有信息到容器中并使用print查看
db.get_all_info()
print(db.content)

# 保存爬取到的信息到本地json文件供以后使用
db.save()

# 爬取指定页数的信息，虽然没啥用，但是写出来了
db = DouBan('这里填入你要的页数')
db.get_choice_info()
db.save()
```

注意上方的save()方法会将原先的json信息清空