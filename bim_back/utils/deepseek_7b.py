import requests

def local_api_7b(file_path):

    # 从文件中读取内容
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
        # with open(path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在，请检查路径是否正确。")
        return None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None
    path = r'C:\Users\16021\Desktop\毕设\规范\规范3.txt'
    with open(path, 'r', encoding='utf-8') as standard:
        standard_content = standard.read()
    # 将文件内容添加到 query 中
    query = f'''
    你是一位专精于建筑法规合规性评估的建筑法规专家，擅长分析建筑描述与规范要求的合规性。
    请根据给定的BIM待审查文件{file_content}和规范条文{standard_content}，判断待审查文件中的信息是否符合条文要求。
    要求：
    1.逐个判断待审查文件中的每条属性信息
    2.请仅返回csv格式，具体包含：审查属性,规范条目,是否合规
    '''
    data = {
        "model": "deepseek-r1:7b",
        "prompt": query,
        "stream": False  # 是否以流式返回（可设为 True/False）
    }
    response = requests.post(
        "http://localhost:11434/api/generate",
        json=data
    )
    result = response.json()['response']
    return result




