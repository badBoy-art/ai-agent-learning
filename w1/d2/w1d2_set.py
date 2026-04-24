# Set 集合 - 无序不重复
# 类似 Java 的 HashSet

# 1. 创建集合
fruits = {"苹果", "香蕉", "橙子"}
numbers = {1, 2, 3, 4, 5}
empty_set = set()  # 空集合要用 set()，不能用 {}

print(f"水果集合: {fruits}")
print(f"数字集合: {numbers}")

# 2. 添加/删除
fruits.add("葡萄")
print(f"添加葡萄后: {fruits}")

fruits.remove("香蕉")  # 不存在会报错
print(f"删除香蕉后: {fruits}")

fruits.discard("芒果")  # 不存在不会报错

# 3. 集合操作
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

print(f"集合1: {set1}")
print(f"集合2: {set2}")

# 并集
print(f"并集: {set1 | set2}")

# 交集
print(f"交集: {set1 & set2}")

# 差集
print(f"差集: {set1 - set2}")

# 对称差集
print(f"对称差集: {set1 ^ set2}")

# 4. 去重
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = list(set(numbers))
print(f"去重前: {numbers}")
print(f"去重后: {unique}")

# 5. 集合推导式
squares = {x ** 2 for x in range(10)}
print(f"平方集合: {squares}")
