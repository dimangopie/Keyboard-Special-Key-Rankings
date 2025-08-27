import json


def clean_string(string: str) -> str:
    """清理字符串，去除首尾空白和换行符"""
    return string.strip().rstrip("\n")


def parse_special_key_line(line: str) -> dict:
    """解析特殊键的一行数据，返回特殊键信息字典"""
    special_key_dict = {
        "level_value": -1,
        "name": "",
        "key_value": -1,
        "scan_code": -1,
        "description": ""
    }
    string_list = line.split(":")
    if len(string_list) != 5:
        return special_key_dict  # 返回默认值，表示解析失败

    # 清理每个字段
    cleaned_list = [clean_string(part) for part in string_list]

    # 解析字段
    special_key_dict["name"] = cleaned_list[0]
    try:
        special_key_dict["key_value"] = int(cleaned_list[1]) if cleaned_list[1] else -1
        special_key_dict["scan_code"] = int(cleaned_list[2].replace(' ', ''), base=16) if cleaned_list[2] else -1
        special_key_dict["level_value"] = int(cleaned_list[3])
        special_key_dict["description"] = cleaned_list[4]
    except ValueError:
        print(f"解析错误: {line}")
    return special_key_dict


def load_special_keys(file_path: str) -> list:
    """从文件中加载特殊键数据"""
    special_key_list = []
    with open(file_path, mode="r", encoding="UTF-8") as fp:
        for line in fp:
            if line.startswith("#"):
                continue  # 跳过注释行
            special_key_info = parse_special_key_line(line)
            if special_key_info["level_value"] != -1:  # 只添加成功解析的特殊键
                special_key_list.append(special_key_info)
    return special_key_list


def initialize_ranking_dict() -> dict:
    """初始化排名字典"""
    return {
        "0": {
            "level_value": 0,
            "level_name": "夯",
            "keys": []
        },
        "1": {
            "level_value": 1,
            "level_name": "顶级",
            "keys": []
        },
        "2": {
            "level_value": 2,
            "level_name": "人上人",
            "keys": []
        },
        "3": {
            "level_value": 3,
            "level_name": "NPC",
            "keys": []
        },
        "4": {
            "level_value": 4,
            "level_name": "拉",
            "keys": []
        }
    }


def categorize_special_keys(special_keys: list) -> dict:
    """根据特殊键的等级分类"""
    ranking_dict = initialize_ranking_dict()
    level_mapping = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4"
    }
    for key_info in special_keys:
        level_key = level_mapping.get(key_info["level_value"], None)
        if level_key:
            ranking_dict[level_key]["keys"].append(key_info)
    return ranking_dict


def save_ranking_to_json(ranking_data: dict, file_path: str):
    """将排名数据保存到 JSON 文件"""
    with open(file_path, mode="w", encoding="UTF-8") as fp:
        json.dump(ranking_data, fp, indent=4, ensure_ascii=False)


def main():
    """主函数，程序入口"""
    # 加载特殊键数据
    special_key_list = load_special_keys("special_key_reference_table.txt")

    # 按等级分类特殊键
    ranking_dict = categorize_special_keys(special_key_list)

    # 保存分类后的数据到 JSON 文件
    save_ranking_to_json(ranking_dict, "ranking.json")

    # 打印结果用于验证
    print("生成的排名数据:")
    print(json.dumps(ranking_dict, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()