from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '118668079'
API_KEY = 'hOHDpLN6dCr5KGIoIrhJDZgA'
SECRET_KEY = 'avINkfd97VcPl81izoQJWXCaihWbrn0L'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def baidu_ocr_text(img_p_n):
    # 百度文本识别 AipOcr
    image = open(img_p_n, 'rb').read()
    # 识别模式，有好几种，下面有介绍
    msg = client.basicGeneral(image)
    text = 'result:\n'
    for i in msg.get('words_result'):
        text += (i.get('words') + '\n')
    print(type(text))
    text = text.replace('\u04B0', '').replace('\uFFE5', '').replace('\u00A5', '')
    return text


def save_to_txt(text, save_path):
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(text)


def main():
    img_path = r"C:\Users\16021\Desktop\毕设\规范\建筑窗口洞口大小\421ac218-3ab3-42d9-bd32-02ce7a2e24d4-04.png"
    result_text = baidu_ocr_text(img_path)
    print(result_text)
    save_path = r"C:\Users\16021\Desktop\ocr_result.txt"  # 指定保存路径
    save_to_txt(result_text, save_path)
    print(f"识别结果已保存到：{save_path}")


if __name__ == '__main__':
    main()