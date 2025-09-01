import json
import os.path
import random
import re
import subprocess
from manim import *


def deal_file_name(file_string : str) -> str:
        file_string = file_string.strip(" ,.。, ")
        file_string = file_string.replace("+", "加")
        file_string = file_string.replace("-", "减")
        file_string = file_string.replace("*", "星号")
        file_string = file_string.replace(".", "点")
        file_string = file_string.replace("/", "斜杠")

        file_string = file_string.replace("`", "")
        file_string = file_string.replace(":", "")
        return file_string


class KeyLabel(VGroup):
    buff_of_key_with_other_key : float = 0.2
    def __init__(self, key_message : dict):
        self.level_value : int = key_message["level_value"]
        self.name : str = key_message["abbreviation"]
        self.label_height = Screen.base_height * 0.43
        self.label_width = len(self.name) / 6 + 0.5
        self.label_width = max(self.label_width, self.label_height)
        super().__init__(*KeyLabel.init_key_label(self.name, self.label_height, self.label_width))

    @staticmethod
    def init_key_label(content : str, height : float, width : float) -> tuple[Mobject, Mobject]:
        _key_label = RoundedRectangle(corner_radius=0.07, fill_opacity=1, fill_color=DARKER_GRAY, color=WHITE, height=height, width=width)
        key_label_content = Text(text=content, color=WHITE, font_size=20)
        VGroup(_key_label, key_label_content).scale(scale_factor=8 / 5)
        return _key_label, key_label_content

    def animate_of_move_to_bar(self):
        Bar.find_by_level_value(self.level_value)
        animate = Bar.find_by_level_value(self.level_value).get_animate_of_key_label_move_to_remaining_space(self)
        return animate


class Bar(VGroup):
    def __init__(self,  title : str, bar_head_color : str, level_value : int):
        self.bar_head: Square
        self.bar_body: Rectangle
        self.bar_title: Text
        self.level_value : int = level_value
        self.title_string : str = title
        self.bar_head , self.bar_body, self.bar_title = Bar.init_bar(title=title, bar_head_color=bar_head_color)
        self.bar_body_width : float = Screen.bar_body_width
        self.bar_height : float = Screen.bar_body_height
        self.stored_key_list : list[KeyLabel] = []
        self.remaining_space_above : float = self.bar_body_width
        self.remaining_space_below : float = self.bar_body_width
        super().__init__(self.bar_head, self.bar_body, self.bar_title)


    def get_animate_of_key_label_move_to_remaining_space(self, key_label : KeyLabel):
        if self.remaining_space_above >= self.remaining_space_below:
            left_point_of_remaining_space = self.get_right() + LEFT * self.remaining_space_above + UP * self.bar_height / 4
            self.remaining_space_above -= key_label.label_width + KeyLabel.buff_of_key_with_other_key
        else :
            left_point_of_remaining_space = self.get_right() + LEFT * self.remaining_space_below + DOWN * self.bar_height / 4
            self.remaining_space_below -= key_label.label_width + KeyLabel.buff_of_key_with_other_key

        animate = key_label.animate.scale(scale_factor=5 / 8).next_to(
            mobject_or_point=left_point_of_remaining_space,
            direction=RIGHT, buff=KeyLabel.buff_of_key_with_other_key
        )
        return animate

    @staticmethod
    def find_by_level_value(level_value) -> "Bar| None":
        for bar in Screen.background_bar_list:
            if bar.level_value == level_value:
                return bar
        return None

    @staticmethod
    def init_bar(title : str, bar_head_color : str) -> tuple[Square, Rectangle, Text]:
        bar_head = Square(fill_opacity=1, fill_color=bar_head_color, color=BLACK, side_length=Screen.square_side_length)
        bar_body = Rectangle(fill_opacity=1, fill_color=Screen.bar_body_color, color=BLACK, height=Screen.bar_body_height, width=Screen.bar_body_width)
        bar_head.next_to(bar_body, LEFT, buff=0)
        bar_title = Text(color=BLACK, text=title, font_size=32)
        bar_title.move_to(bar_head.get_center())
        return bar_head, bar_body, bar_title



