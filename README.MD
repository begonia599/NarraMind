<div align="center">
  <img src="https://placehold.co/400x150?text=NarraMind" alt="NarraMind Logo" width="400"/>
  
  # NarraMind
  
  *基于知识图谱的智能角色扮演与记忆管理系统*
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![MCP Protocol](https://img.shields.io/badge/MCP-compatible-green.svg)](https://github.com/microsoft/modelcontrolprotocol)
  [![Last Updated](https://img.shields.io/badge/last%20updated-April%202025-orange.svg)](https://github.com/yourusername/narramind)
  
  <p align="center">
    <a href="#快速开始">快速开始</a> •
    <a href="#核心功能">核心功能</a> •
    <a href="#系统架构">系统架构</a> •
    <a href="#数据模型">数据模型</a> •
    <a href="#工具集">工具集</a> •
    <a href="#贡献指南">贡献指南</a>
  </p>
</div>

---

## 📌 项目概述

NarraMind 是一个先进的角色扮演与记忆管理系统，专为创建持久、连贯且智能的虚拟角色体验而设计。本项目核心由两大技术支撑：

1. **Model-Controller Protocol (MCP)框架**：确保大型语言模型(LLM)能以结构化、可控的方式与外部系统交互
2. **知识图谱数据库**：采用MySQL构建的复杂关系型数据库，存储角色、地点、事件和关系等核心元素

NarraMind通过精心设计的MCP工具(Tools)和资源(Resources)，使AI能够自主地读取、更新和利用历史记忆，从而实现更加真实、连贯的角色扮演体验。无论是游戏开发、交互式故事创作还是AI助手培训，NarraMind都提供了强大的记忆管理基础架构。

---

## ⚡ 快速开始

### 环境要求

- Python 3.10+
- MySQL 8.0+
- 支持 MCP 协议的 LLM API（如 Azure OpenAI 或兼容接口）

### 安装步骤

1. **克隆仓库：**
   ```bash
   git clone https://github.com/yourusername/narramind.git
   cd narramind
   ```

2. **创建虚拟环境：**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖：**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置数据库连接：**
   - 编辑 `config/database.py` 文件
   - 设置您的 MySQL 数据库连接参数

5. **运行 MCP 服务器：**
   ```bash
   python main.py
   ```
   *首次运行时，程序会自动初始化数据库和表结构*

### 命令行参数

```bash
python main.py --host localhost --port 8080 --skip-db-init
```

- `--host`：指定服务器主机地址（默认：localhost）
- `--port`：指定服务器端口（默认：8080）
- `--skip-db-init`：跳过数据库初始化检查

### 快速演示

服务器启动后，您可以使用支持 MCP 协议的客户端连接它，例如：

```python
from mcp_client import MCPClient

client = MCPClient("http://localhost:8080")
response = client.chat("创建一个名为'艾莉丝'的角色，她是一位年轻的冒险家。")
print(response)

# 检索角色信息
response = client.chat("告诉我关于艾莉丝的信息")
print(response)
```

---

## 🚀 快速开始

### 环境要求
- Python 3.10+
- MySQL 8.0+
- 兼容MCP协议的LLM服务
- uv
-

### 安装
1. 克隆仓库
```bash
git clone https://github.com/yourusername/narramind.git
cd narramind
```

2. 安装依赖
```bash
uv init
uv add -r requirements.txt
```

### 配置数据库
1. 在MySQL中创建数据库
```sql
CREATE DATABASE narramind CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 更新配置文件
编辑 `config/database.py` 文件，填入您的数据库连接信息：
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'narramind'
}
```

### 启动服务
进入您的mcp客户端，在客户端配置输入以下信息：
```bash
{
  "mcpServer": {
    "NarraMind":{
      "command":"uv",
      "args": [
        "--directory",
        "narramind/src/mcp",
        "run",
        "main.py"
      ]
    }
  }
}

```

---

## ✨ 核心功能

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://placehold.co/60x60?text=👤" width="60"/><br />
        <b>角色管理</b><br />
        创建、查询和更新虚拟角色的各种属性
      </td>
      <td align="center">
        <img src="https://placehold.co/60x60?text=🌍" width="60"/><br />
        <b>世界构建</b><br />
        设计互联的地点和场景
      </td>
      <td align="center">
        <img src="https://placehold.co/60x60?text=🔗" width="60"/><br />
        <b>关系网络</b><br />
        建立角色之间的复杂社交关系
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="https://placehold.co/60x60?text=📜" width="60"/><br />
        <b>事件记忆</b><br />
        记录和检索游戏中发生的关键事件
      </td>
      <td align="center">
        <img src="https://placehold.co/60x60?text=🔄" width="60"/><br />
        <b>MCP接口</b><br />
        结构化AI与数据库的交互
      </td>
      <td align="center">
        <img src="https://placehold.co/60x60?text=📊" width="60"/><br />
        <b>知识图谱</b><br />
        构建完整的世界状态数据库
      </td>
    </tr>
  </table>
</div>

---

## 🚀 核心功能

### 1. 角色记忆管理

NarraMind 能够创建、存储和检索角色的详细信息，包括：

- **基本属性**：姓名、年龄、性别、外貌等基本信息
- **性格特征**：个性、价值观、心理特点等深层次描述
- **技能与能力**：量化的技能评级与专长描述
- **生平历史**：背景故事、关键生活事件与经历

系统会自动整合这些信息，使 LLM 能够具备持久化记忆，在多轮对话中保持角色的一致性。

### 2. 关系网络追踪

- **角色间关系**：记录并管理角色之间的复杂社交网络
- **关系属性**：包括亲密度、信任度、敌对度等量化指标
- **关系历史**：记录关系发展的关键事件与转折点
- **动态更新**：基于交互自动调整关系参数

### 3. 事件与记忆检索

- **事件记录**：自动或手动记录叙事中的重要事件
- **语义检索**：根据相关性智能检索过去事件与记忆
- **时间线管理**：构建完整的叙事时间线与因果链
- **记忆衰减**：模拟真实的记忆特性，远期记忆可能变得模糊

### 4. 环境与地点建模

- **地点定义**：创建并管理叙事世界中的各种地点
- **环境属性**：记录地点的物理特性、文化特点等信息
- **地理关系**：建立地点间的空间关联与导航逻辑
- **氛围设定**：定义地点的情绪氛围与感官体验

### 5. MCP 工具集成

- **标准化接口**：遵循 MCP 协议设计的工具函数
- **双向交互**：LLM 可主动查询和修改知识库
- **智能检索**：基于上下文的相关信息智能推荐
- **资源管理**：结构化资源定义与访问控制

---

## 💡 核心功能

### 角色系统
- 创建、编辑和管理虚拟角色
- 定义角色基本属性（性格、背景、目标等）
- 追踪角色状态和发展轨迹

### 记忆管理
- 长短期记忆分离存储
- 智能记忆检索与关联
- 根据上下文动态更新记忆重要性

### 关系网络
- 角色间关系建模与更新
- 关系强度动态调整
- 社交网络可视化

### 事件追踪
- 记录角色间互动和重要事件
- 事件时间线管理
- 事件影响分析

### 位置与环境
- 地点管理和场景描述
- 角色位置追踪
- 环境对角色行为的影响分析

### 技能系统
- 角色能力定义与升级
- 技能检测与应用
- 基于技能的行动结果推断

---

## 🏛️ 系统架构

<div align="center">
  <img src="https://placehold.co/800x400?text=NarraMind+Architecture+Diagram" alt="NarraMind 架构图" width="800"/>
  <!-- 这里可以替换为真实的架构图 -->
</div>

NarraMind 系统由三个主要组件组成：

1. **大型语言模型 (LLM)**: 作为智能代理的核心，负责理解用户输入和生成角色扮演内容
2. **MCP 服务器**: 处理LLM与外部工具和服务的交互
3. **知识图谱数据库**: 存储结构化的游戏世界信息

---

## 💾 数据模型

NarraMind 使用 MySQL 数据库存储以下关键实体：

### 核心实体

<div align="center">
  <table>
    <tr>
      <th>实体</th>
      <th>描述</th>
      <th>主要字段</th>
    </tr>
    <tr>
      <td><b>角色 (characters)</b></td>
      <td>游戏中的所有角色实体</td>
      <td>id, 名称, 年龄, 性别, 职业, 外观, 性格</td>
    </tr>
    <tr>
      <td><b>地点 (locations)</b></td>
      <td>游戏世界中的场景和地点</td>
      <td>id, 名称, 描述, 类型, 连接点</td>
    </tr>
    <tr>
      <td><b>关系 (relationships)</b></td>
      <td>角色之间的社交关系</td>
      <td>角色1, 角色2, 关系类型, 描述</td>
    </tr>
    <tr>
      <td><b>事件 (events)</b></td>
      <td>游戏中发生的事件记录</td>
      <td>id, 时间戳, 地点, 描述, 详情</td>
    </tr>
  </table>
</div>

详细数据库结构:

* **`characters` 表:** 存储角色基本信息。
    * `character_id` (VARCHAR, PRIMARY KEY)
    * `name` (VARCHAR)
    * `played_by` (ENUM: 'player', 'ai')
    * `age` (INT)
    * `gender` (VARCHAR)
    * `occupation` (VARCHAR)
    * `appearance` (TEXT)
    * `voice_tone` (VARCHAR)
    * `voice_style` (VARCHAR)
    * `mannerisms` (TEXT)
    * `current_goal` (TEXT)
    * `backstory` (TEXT)
    * `notes` (TEXT)

* **`locations` 表:** 存储地点信息。
    * `location_id` (VARCHAR, PRIMARY KEY)
    * `name` (VARCHAR)
    * `description` (TEXT)
    * `type` (VARCHAR)
    * `connections` (TEXT)
    * `inhabitants` (TEXT)
    * `items` (TEXT)
    * `notes` (TEXT)

* **`relationships` 表:** 存储角色之间的关系。
    * `relationship_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `character_id_1` (VARCHAR, FOREIGN KEY to `characters`)
    * `character_id_2` (VARCHAR, FOREIGN KEY to `characters`)
    * `relation_type` (VARCHAR)
    * `description` (TEXT)

* **`character_location_state` 表:** 存储角色对地点的认知状态。
    * `relation_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `character_id` (VARCHAR, FOREIGN KEY to `characters`)
    * `location_id` (VARCHAR, FOREIGN KEY to `locations`)
    * `state` (ENUM: '未知', '已知', '去过', '当前')

* **`events` 表:** 存储游戏中发生的事件。
    * `event_id` (VARCHAR, PRIMARY KEY)
    * `timestamp` (DATETIME)
    * `location_id` (VARCHAR, FOREIGN KEY to `locations`)
    * `description` (TEXT)
    * `details` (JSON)

* **`items` 表:** 存储物品信息。
    * `item_id` (VARCHAR, PRIMARY KEY)
    * `name` (VARCHAR)
    * `description` (TEXT)
    * `type` (VARCHAR)
    * `properties` (JSON)
    * `rarity` (VARCHAR)
    * `value` (INT)

* **`skills` 表:** 存储技能信息。
    * `skill_id` (VARCHAR, PRIMARY KEY)
    * `name` (VARCHAR)
    * `description` (TEXT)

* **`personalities` 表:** 存储性格特征信息。
    * `personality_id` (VARCHAR, PRIMARY KEY)
    * `trait` (VARCHAR, UNIQUE)
    * `description` (TEXT)

* **`character_skills` 表:** 关联角色和技能。
    * `relation_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `character_id` (VARCHAR, FOREIGN KEY to `characters`)
    * `skill_id` (VARCHAR, FOREIGN KEY to `skills`)
    * `level` (INT)

* **`character_personalities` 表:** 关联角色和性格特征。
    * `relation_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `character_id` (VARCHAR, FOREIGN KEY to `characters`)
    * `personality_id` (VARCHAR, FOREIGN KEY to `personalities`)

* **`event_characters` 表:** 关联事件和参与角色。
    * `relation_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `event_id` (VARCHAR, FOREIGN KEY to `events`)
    * `character_id` (VARCHAR, FOREIGN KEY to `characters`)
    * `role_in_event` (VARCHAR)

---

## 🛠️ 工具集

NarraMind 提供了丰富的MCP工具，使AI能够与知识图谱进行交互：

<div class="tools-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
  <div class="tool-card">
    <h3>🧩 角色工具</h3>
    <ul>
      <li><code>add_character</code>: 添加新角色</li>
      <li><code>get_character_profile</code>: 获取角色信息</li>
      <li><code>update_character_attribute</code>: 更新角色属性</li>
    </ul>
  </div>
  
  <div class="tool-card">
    <h3>🏙️ 地点工具</h3>
    <ul>
      <li><code>add_location</code>: 添加新地点</li>
      <li><code>get_location_info</code>: 获取地点信息</li>
      <li><code>update_location_attribute</code>: 更新地点属性</li>
    </ul>
  </div>
  
  <div class="tool-card">
    <h3>🤝 关系工具</h3>
    <ul>
      <li><code>set_relationship</code>: 设置角色关系</li>
      <li><code>get_character_relationships</code>: 获取角色关系网络</li>
    </ul>
  </div>
  
  <div class="tool-card">
    <h3>📝 事件工具</h3>
    <ul>
      <li><code>log_event</code>: 记录新事件</li>
      <li><code>get_events_involving_character</code>: 检索角色相关事件</li>
    </ul>
  </div>
</div>

---

## 📊 使用示例

### 创建角色并设置关系

```python
# 创建主角
add_character({
    "character_id": "mc01",
    "name": "艾莉亚",
    "age": 25,
    "gender": "女",
    "occupation": "探险家",
    "backstory": "来自遥远的山村，寻找失落的古代神器..."
})

# 创建NPC
add_character({
    "character_id": "npc01",
    "name": "莱昂",
    "age": 40,
    "gender": "男",
    "occupation": "商人"
})

# 设置角色关系
set_relationship("mc01", "npc01", "熟人", "艾莉亚经常向莱昂购买探险用品")
```

---

## 🧩 模块结构

```
narramind/
│
├── config/               # 配置文件
│   └── database.py       # 数据库配置
│
├── src/
│   ├── mcp/              # MCP协议实现
│   │   ├── server.py     # MCP服务器
│   │   └── tools/        # MCP工具函数
│   │
│   ├── models/           # 数据模型
│   │   ├── character.py  # 角色模型
│   │   ├── event.py      # 事件模型
│   │   ├── location.py   # 位置模型
│   │   ├── relationship.py # 关系模型
│   │   └── skill.py      # 技能模型
│   │
│   ├── db/               # 数据库操作
│   │   └── connection.py # 数据库连接管理
│   │
│   └── utils/            # 工具函数
│       └── init_database.py # 数据库初始化
│
├── main.py               # 主程序入口
└── requirements.txt      # 项目依赖
```

---

## 📄 许可证

本项目使用 [MIT License](LICENSE) 开源。

---

<div align="center">
  <p>Made with ❤️ by Your Team</p>
  <p>
    <a href="https://github.com/yourusername/narramind">GitHub</a> •
    <a href="https://your-documentation-url.com">文档</a>
  </p>
</div>
