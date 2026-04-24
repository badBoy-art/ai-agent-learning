# List 列表 - 最常用的数据结构 类似 Java 的 ArrayList

# 1. 创建列表
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]  # 可以混合类型

print(f"水果列表: {fruits}")
print(f"数字列表: {numbers}")
print(f"混合列表: {mixed}")

# 2. 访问元素 (索引从 0 开始)
print(f"第一个水果: {fruits[0]}")  # 苹果
print(f"最后一个水果: {fruits[-1]}")  # 葡萄
print(f"前两个: {fruits[0:2]}")  # ['苹果', '香蕉']

# 3. 添加元素
fruits.append("芒果")  # 末尾添加
print(f"添加芒果后: {fruits}")

fruits.insert(1, "草莓")  # 在指定位置插入
print(f"插入草莓后: {fruits}")

fruits.extend(["西瓜", "荔枝"])  # 添加多个元素
print(f"扩展后: {fruits}")

# 4. 删除元素
fruits.remove("香蕉")  # 删除指定元素
print(f"删除香蕉后: {fruits}")

popped = fruits.pop()  # 删除并返回最后一个
print(f"弹出的元素: {popped}")

del fruits[0]  # 删除指定索引的元素
print(f"删除第一个后: {fruits}")

# 5. 列表操作
print(f"列表长度: {len(fruits)}")
print(f"苹果出现次数: {fruits.count('苹果')}")
if '苹果' in fruits:
    print(f"苹果的索引: {fruits.index('苹果')}")
else:
    print(f"没苹果")

print(f"橙子的索引: {fruits.index('橙子')}")

# 6. 列表排序
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"排序前: {numbers}")

numbers.sort()  # 原地排序
print(f"排序后: {numbers}")

numbers.reverse()  # 反转
print(f"反转后: {numbers}")

# 7. 列表推导式 (Python 特色)
squares = [x ** 2 for x in range(10)]
print(f"平方数: {squares}")

evens = [x for x in range(20) if x % 2 == 0]
print(f"偶数: {evens}")

# 8. 遍历列表
print("遍历水果列表:")
for fruit in fruits:
    print(f"  - {fruit}")

# 带索引遍历
print("带索引遍历:")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")
