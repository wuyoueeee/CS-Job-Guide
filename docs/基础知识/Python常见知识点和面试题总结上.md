# Python常见知识点和面试题总结（上）
## Python 语言特点
Python 是一种高级编程语言，具有以下特点：

1. 易学易用：Python 语法简洁清晰，易于理解和学习。它的代码可读性强，能够提高开发效率和代码的可维护性。

2. 动态解释型：Python 是一种动态解释型语言，它不需要编译成二进制代码，可以直接执行源代码。这使得 Python 在开发过程中具有快速迭代的优势。

3. 跨平台性：Python 支持多个主流操作系统，包括 Windows、Linux、macOS 等，可以在不同平台上运行。

4. 面向对象：Python 支持面向对象编程，具有类、继承、封装和多态等特性，可以更好地管理代码，提高代码的可重用性和可扩展性。

5. 高级内置数据类型：Python 内置了许多高级数据类型，如列表、字典、元组、集合等，可以方便地处理各种数据结构。

6. 强大的标准库：Python 拥有丰富的标准库，包括网络、文件、GUI、数据库、图像处理等各种模块，可以满足大多数开发需求。

7. 第三方库丰富：Python 生态系统中有大量的第三方库，可以扩展 Python 的功能，如科学计算、机器学习、Web 开发等。

8. 开放源代码：Python 是一种开放源代码的语言，可以自由地使用、分发和修改 Python 的源代码，也鼓励开发者贡献代码。

## Python为什么比较慢,如何改进
1. 解释型语言：Python 是一种解释型语言，代码需要在运行时进行解释，并转换为字节码执行。这个过程可能比编译型语言的直接转换机器码更耗时。

2. 全局解释器锁（GIL）：Python 中的 GIL 是一种互斥锁，用于保护共享资源。它在同一时间只允许一个线程执行 Python 代码，这可能会使多线程的 CPU 密集型任务在同一时间只能使用一个 CPU 核心，从而导致性能下降。

3. 动态类型检查：Python 是一种动态类型语言，在变量赋值时不需要显式地声明变量类型，这使得 Python 在运行时需要进行类型检查，相比静态类型语言，可能会导致一些性能损失。

4. 内存管理：Python 中的内存管理使用引用计数和垃圾回收机制。这些机制在一些场景下可能会引入一些额外的开销，例如创建和销毁 Python 对象所需的时间。

5. 模块导入：Python 中的模块导入机制可能会导致一些额外的开销，例如搜索模块路径、编译字节码等。
   
改进：
1. 减少内存占用。

2. 使用内置函数和库。

3. 将计算移到循环外。

4. 保持小的代码库。

5. 避免不必要的循环

## 解释型和编译型语言的区别
编译型语言需要先将源代码编译成可执行的机器码，然后再执行程序；而解释型语言则是在运行时逐行解释执行源代码。因此，编译型语言需要编译时间，但执行效率较高；解释型语言则无需编译时间，但执行效率较低。

## 简述下 Python 中的字符串、列表、元组和字典
字符串是 Python 中的文本类型，用于存储字符序列；列表是一种有序的可变序列类型，用于存储多个元素；元组是一种有序的不可变序列类型，用于存储多个元素；字典是一种无序的键值对类型，用于存储多个键值对。

## 简述上述数据类型的常用方法
字符串常用方法包括：查找、替换、大小写转换、分割、连接等；列表常用方法包括：添加、删除、排序、反转等；元组常用方法包括：查询、拼接、转换为列表等；字典常用方法包括：添加、删除、查询、遍历等。
## 简述 Python 中的字符串编码
Python 中的字符串编码包括 ASCII、Unicode 和 UTF-8 等。ASCII 编码是一种 7 位编码，可以表示 128 种字符；Unicode 是一种可以表示全球所有字符的编码，包括 ASCII 编码；UTF-8 是一种可变长度的 Unicode 编码，兼容 ASCII 编码。

## is 和 == 的区别
is 判断两个对象是否是同一对象，即它们的 id 是否相同；而 == 判断两个对象的值是否相等。
## Python中in 和 exist区别
在 Python 中，in 和 exist 都用于判断某个元素是否在一个序列中，但是它们的用法有所不同。

