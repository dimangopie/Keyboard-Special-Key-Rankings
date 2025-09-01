# 键盘特殊键从夯到拉 / The Ultimate Keyboard Special Key Survival Pyramid 🎯

## 简介 / Introduction 📖
这是一个关于键盘特殊键的排名项目，
旨在帮助用户了解和优化键盘特殊键的使用效率。
项目包含了键盘上大部分的特殊键，
并根据使用频率和重要性将特殊键分为五个等级：
拉、NPC、人上人、顶级、夯。
<br>
查看排名 👀:
- Bilibili[键盘特殊键从夯到拉] (https://www.bilibili.com/video/BV1i2aEz1EmQ/?share_source=copy_web&vd_source=9cb578356de45dce5e60e99994f6f477)
- 也可以选择编译`manim`动画进行观看
- 也可以选择查看`special_key_reference_table.txt`文件或者`ranking.json`文件。
<br>
你是否在使用最高效的特殊键？欢迎参与讨论并贡献你的见解！🎉

## 特殊键等级说明 / Ranking System
从高到低分为以下五个等级：
- **夯 (Ultimate)**：改变规则的存在。 💪
- **顶级 (Top-tier)**：一天不用受不了。 🥰
- **人上人 (Advanced)**：常用键。 🌟
- **NPC (Non-Player Character)**：纯人机才会用 (AI都嫌弃)。 🤖
- **拉 (Lag)**：膈应人的装饰品。 🤮

## 使用方法 / How to Use 🛠️
1. 克隆项目到本地： 📁
   ```bash
   git clone https://github.com/dimangopie/Keyboard-Special-Key-Rankings
   ```
2. 查看当前排名： 📄
   ```bash
   cat src/ranking.json
   ```
3. `PYTHON` 编译`manim`动画 🐍
    ```bash
    python3 src/get_json_of_ranking.py
    python3 src/make_subtitle.py # 可不运行 make_subtitle.py
    python3 src/main.py
    ```
4. 提出你的修改建议： ✏️
   ```bash
   git pull-request
   ```

## 资源文件 / Resource Files 📂
### `special_key_reference_table.txt`
包含键盘特殊键的名称、键值（十进制）、扫描码（十六进制）和等级信息。此文件用于生成 `ranking.json` 文件。📄

### `reference_table_for_key_value.txt`
包含键盘键的名称和对应的键值（十进制）。此文件用于参考。📄

### `reference_table_for_scan_code.txt`
包含键盘键的名称和对应的扫描码（十六进制）。此文件用于参考。📄

## `main.py` 文档说明 📝
`main.py` 是一个 Python 脚本，使用`manim`库, 用于从 `ranking.json` 文件读取特殊键信息，和, 并生成视频文件。

使用由`bilibili`开源的[index-tts](https://github.com/index-tts/index-tts)工业级可控高效零样本文本转语音系统,
用于配合 `main.py` 的字幕生成器，生成音频文件，并生成在 `resource/subtitle_video` 文件下。

## `make_subtitle.py` 文档说明 📝
`make_subtitle.py` 是一个 Python 脚本, 生成字幕表


## `get_json_of_ranking.py` 文档说明 📝
`get_json_of_ranking.py` 是一个 Python 脚本，用于从 `special_key_reference_table.txt` 文件读取特殊键信息，并生成 `ranking.json` 文件。以下是脚本的主要功能：
1. 读取 `special_key_reference_table.txt` 文件中的每一行数据。
2. 解析每一行的数据，提取键名、键值、扫描码和等级信息。
3. 根据等级信息将特殊键信息添加到对应的等级列表中。
4. 将生成的排名信息保存到 `ranking.json` 文件中。

运行`get_json_of_ranking.py`脚本：
```bash
python get_json_of_ranking.py
```

## `ranking.json`文档说明 📄
- 使用 `UTF-8` 编码。
- 文件结构示例：
  ```json
  {
      "0": {
          "level_value": 0,
          "level_name": "夯",
          "keys": [
              {
                "level_value": 0,
                "level_name": "夯",
                "name": "Space",
                "key_value": 32,
                "scan_code": 14592,
                "description": "不特殊的特殊键, 最实在的一集"
              }
          ]
      }
  }
  ```

## 特殊键的跨平台体验 🌐
特殊键的行为会因操作系统和设备而异。请在不同平台上测试特殊键的功能，以确保其符合预期。
- **Windows 🪟**：某些特殊键可能具有特定的功能。
- **Linux 🐧**：某些键的行为可能需要额外的配置。
- **MacOS 🍎**：在MacOS系统中，部分键盘按键的功能与Windows系统有所不同，具体映射关系如下：
  - Windows系统中的Ctrl键，在MacOS中对应为Command键（⌘）。
  - Windows系统中的Win键（即带有Windows图标 的按键），在MacOS中对应为Super键（也称作“指挥键”）。 

## 贡献者指南 / Contribution Guidelines 🤝
- **提出特殊键的描述、等级修改或新增建议**：你可以通过提交 Pull Request 来添加或修改特殊键的描述、等级等信息。
- **遵循JSON文件的结构和格式**：确保你的修改符合 `ranking.json` 的结构。
- **提交Pull Request时请附上相关解释**：在提交PR时，请详细说明你的修改内容和理由。

## 致谢 / Acknowledgements 🙏
感谢所有为本项目做出贡献的开发者和键盘爱好者。特别感谢以下人员：
- [dimangopie](https://github.com/dimangopie)：项目发起人和主要维护者。
- [其他贡献者](https://github.com/dimangopie/Keyboard-Special-Key-Rankings/graphs/contributors)：为项目提供了宝贵的建议和代码。

## 许可证 / License📜
本项目采用 [Apache License 2.0](LICENSE)。详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式 / Contact 📮
如有任何问题或建议，请通过以下方式联系我们：
- 项目主页：[https://github.com/dimangopie/Keyboard-Special-Key-Rankings](https://github.com/dimangopie/Keyboard-Special-Key-Rankings)
- 邮箱：[1106211173@qq.com](mailto:1106211173@qq.com)
