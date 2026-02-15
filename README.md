# Obsidian Knowledge Adapter

> 一个为 AI Agent 设计的 Obsidian 知识管理 Skill，集成 Obsidian CLI 和自定义 Agent（概念解剖 / 解法结晶 / 范式提炼），构建 **检索 → 加工 → 结晶** 的知识工作流。

## ✨ 特性

- 🧠 **三大内置 Agent（Persona）**
  - **Concept Anatomist（概念解剖师）** — 通过 8 个维度解构任何概念，最终压缩为「顿悟」
  - **Solution Crystallizer（解法结晶师）** — 将调试过程提炼为可复用的解法模式
  - **Pattern Distiller（范式提炼师）** — 从任何优秀作品中萃取核心 DNA（结构、原则、组合规则），适用于代码、架构、设计、工作流等领域
- 🔗 **Obsidian 深度集成** — Wiki-links、Frontmatter、图谱感知
- 🛠 **CLI 封装脚本** — 一行命令完成读取、反向链接、搜索、创建笔记等操作
- 📦 **Agent 安装器** — 一键将内置 Agent 安装到你的 Vault

## 📂 目录结构

```
obsidian-knowledge-adapter/
├── SKILL.md              # 核心指令文件（Agent 读取入口）
├── agents/               # 内置 Agent 定义
│   ├── lijigang_concept.md     # 概念解剖师
│   ├── solution_crystallizer.md # 解法结晶师
│   └── pattern_distiller.md    # 范式提炼师
├── scripts/
│   ├── obsidian_cli.py         # Obsidian CLI 封装
│   ├── list_agents.py          # Agent 发现工具
│   └── install_agent.py        # Agent 安装工具
└── resources/            # 扩展资源（预留）
```

## 🚀 快速开始

### 安装

将本仓库克隆到你的 AI Agent 的 skills 目录下：

```bash
# 以 Antigravity 为例
git clone https://github.com/SynthThoughts/obsidian-knowledge-adapter.git \
  ~/.gemini/antigravity/skills/obsidian-knowledge-adapter

# 或以 Claude Code 为例
git clone https://github.com/SynthThoughts/obsidian-knowledge-adapter.git \
  ~/.claude/skills/obsidian-knowledge-adapter
```

### 使用

1. **列出可用 Agent**
   ```bash
   python3 scripts/install_agent.py --list
   ```

2. **安装 Agent 到 Vault**
   ```bash
   cd /path/to/your/obsidian-vault
   python3 /path/to/skills/obsidian-knowledge-adapter/scripts/install_agent.py lijigang_concept
   ```
   Agent 将被复制到 `.antigravity/agents/` 目录。

3. **使用 CLI 工具**
   ```bash
   # 在你的 Vault 根目录下运行
   python3 scripts/obsidian_cli.py read "folder/note.md"
   python3 scripts/obsidian_cli.py backlinks "folder/note.md"
   python3 scripts/obsidian_cli.py search "query"
   python3 scripts/obsidian_cli.py orphans
   python3 scripts/obsidian_cli.py tags
   ```

## 🎯 设计理念

本 Skill 的核心理念是 **网络重于节点（Network Over Node）**：

> 知识从不孤立存在。每一条新笔记都必须连接到已有节点（反向链接），并留下供未来扩展的钩子。没有链接的笔记是死去的笔记。

通过三种内置 Agent，覆盖知识管理的三大核心场景：

| Agent | 场景 | 输入 | 输出 |
|-------|------|------|------|
| 概念解剖师 | 理解新概念 | 任意概念/术语 | 八维分析 + 顿悟压缩 |
| 解法结晶师 | 事后复盘 | 调试过程/错误日志 | 根因分析 + 通用原则 |
| 范式提炼师 | 提取成功范式 | 代码/架构/设计/工作流 | 核心 DNA + 组合规则 |

## 🙏 致谢

本项目的设计思路受到以下优秀项目的启发，在此表示衷心感谢：

- **[Claudian](https://github.com/YishenTu/claudian)** by [@YishenTu](https://github.com/YishenTu) — 提供了 Obsidian 知识管理与 AI Agent 集成的核心思路和最佳实践
- **[ljg-explain-concept](https://github.com/lijigang/ljg-explain-concept)** by [@lijigang](https://github.com/lijigang) — 八维概念解剖的原始灵感来源，「概念解剖师」Agent 直接受益于此项目

## 📄 License

[MIT](LICENSE)