1. **in**：用于判断某个元素是否在一个序列中，返回布尔值。可以用于字符串、列表、元组、集合等序列类型，语法为 element in sequence。
例如：
```
str1 = "hello"
list1 = [1, 2, 3, 4, 5]
tuple1 = (6, 7, 8, 9, 10)
set1 = {11, 12, 13, 14, 15}

print("h" in str1)     # True
print(6 in tuple1)     # True
print(0 in list1)      # False
print(10 in set1)      # True
```
2. **exist**：用于判断某个文件或目录是否存在，返回布尔值。可以用于判断文件或目录是否存在，语法为 os.path.exist(path)。
例如：
```
import os

file_path = "test.txt"
dir_path = "test_dir"

print(os.path.exists(file_path))  # False
print(os.path.exists(dir_path))   # True
```
in 和 exist 的用法和功能是不同的，in 用于序列中元素的查找，exist 用于文件和目录的查找。
## Python 函数中的参数类型
Python 函数中的参数类型包括：位置参数、默认参数、可变参数和关键字参数。位置参数通过参数位置传递，必须按照函数定义的顺序传递；默认参数在函数定义时指定默认值，可以不传递；可变参数使用 *args 表示，接受任意数量的位置参数，传递时使用 * 将参数序列展开；关键字参数使用 **kwargs 表示，接受任意数量的关键字参数，传递时使用 ** 将参数字典展开。
## *arg 和 **kwarg 作用
*arg 和 **kwarg 分别用于在函数定义时接受可变数量的位置参数和关键字参数。*arg 表示接受任意数量的位置参数，传递时使用 * 将参数序列展开；**kwarg 表示接受任意数量的关键字参数，传递时使用 ** 将参数字典展开。
## PEP8 规范
PEP8 是 Python 官方推荐的代码风格规范，包括缩进、命名、注释、空格等方面的要求。遵循 PEP8 规范可以使代码更易读、易维护、易扩展。
## 可变类型与不可变类型
Python 中的可变类型包括列表、字典等，可以在原地修改其值；而不可变类型包括数字、字符串、元组等，不能在原地修改其值，只能重新赋值。
## filter、map、reduce 的作用
filter、map 和 reduce 是 Python 中的三个常用高阶函数。filter 用于筛选序列中符合条件的元素；map 用于对序列中的每个元素执行函数操作；reduce 用于对序列中的元素进行累积计算。这三个函数的返回值均为迭代器。
## re 的 match 和 search 区别
re 模块中的 match 函数用于在字符串开头匹配正则表达式，而 search 函数则用于在字符串中查找匹配正则表达式的子串。如果需要匹配整个字符串，可以使用 match 函数；如果需要在字符串中查找匹配的子串，可以使用 search 函数。
## python列表和字典底层原理实现
Python中的列表和字典是常用的数据结构，它们的底层实现原理如下：

1. 列表底层实现原理
Python中的列表是一种可变的有序序列，可以存储任意类型的数据。在Python中，列表是通过动态数组实现的。

当你创建一个空列表时，Python会分配一块内存来存储该列表的元素。当你向列表中添加元素时，Python会检查是否有足够的内存来存储新元素，如果有，就将新元素添加到列表的末尾；如果没有，Python会分配一块更大的内存来存储列表元素，并将原来的元素复制到新的内存区域中，然后再将新元素添加到列表的末尾。这个过程称为“重新分配内存”。

删除元素时，Python会将列表中的元素向左移动来填补删除的元素，并将列表的大小减少1。如果列表中的元素数量少于实际分配的内存大小的一半，Python会将列表的内存大小缩小为实际需要的大小，这个过程称为“收缩内存”。

2. 字典底层实现原理
Python中的字典是一种可变的无序键值对集合，可以存储任意类型的数据。在Python中，字典是通过哈希表实现的。

当你创建一个空字典时，Python会分配一块内存来存储该字典的元素。当你向字典中添加一个键值对时，Python会将键哈希为一个整数，然后使用这个整数来作为哈希表的索引，将值存储在哈希表中。如果哈希表的索引已经被占用，Python会使用开放定址法或链式哈希表等方法来解决冲突。

