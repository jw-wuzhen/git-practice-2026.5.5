import requests
from bs4 import BeautifulSoup
import re

# 模拟浏览器请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_baike_infobox(url):
    try:
        # 获取页面内容
        resp = requests.get(url, headers=headers)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 适配新版百科 infobox：查找所有 basicInfo-block
        data = []
        for dl in soup.find_all("dl", class_=re.compile(r"basicInfo-block")):
            dt_tags = dl.find_all("dt", class_=re.compile(r"basicInfo-item name"))
            dd_tags = dl.find_all("dd", class_=re.compile(r"basicInfo-item value"))
            for dt, dd in zip(dt_tags, dd_tags):
                key = dt.get_text(strip=True).rstrip(":：")
                val = dd.get_text(strip=True)
                data.append((key, val))
        if data:
            print(f"新版infobox提取到 {len(data)} 条数据")
            return data

        # 兼容旧版
        infobox = soup.find("div", class_="basic-info cmn-clearfix") or soup.find("div", class_="basic-info") or soup.find("div", {"class": lambda x: x and "basic-info" in x})
        if infobox:
            name_tag = infobox.find("dt", class_="basicInfo-item name")
            value_tag = infobox.find("dd", class_="basicInfo-item value")
            if name_tag and value_tag:
                key = name_tag.get_text(strip=True).rstrip("：")
                val = value_tag.get_text(strip=True)
                data.append((key, val))
            rows = infobox.find_all("div", class_="basicInfo-row")
            for row in rows:
                name = row.find("dt", class_="basicInfo-item name")
                value = row.find("dd", class_="basicInfo-item value")
                if name and value:
                    key = name.get_text(strip=True).rstrip("：")
                    val = re.sub(r"\s+", " ", value.get_text(strip=True))
                    data.append((key, val))
            print(f"旧版infobox提取到 {len(data)} 条数据")
            return data

        print("未找到infobox")
        return []
    except Exception as e:
        print(f"爬取失败: {e}")
        return []

def get_baike_infobox_from_file(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        
        data = []
        # 适配新版百科 infobox
        for dl in soup.find_all("dl", class_=re.compile(r"basicInfoBlock_CPCqm")):
            for item in dl.find_all("div", class_=re.compile(r"itemWrapper_zVsFh")):
                dt = item.find("dt", class_=re.compile(r"basicInfoItem_YOC73"))
                dd = item.find("dd", class_=re.compile(r"basicInfoItem_YOC73"))
                if dt and dd:
                    key = dt.get_text(strip=True).replace("\xa0", "").replace("：", "")
                    val = dd.get_text(" ", strip=True)
                    data.append((key, val))
        print(f"从本地HTML提取到 {len(data)} 条数据")
        return data
    except Exception as e:
        print(f"解析失败: {e}")
        return []

def to_triple(entity, infobox_data):
    # 转换为三元组 <实体, 属性, 属性值>
    triples = []
    for attr, value in infobox_data:
        triples.append(f"<{entity}, {attr}, {value}>")
    return triples

if __name__ == "__main__":
    # 从本地HTML文件解析林则徐百度百科 infobox
    filepath = "林则徐.html"
    infobox = get_baike_infobox_from_file(filepath)
    
    # 转换为三元组
    entity = "林则徐"
    triples = to_triple(entity, infobox)
    
    # 输出结果
    print(f"民族英雄：{entity}")
    print("三元组表示：")
    for t in triples:
        print(t)

    # --- 知识图谱可视化 ---
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'networkx', 'matplotlib'])
        import networkx as nx
        import matplotlib.pyplot as plt

    G = nx.DiGraph()
    for triple in triples:
        # triple 格式为 <主语, 谓语, 宾语>
        triple = triple.strip('<>')
        h, r, t = [x.strip() for x in triple.split(',', 2)]
        G.add_edge(h, t, label=r)

    pos = nx.spring_layout(G, k=1.5)
    plt.figure(figsize=(14, 9))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_family='SimHei')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_family='SimHei')
    plt.title(f"{entity} 知识图谱", fontproperties='SimHei', fontsize=18)
    plt.tight_layout()
    plt.show()