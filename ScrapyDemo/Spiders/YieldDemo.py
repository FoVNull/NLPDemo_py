b = 10
def test(x) -> int:
    for i in range(1,x):
        a = i * 10
        print("start")
        yield a + b
    for i in range(1,x):
        a = i * 100
        yield a + b
    return 114514


# 带了yield函数就成为了一个generator
g = test(5)
print(g)

# generator是一种特殊的iterator，它缓存了函数式而非值，遍历时执行并返回yield的值

# yield就像是打了断点，next(g)就继续执行到下一个断点，同时返回yield中的内容
print(next(g))
print("---")
b += 10
print(next(g))
print("---")
print(next(g))
while True:
    try:
        print(next(g))
    except StopIteration:
        break