查找一个键值对时，Python会先将键哈希为一个整数，然后使用这个整数来作为哈希表的索引，查找对应的值。如果哈希表中没有这个键值对，Python会返回KeyError异常。

删除一个键值对时，Python会将键哈希为一个整数，然后使用这个整数来作为哈希表的索引，查找对应的值。如果哈希表中有这个键值对，Python会将这个键值对从哈希表中删除。如果哈希表中的键值对数量少于实际分配的内存大小的一半，Python会将哈希表的内存大小缩小为实际需要的大小，这个过程称为“收缩内存”。
## python with用法
在 Python 中，with 语句提供了一种方便的方式来管理代码块中的资源，比如文件、网络连接和数据库连接等。它可以自动地为资源分配和释放资源，避免了手动管理资源的麻烦，并且可以保证资源在使用后被正确地关闭或释放。

with 语句的一般语法如下：
```
with expression [as variable]:
    with-block
```
其中，expression 是一个返回上下文管理器对象的表达式，with-block 是一个语句块，variable 是一个可选的变量名，用于存储上下文管理器返回的值。

当执行 with 语句时，Python 会调用上下文管理器对象的 __ enter __ 方法进入上下文管理器，并在 with-block 中执行代码。当代码块执行完毕时，Python 会调用上下文管理器对象的 __ exit __ 方法退出上下文管理器，并释放资源。

下面是一些 with 语句的示例用法：

1. 打开文件并读取内容：

```
with open('file.txt') as f:
    contents = f.read()
```
这个例子中，open 函数返回一个上下文管理器对象，当 with 语句开始执行时，Python 会调用 open 函数返回的对象的  __ enter __ 方法打开文件。在 with 代码块中，我们可以读取文件内容并存储在 contents 变量中。当代码块执行完毕时，Python 会自动调用上下文管理器对象的 __ exit__ 方法关闭文件。
2. 向数据库插入数据：
```
with connect('localhost', 'user', 'password', 'database') as conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', ('John', 'john@example.com'))
    conn.commit()
```
这个例子中，connect 函数返回一个上下文管理器对象，当 with 语句开始执行时，Python 会调用 connect 函数返回的对象的 __ enter__ 方法建立与数据库的连接。在 with 代码块中，我们可以执行 SQL 命令并提交事务。当代码块执行完毕时，Python 会自动调用上下文管理器对象的 __ exit__ 方法关闭数据库连接。

在 with 语句中，as 子句是可选的，如果省略了 as 子句，则上下文管理器返回的值将被忽略。如果指定了 as 子句，则上下文管理器返回的值将存储在指定的变量中，可以在 with 代码块中使用。

总之，with 语句提供了一种方便的方式来管理资源，避免了手动管理资源的麻烦，并且可以保证资源在使用后被正确地关闭或释放。
## Python常见的单元测试工具
Python 中常用的单元测试工具包括：

1. unittest：Python 自带的单元测试框架，提供了断言方法和测试用例的组织方式，可以方便地编写和执行测试用例。unittest 支持测试套件、测试用例、测试装置等功能。

2. pytest：第三方的单元测试框架，具有更加简单易用的语法和更加丰富的插件支持，可以快速编写和执行测试用例。pytest 支持参数化测试、测试装置、测试过滤等功能。

3. nose：第三方的单元测试框架，可以自动发现和执行测试用例，支持测试装置、测试过滤、测试覆盖率等功能。nose 的语法与 unittest 相似，但使用起来更加方便。

4. doctest：Python 自带的文档测试工具，可以从文档字符串中提取测试用例，并执行测试并验证结果。doctest 可以方便地与文档维护一致，但只适用于简单的测试场景。

5. tox：第三方的测试工具，可以自动化地在不同的 Python 版本和环境中运行测试，以确保代码的兼容性和稳定性。tox 可以方便地集成到持续集成系统中，自动执行测试并生成测试报告。
## python中有什么排序
1. 冒泡排序（Bubble Sort）：重复地遍历要排序的序列，比较相邻的两个元素，如果顺序不对就交换它们，直到序列有序为止。

2. 插入排序（Insertion Sort）：将序列分为已排序和未排序两部分，依次将未排序的元素插入到已排序的序列中，保持已排序的序列始终有序。

