# Tuple 元组 - 不可变的列表
# 一旦创建就不能修改

# 1. 创建元组
point = (3, 4)
colors = ("红", "绿", "蓝")
single = (1,)  # 单元素元组需要逗号

print(f"坐标: {point}")
print(f"颜色: {colors}")

# 2. 访问元素
print(f"X坐标: {point[0]}")
print(f"Y坐标: {point[1]}")

# 3. 元组解包
x, y = point
print(f"解包: x={x}, y={y}")

# 4. 元组不可变 (以下操作会报错)
# point[0] = 5  # ❌ TypeError

# 5. 元组作为字典的键
locations = {
    (0, 0): "原点",
    (1, 0): "东",
    (0, 1): "北"
}
print(f"位置: {locations[(0, 0)]}")


# 6. 函数返回多个值
def get_min_max(numbers):
    return min(numbers), max(numbers)


result = get_min_max([3, 1, 4, 1, 5, 9])
print(f"最小值: {result[0]}, 最大值: {result[1]}")

# 解包
min_val, max_val = get_min_max([3, 1, 4, 1, 5, 9])
print(f"最小值: {min_val}, 最大值: {max_val}")
