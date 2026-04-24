# 四、实例属性和方法
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner  # 实例属性
        self.balance = balance

    def deposit(self, amount):
        # 存款
        if amount > 0:
            self.balance += amount
            print(f"存入 {amount} 元，余额: {self.balance} 元")
        else:
            print("存款金额必须大于0")

    def withdraw(self, amount):
        # 取款
        if amount > self.balance:
            print("余额不足")
        elif amount <= 0:
            print("取款金额必须大于0")
        else:
            self.balance -= amount
            print(f"取出 {amount} 元，余额: {self.balance} 元")

    def get_balance(self):
        # 查询余额
        return self.balance

    def __str__(self):
        # 字符串表示
        return f"银行账户(户主: {self.owner}, 余额: {self.balance}元)"


# 使用
account = BankAccount("张三", 1000)
print(account)  # 银行账户(户主: 张三, 余额: 1000元)

account.deposit(500)  # 存入 500 元，余额: 1500 元
account.withdraw(200)  # 取出 200 元，余额: 1300 元
print(f"余额: {account.get_balance()} 元")