3. 选择排序（Selection Sort）：遍历序列，找到最小的元素，将其与序列的第一个元素交换位置，然后从剩余的元素中找到最小的元素，将其与序列的第二个元素交换位置，以此类推。

4. 快速排序（Quick Sort）：选定一个基准元素，将序列中小于基准元素的元素放在左边，大于基准元素的元素放在右边，然后递归地对左右两个子序列进行排序。

5. 归并排序（Merge Sort）：将序列分为若干个子序列，对每个子序列进行排序，然后合并所有子序列，得到最终有序序列。

6. 堆排序（Heap Sort）：将序列看作是一棵完全二叉树，将其转换为一个大根堆或小根堆，然后依次取出堆顶元素，重新调整堆，直到序列有序为止。

以上是常见的几种排序算法，Python 中的内置函数 sorted() 和列表的 sort() 方法也是常用的排序工具。

## Python连接数据库
Python 可以通过多种方式连接数据库，以下是其中常用的几种方式：

1. 使用 Python 内置的 sqlite3 模块连接 SQLite 数据库。SQLite 是一种轻量级的关系型数据库，没有独立的服务器进程，数据以文件的形式存储在本地磁盘上。连接 SQLite 数据库的代码示例如下：
```
import sqlite3

# 连接 SQLite 数据库
conn = sqlite3.connect('test.db')

# 创建游标对象
cursor = conn.cursor()

# 执行 SQL 查询
cursor.execute('SELECT * FROM table_name')

# 获取查询结果
result = cursor.fetchall()

# 关闭游标和连接
cursor.close()
conn.close()
```
2. 使用第三方库连接其他关系型数据库，例如 MySQL、PostgreSQL、Oracle 等。常用的第三方库有 MySQLdb、psycopg2、cx_Oracle 等。连接 MySQL 数据库的代码示例如下：
```
import MySQLdb

# 连接 MySQL 数据库
conn = MySQLdb.connect(host='localhost', user='root', password='password', db='database_name')

# 创建游标对象
cursor = conn.cursor()

# 执行 SQL 查询
cursor.execute('SELECT * FROM table_name')

# 获取查询结果
result = cursor.fetchall()

# 关闭游标和连接
cursor.close()
conn.close()
```
3. 使用 ORM 框架连接数据库，例如 SQLAlchemy、Django ORM 等。ORM 框架可以将数据库操作封装成面向对象的方法，使得操作数据库更加方便和灵活。连接 MySQL 数据库并执行查询的代码示例如下：
```
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建数据库引擎
engine = create_engine('mysql+pymysql://root:password@localhost/database_name')

# 创建会话工厂
Session = sessionmaker(bind=engine)

# 创建基类
Base = declarative_base()

# 定义数据模型
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

# 创建会话对象
session = Session()

# 执行查询
result = session.query(User).all()

# 关闭会话
session.close()
```
## Python反转字符串
Python 中可以使用切片（slice）来反转字符串，即将字符串从后往前切片，步长为 -1，代码示例如下：
```
s = "hello world"
s_reversed = s[::-1]  # 切片反转字符串
print(s_reversed)  # 输出：dlrow olleh
```
也可以使用 reversed() 函数反转字符串，代码示例如下：
```
s = "hello world"
s_reversed = ''.join(reversed(s))  # 使用 reversed() 函数反转字符串
print(s_reversed)  # 输出：dlrow olleh
```
## Python生成随机数
Python 中可以使用 random 模块生成随机数，常用的方法有以下几种：

1. random.random()：生成一个 0 到 1 之间的随机小数。
```
import random

x = random.random()
print(x)  # 输出：0.123456789
```
2. random.randint(a, b)：生成一个在指定范围内的随机整数，包括 a 和 b。
```
import random

x = random.randint(1, 100)
print(x)  # 输出：42
```
3. random.choice(seq)：从序列中随机选择一个元素。
```
import random

seq = ['apple', 'banana', 'orange']
x = random.choice(seq)
print(x)  # 输出：banana
```
4. random.shuffle(seq)：将序列中的元素随机排序。
```
import random

seq = ['apple', 'banana', 'orange']
random.shuffle(seq)
print(seq)  # 输出：['orange', 'apple', 'banana']
```