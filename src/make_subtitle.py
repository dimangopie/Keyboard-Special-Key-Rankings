import json
import os.path
import re

from src.main import deal_file_name


def read_key_ranking_data() -> list[dict]:
    ranking_file_path : str = "/home/mango/IdeaProjects/Keyboard-Special-Key-Rankings/src/ranking.json"
    _keys_list : list = []
    with open(file=ranking_file_path, mode="r", encoding="UTF-8") as fp:
        data = json.load(fp)

    for level in "01234":
        for _key in data[level]["keys"]:
            _keys_list.append(_key)

    return _keys_list


def save_subtitle_list(subtitle_list : list[str]):
    for nth, subtitle_string in enumerate(subtitle_list):
        subtitle_list[nth] = deal_file_name(subtitle_list[nth])
        print(subtitle_list[nth])
    with open(file="../resource/subtitle_list.json", mode="w", encoding="UTF-8") as fp:
        subtitle_list.sort()
        json.dump(obj=subtitle_list, fp=fp , indent=4, ensure_ascii=False)


def main():
    subtitle_list = ["键盘特殊键从夯到拉"]
    keys_message_list = read_key_ranking_data()
    playing_count = len(keys_message_list)

    for i in range(playing_count):
        key_message = keys_message_list[i]
        content : str =key_message["description"]
        key_name = key_message["name"]
        subtitle_list.append(f"下一个是 `{key_name}`")


        line_list : list[str] = content.split("\\n")
        for line in line_list:
            subtitle_list.append(f"{line}")

        level_name = key_message["level_name"]
        subtitle_list.append(f"这里我给到 `{level_name}`")

    save_subtitle_list(subtitle_list=subtitle_list)

if __name__ == '__main__':
    main()
