import json
import random
import subprocess
from manim import *


class KeyLabel(VGroup):
    def __init__(self, key_message : dict):
        self.level_value : int = key_message["level_value"]
        self.name : str = key_message["abbreviation"]
        self.key_value : int = key_message["key_value"]
        self.scan_code : str = key_message["scan_code"]
        self.description : str = key_message["description"]
        super().__init__(KeyLabel.init_key_label(self.name))

    @staticmethod
    def init_key_label(content : str) -> VGroup:
        text_length = len(content)
        height = Screen.base_height * 0.4
        width = text_length / 6 + 0.5
        width = width if width >= height else height
        _key_label = RoundedRectangle(corner_radius=0.08, fill_opacity=1, fill_color=DARKER_GRAY, color=WHITE, height=height, width=width)
        key_label_content = Text(text=content, color=WHITE, font_size=20)
        return VGroup(_key_label, key_label_content).scale(scale_factor=8 / 5)

    def animate_of_move_to_screen_bar(self):
        list_of_key_within_bar : list[Mobject] = Screen.table_of_key_label_within_bar_bodies[self.level_value]
        if len(list_of_key_within_bar) == 0:
            animate = self.animate.scale(scale_factor=5 / 8).next_to(mobject_or_point=Screen.bar_body_list[self.level_value].get_left(), direction=RIGHT, buff=0.2)
        else:
            animate = self.animate.scale(scale_factor=5 / 8).next_to(mobject_or_point=list_of_key_within_bar[-1].get_right(), direction=RIGHT, buff=0.2)
        list_of_key_within_bar.append(self)
        return animate

class Screen(Scene) :
    ranking_file_path : str = "/home/mango/IdeaProjects/Keyboard-Special-Key-Rankings/src/ranking.json"
    bar_head_message_list : list[tuple[str, str]] = [("夯", "#FB0601"), ("顶级", "#FFC601"), ("人上人", "#FCFA11"), ("NPC", "#FFEFCE"), ("拉", "#FFFFFF")]
    bar_body_color : str = "#6b6160"
    background_height : float = 8
    background_width : float = 256 / 9
    bar_count : int = 5
    base_height : float = background_height / bar_count
    square_side_length : float = base_height

    bar_body_list : list[Mobject] = []
    table_of_key_label_within_bar_bodies : list[list[KeyLabel]] = [[] for _ in range(bar_count)]
    keys_list : list[dict] = []
    background_bar_list : list[VGroup] = []


    def __init__(self):
        super().__init__()
        Screen.keys_list = self.get_key_ranking_data()
        Screen.background_bar_list = self.init_background_bar_list()

    @staticmethod
    def init_bar(title : str, bar_head_color : str) -> VGroup:
        bar_head = Square(fill_opacity=1, fill_color=bar_head_color, color=BLACK, side_length=Screen.square_side_length)
        bar_body = Rectangle(fill_opacity=1, fill_color=Screen.bar_body_color, color=BLACK, height=Screen.base_height, width=Screen.background_width - Screen.square_side_length)
        bar_head.next_to(bar_body, LEFT, buff=0)
        bar_title = Text(color=BLACK, text=title, font_size=32)
        bar_title.move_to(bar_head.get_center())
        Screen.bar_body_list.append(bar_body)
        return VGroup(bar_head, bar_body, bar_title)


    def init_background_bar_list(self) -> list[VGroup]:
        bar_list : list[VGroup] = []
        for nth, bar_head_message in enumerate(Screen.bar_head_message_list):
            bar : VGroup = Screen.init_bar(title=bar_head_message[0], bar_head_color=bar_head_message[1])
            if nth == 0:
                bar.to_edge(UL, buff=0)
            elif nth < self.bar_count:
                bar.next_to(bar_list[nth - 1], DOWN, buff=0)
            else:
                break
            bar_list.append(bar)

        return bar_list

    @staticmethod
    def get_key_ranking_data() -> list[dict]:
        _keys_list : list = []
        with open(file=Screen.ranking_file_path, mode="r", encoding="UTF-8") as fp:
            data = json.load(fp)

        for level in "01234":
            for _key in data[level]["keys"]:
                _keys_list.append(_key)

        return _keys_list



    def construct(self):
        self.add(NumberPlane())
        self.add(*Screen.background_bar_list)
        self.wait(duration=2)

        random.shuffle(Screen.keys_list)

        for i in range(30):
            key_label = KeyLabel(Screen.keys_list[i])
            self.play(Create(key_label))
            self.wait()
            self.play(key_label.animate_of_move_to_screen_bar())

        self.wait()


if __name__ == '__main__':
    command : list[str]= ["manim", str(__file__), "Screen", "-pql"]
    print(" ".join(command))
    subprocess.run(command, capture_output=True, text=True)
