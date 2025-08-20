from utils import api_test

def api(file_path):

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
    # query = f'''
    # 假设你是bim审查师，以下是待审查文件：\n{file_content},
    # 以下是《建筑窗口洞口大小》和《住宅设计规范》等国家规范标准\n{standard_content}，
    # 请帮我审查一下待审查文件门和窗的尺寸大小及层高是否规范化\n
    # 要求:1.输出以csv表格的格式:具体审查属性,规范条目,是否合规
    # 2.逐一审查各项内容，将所有内容审查完毕
    # 3.每一行审查一条属性的高和宽
    # 4.只输出csv表格内容，不输出其他内容
    # '''
    query = f'''
    你是一位专精于建筑法规合规性评估的建筑法规专家，擅长分析建筑描述与规范要求的合规性。
    请根据给定的BIM待审查文件{file_content}和规范条文{standard_content}，判断待审查文件中的信息是否符合条文要求。
    要求：
    1.逐个判断待审查文件中的每条属性信息
    2.请仅返回csv格式，具体包含：审查属性,规范条目,是否合规（是或否）
    '''
    appid = "177106f3"
    api_secret = "MGRhYmYxYTI2ZGVhNTY2NGZlMDllY2U3"
    api_key = "ba787f45cf08aa1150add330eb35fdf2"
    Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat"
    domain = "4.0Ultra"
    result = api_test.call_spark_api(appid,api_secret,api_key,Spark_url,domain,query)
    return result