class SubtitleGenerator:
    last_previous_subtitle : Text | None
    color = None
    font_size = None
    base_position = None
    spacing = None
    animation_duration = None
    font = None
    font_weight = None
    stroke_color = None
    def __init__(self, _color=BLACK, font="Arial", font_size=30, font_weight="BOLD", base_position=(0, -3, 0), spacing=0.5, animation_duration=1.0, stroke_color = WHITE):
        SubtitleGenerator.color = _color
        SubtitleGenerator.font_size = font_size
        SubtitleGenerator.base_position = base_position
        SubtitleGenerator.spacing = spacing
        SubtitleGenerator.animation_duration = animation_duration
        SubtitleGenerator.font = font
        SubtitleGenerator.font_weight = font_weight
        SubtitleGenerator.stroke_color = stroke_color

    @staticmethod
    def generate(scene : Scene, content : str, create_time=1.0, point_or_mobject=None):
        if point_or_mobject is None:
            point_or_mobject = SubtitleGenerator.base_position
        SubtitleGenerator.last_previous_subtitle = Text(
            text=content, color=SubtitleGenerator.color,
            font=SubtitleGenerator.font,
            font_size=SubtitleGenerator.font_size,
            weight=SubtitleGenerator.font_weight
        )
        subtitle_video_file = f"/home/mango/IdeaProjects/Keyboard-Special-Key-Rankings/resource/subtitle_video/{deal_file_name(content)}.wav"
        if os.path.exists(subtitle_video_file) and os.path.isfile(subtitle_video_file):
            scene.add_sound(subtitle_video_file)
            print(f"add subtitle video `{subtitle_video_file}`")
        else:
            print(f"subtitle video file `{subtitle_video_file}` not found")
        scene.play(
            Create(
                SubtitleGenerator.last_previous_subtitle.move_to(
                    point_or_mobject=point_or_mobject
                ).set_stroke(
                    color=SubtitleGenerator.stroke_color,
                    width=1
                ),
                create_time=create_time
            )
        )



    @staticmethod
    def animate_display(scene : Scene, content : str):
        line_length = len(content)
        create_time = line_length / 6
        SubtitleGenerator.generate(scene=scene, content=content, create_time=create_time)
        scene.wait(duration=create_time)

    @staticmethod
    def animate_disappear(scene : Scene, fade_out_time = 1.0):
        scene.play(FadeOut(SubtitleGenerator.last_previous_subtitle, run_time=fade_out_time))
        SubtitleGenerator.last_previous_subtitle = None

    @staticmethod
    def animate_display_and_disappear(scene : Scene, content : str, fade_out_time = 1.0):
        SubtitleGenerator.animate_disappear(scene=scene, fade_out_time=fade_out_time)
        SubtitleGenerator.animate_display(scene=scene, content=content)


class Screen(Scene) :
    ranking_file_path : str = "/home/mango/IdeaProjects/Keyboard-Special-Key-Rankings/src/ranking.json"
    background_height : float = 8
    background_width : float = 256 / 9
    bar_count : int = 5
    base_height : float = background_height / bar_count
    square_side_length : float = base_height

    bar_head_message_list : list[tuple[str, str]] = [("夯", "#FB0601"), ("顶级", "#FFC601"), ("人上人", "#FCFA11"), ("NPC", "#FFEFCE"), ("拉", "#FFFFFF")]
    bar_body_color : str = "#6b6160"
    bar_body_width : float = background_width - square_side_length
    bar_body_height : float = square_side_length

    keys_message_list : list[dict] = []
    background_bar_list : list[Bar] = []


    def __init__(self):
        super().__init__()
        Screen.keys_message_list = self.get_key_ranking_data()
        Screen.background_bar_list = self.init_background_bar_list()


    def init_background_bar_list(self) -> list[Bar]:
        bar_list : list[Bar] = []
        for nth, bar_head_message in enumerate(Screen.bar_head_message_list):
            bar : Bar = Bar(title=bar_head_message[0], bar_head_color=bar_head_message[1], level_value=nth)
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

    @staticmethod
    def animate_of_thanks_for_watching():
        circle = Circle(color=WHITE, fill_color=BLACK, fill_opacity=1)
        text = Text("Thanks for watching", color=WHITE, font="Arial", slant=ITALIC)
        text.scale(circle.radius / text.width).move_to(circle.get_center())
        group = VGroup(circle, text)
        scale_factor = config.frame_height / circle.height * 3
        return group.animate.scale(scale_factor)


    def construct(self):
        self.play(Create(VGroup(*Screen.background_bar_list), run_time=1))
        self.wait(3)

        SubtitleGenerator()
        SubtitleGenerator.animate_display(scene=self, content="键盘特殊键从夯到拉")

        self.wait(duration=2)
        random.seed = 42
        random.shuffle(Screen.keys_message_list)
        # playing_count = min(5, len(Screen.keys_message_list)) # 测试用
        playing_count = len(Screen.keys_message_list)

        for i in range(playing_count):
            key_message = Screen.keys_message_list[i]
            content : str =key_message["description"]
            content.replace("\n", "")
            key_label = KeyLabel(key_message=key_message)
            key_name = key_message["name"]
            SubtitleGenerator.animate_display_and_disappear(scene=self, content=f"下一个是 `{key_name}`")

            self.play(Create(key_label))
            SubtitleGenerator.animate_disappear(scene=self, fade_out_time=0.1)

            line_list : list[str] = content.split("\\n")
            for line in line_list:

                SubtitleGenerator.animate_display_and_disappear(scene=self, content=line, fade_out_time=0.1)
                self.wait(0.5)

            level_name = key_message["level_name"]
            SubtitleGenerator.animate_display_and_disappear(scene=self, content=f"这里我给到 `{level_name}`", fade_out_time=1)
            self.wait(1)
            self.play(key_label.animate_of_move_to_bar())

        SubtitleGenerator.animate_disappear(scene=self, fade_out_time=0.1)
        self.play(Screen.animate_of_thanks_for_watching(), run_time=3, rate_func=linear)
        self.wait(5)


if __name__ == '__main__':
    manim_path = "/home/mango/anaconda3/envs/Keyboard-Special-Key-Rankings/bin/manim"
    command : list[str]= [manim_path, str(__file__), "Screen", "-p"] # 测试用 "-pql"
    print(" ".join(command))
    subprocess.run(command, capture_output=True, text=True)
