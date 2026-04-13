# 中国法律研究 Skill 构建计划

**日期**：2026-04-12

## Context

用户已有一个可工作的 Command 版本（`test_command/.claude/commands/法律研究.md`），经过两次真实法律研究测试验证可用。现在需要构建正式 Skill，放在 `test_skill/.claude/skills/` 下，使 Claude 能**自动识别触发**（而非用户手动输入 `/法律研究`）。

### 现状

- `test_command/.claude/commands/法律研究.md` — 已验证的 Command 版本（244行）
- `tavily_search.py` — Tavily 检索封装（已完成）
- `yuandian_api.py` — 元典 API 封装（已完成）
- `config.py` — API 密钥（已完成）
- `test_skill/` — 已创建但为空

### Command vs Skill 的区别

| 维度 | Command | Skill |
|------|---------|-------|
| 触发方式 | 用户手动 `/法律研究 问题` | Claude 根据 description 自动识别 |
| 文件位置 | `.claude/commands/法律研究.md` | `.claude/skills/法律研究/SKILL.md` |
| 参数传递 | `$ARGUMENTS` | 无 `$ARGUMENTS`，从对话上下文获取 |

---

## 目标目录结构

```
test_skill/
└── .claude/
    └── skills/
        └── 法律研究/
            ├── SKILL.md              ← 主文件（从 Command 转换）
            ├── scripts/
            │   ├── yuandian_api.py   ← 元典 API 封装（从项目根目录复制）
            │   ├── tavily_search.py  ← Tavily 检索封装（从项目根目录复制）
            │   └── config.py         ← API 密钥配置（从项目根目录复制）
            └── references/
                └── 引用格式要求.md    ← 引注规范参考
```

**scripts/ 目录说明**：将三个 Python 脚本复制到 Skill 内部，使 Skill 自包含。SKILL.md 中的 API 调用示例路径指向 `scripts/` 目录下的脚本。

---

## 实施步骤

### Step 1：创建目录结构

```bash
mkdir -p test_skill/.claude/skills/法律研究/scripts
mkdir -p test_skill/.claude/skills/法律研究/references
```

### Step 2：复制脚本到 scripts/

```bash
cp yuandian_api.py test_skill/.claude/skills/法律研究/scripts/
cp tavily_search.py test_skill/.claude/skills/法律研究/scripts/
cp config.py test_skill/.claude/skills/法律研究/scripts/
cp 法规检索Skill研发/引用格式要求.md test_skill/.claude/skills/法律研究/references/
```

### Step 3：创建 SKILL.md

基于现有 `test_command/.claude/commands/法律研究.md`，整合以下更新：

1. **frontmatter**：优化 `description`，加入触发关键词，使 Claude 自动识别法律问题场景
2. **移除 `$ARGUMENTS`**：改为从对话上下文读取用户问题
3. **整合 思路.md 的更新内容**：
   - 新增"首次使用时检测 API Key"提示（思路.md 第22-24行）
   - 新增第六阶段"验证和风险识别"自检清单（思路.md 第98-106行）
   - 新增第八阶段"工具使用报告"（思路.md 第154-158行）
   - 新增分析推理执行要求（思路.md 第82-86行：不得跳转结论、区分观点强弱、列明缺失事实）
   - 备忘录文首增加"收件人""发件人"字段（思路.md 第116-118行）
   - 法律研究方法论来源：IRAC/CREAC + Gutachtenstil（思路.md 第5行）
4. **API 调用路径更新**：调用示例中的脚本路径改为指向 `scripts/` 目录

### Step 4：验证

1. 确认目录结构和所有文件存在
2. 确认 SKILL.md frontmatter 格式正确（含 name 和 description）
3. 确认 scripts/ 下三个 Python 文件可被正确调用

---

## 关键文件清单

| 文件 | 来源路径 | 目标路径 | 操作 |
|------|---------|---------|------|
| 参考 Command | `test_command/.claude/commands/法律研究.md` | — | 读取 |
| 思路文档 | `法规检索Skill研发/思路.md` | — | 读取 |
| 引用格式 | `法规检索Skill研发/引用格式要求.md` | `skills/法律研究/references/` | 复制 |
| yuandian_api.py | 项目根目录 | `skills/法律研究/scripts/` | 复制 |
| tavily_search.py | 项目根目录 | `skills/法律研究/scripts/` | 复制 |
| config.py | 项目根目录 | `skills/法律研究/scripts/` | 复制 |
| SKILL.md | 新建 | `skills/法律研究/SKILL.md` | 创建 |

---

## SKILL.md description 触发关键词设计

应触发场景：
- 用户描述法律事实并询问法律问题
- 用户直接提出法律争议问题（是否有效、是否合法、如何处理）
- 用户要求分析某法规/条款的适用性
- 用户要求合规性论证
- 用户提到"法律备忘录""法律研究""法条""案例分析"

不触发场景：
- 编程、代码相关问题
- 非中国法律问题
- 一般性搜索或写作任务
