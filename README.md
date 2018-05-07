# yajp

## What
A naive json parser

## Why

For practice, For fun, For learning, For nothing

## install

Download the source code, cd into the directory, type

    python3 setup.py install

## usage

code

    from yajp import loads
    loads("{\"hello\": \"world\"}")

output(dict)

    {'hello': 'world'}

error

    from yajp import loads, ParseError
    try:
        loads("")
    except ParseError as e:
        print(e.line, e.column, e.description)

output

    1 0 No Input

it means error occur at line 1, column 0, error because no input detected.

if you dont catch error

    from yajp import loads
    loads("")

output

    yajp.errors.DecodeError: No Input: At line 1 column 0

other

escape supported(less than 32 is not a valid escape character), UTF-8 supported

---
## 这是啥
一个naive的json解释器

## 为什么要写这个
练习

## 安装
下载源码, 进入目录, 命令行键入 

    python3 setup.py install

## 使用指北

代码

    from yajp import loads
    loads("{\"hello\": \"world\"}")

输出(字典)

    {'hello': 'world'}

错误

    from yajp import loads, ParseError
    try:
        loads("")
    except ParseError as e:
        print(e.line, e.column, e.description)

输出
    
    1 0 No Input

表明错误出在第一行, 第0列, 原因是No Input

如果你不捕获异常

    from yajp import loads
    loads("")

输出

    yajp.errors.DecodeError: No Input: At line 1 column 0

还有啥
兹兹转义字符(小于32的转义为不合法转义), 兹兹utf-8