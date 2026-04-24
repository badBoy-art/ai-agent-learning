from openai import OpenAI

# DeepSeek API 配置
client = OpenAI(
    api_key="sk-32d5a3300557486f934147157415c2da",
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-chat"


# ============================================
# 练习1: 多轮对话
# ============================================

def chat_multi_turn():
    """多轮对话 - 保持上下文"""
    print("=" * 50)
    print("练习1: 多轮对话 (输入 quit 退出)")
    print("=" * 50)
    
    # 初始化对话历史
    messages = [
        {"role": "system", "content": "你是一个有用的助手"}
    ]
    
    while True:
        # 获取用户输入
        user_input = input("\n你: ").strip()
        
        # 检查退出命令
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("再见!")
            break
        
        if not user_input:
            continue
        
        # 添加用户消息到历史
        messages.append({"role": "user", "content": user_input})
        
        try:
            # 调用 API
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            
            # 获取 AI 回复
            ai_reply = response.choices[0].message.content
            
            # 添加 AI 回复到历史
            messages.append({"role": "assistant", "content": ai_reply})
            
            # 显示回复
            print(f"AI: {ai_reply}")
            
        except Exception as e:
            print(f"错误: {e}")


# ============================================
# 练习2: 流式输出
# ============================================

def chat_stream():
    """流式输出 - 打字机效果"""
    print("=" * 50)
    print("练习2: 流式输出 (输入 quit 退出)")
    print("=" * 50)
    
    messages = [
        {"role": "system", "content": "你是一个有用的助手"}
    ]
    
    while True:
        user_input = input("\n你: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("再见!")
            break
        
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            # 流式调用
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True  # 开启流式
            )
            
            # 收集完整回复
            full_response = ""
            print("AI: ", end="", flush=True)
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    print(content, end="", flush=True)  # 逐字打印
            
            print()  # 换行
            
            # 保存到历史
            messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"\n错误: {e}")


# ============================================
# 练习3: 保存对话历史
# ============================================

import json
from datetime import datetime

def save_history(messages, filename="chat_history.json"):
    """保存对话历史到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "messages": messages
        }, f, ensure_ascii=False, indent=2)
    print(f"\n对话已保存到: {filename}")


def load_history(filename="chat_history.json"):
    """从文件加载对话历史"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"加载历史记录: {data['timestamp']}")
            return data['messages']
    except FileNotFoundError:
        print("没有找到历史记录，开始新对话")
        return [{"role": "system", "content": "你是一个有用的助手"}]


def chat_with_save():
    """带保存功能的对话"""
    print("=" * 50)
    print("练习3: 带保存的对话")
    print("=" * 50)
    print("命令:")
    print("  quit/exit/q - 退出")
    print("  save - 保存对话")
    print("  load - 加载历史")
    print("  clear - 清空对话")
    print("=" * 50)
    
    # 初始化对话历史
    messages = [
        {"role": "system", "content": "你是一个有用的助手"}
    ]
    
    while True:
        user_input = input("\n你: ").strip()
        
        # 处理命令
        if user_input.lower() in ['quit', 'exit', 'q']:
            # 退出前询问是否保存
            save_input = input("是否保存对话? (y/n): ").strip().lower()
            if save_input == 'y':
                save_history(messages)
            print("再见!")
            break
        
        elif user_input.lower() == 'save':
            save_history(messages)
            continue
        
        elif user_input.lower() == 'load':
            messages = load_history()
            continue
        
        elif user_input.lower() == 'clear':
            messages = [{"role": "system", "content": "你是一个有用的助手"}]
            print("对话已清空")
            continue
        
        elif not user_input:
            continue
        
        # 添加用户消息
        messages.append({"role": "user", "content": user_input})
        
        try:
            # 流式输出
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True
            )
            
            full_response = ""
            print("AI: ", end="", flush=True)
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    print(content, end="", flush=True)
            
            print()
            
            # 保存到历史
            messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"\n错误: {e}")


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    print("\n请选择练习:")
    print("1. 多轮对话")
    print("2. 流式输出")
    print("3. 带保存的对话")
    print("4. 运行全部")
    
    choice = input("\n请输入选择 (1/2/3/4): ").strip()
    
    if choice == '1':
        chat_multi_turn()
    elif choice == '2':
        chat_stream()
    elif choice == '3':
        chat_with_save()
    elif choice == '4':
        print("\n--- 练习1: 多轮对话 ---")
        chat_multi_turn()
        print("\n--- 练习2: 流式输出 ---")
        chat_stream()
        print("\n--- 练习3: 带保存的对话 ---")
        chat_with_save()
    else:
        print("无效选择")
