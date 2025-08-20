import json
# 读取JSON文件内容
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
            return json.dumps(json_content, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"读取JSON文件时出错: {e}")
        return None

