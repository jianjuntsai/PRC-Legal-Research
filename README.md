# 中国法律研究 Skill

面向中国境内法律研究的 agent skill。

## 研究框架

本 skill 的研究方法论融合了三种法律推理框架：

- **IRAC / CREAC**（英美法系）：Issue → Rule → Application → Conclusion，强调从规则到事实的演绎适用
- **Gutachtenstil**（德国法系）：问题式推理风格，按"假设前提 → 规则 → 涵摄 → 结论"逐层展开，适合处理复杂的法律解释问题
- **漏斗式结构**：从最宽泛的一般原则出发，逐步收窄至特别规定和具体适用，层次清晰

三者结合适应中国法律体系的特点——成文法为主、司法解释重要、裁判尺度存在地区差异。

## 工作原理

研究流程分八个阶段：

1. **信息完整性检查**：确认主体、事实、争议问题
2. **研究问题确认**：将事实转化为法律争议问题，与用户确认研究方向
3. **二手文献检索**：使用 Tavily 检索律所文章、政府解读、学术论文等，构建问题框架
4. **二手文献分析**：提取引用的法规条号、案例案号，为下一阶段检索提供线索
5. **权威法律渊源（Primary Sources）检索与验证**：通过元典 API 获取法条原文、裁判文书，验证二手文献的引用准确性
6. **分析与推理**：依托权威法律渊源，遵循推导链条（事实前提 → 法律问题 → 适用规则 → 规则解释 → 对事实的适用 → 初步结论 → 风险与不确定性）
7. **验证与风险识别**：自检来源层级、效力有效期、地区差异等
8. **生成法律研究备忘录**：输出标准格式 Markdown 文件

## 数据来源

| 类型 | 来源 | 用途 |
|------|------|------|
| 权威法律渊源（Primary Sources） | [元典 API](https://apiplatform.legalmind.cn/)（法条原文、裁判文书） | 最终结论的唯一依据 |
| 二手文献（Secondary Sources） | [Tavily](https://www.tavily.com/)（律所文章、政府解读、其他资料） | 构建分析框架、引出线索，不作为直接结论依据 |

**二手文献优先检索范围**：
- 律所文章：金杜（KWM）、君合、方达、中伦、通商、环球、海问、竞天公诚、植德、汉坤等头部律所
- 政府解读：全国人大、最高人民法院、司法部、各主要监管部门官网
- 其他资料：法学院校网站、法学期刊、书籍出版物、毕业论文、其他网络文章

## 适用场景

- 对某个交易或经营行为的合规性论证
- 分析中国境内全国范围或某地区的法律问题
- 对某个法律观点的正确性或实效性进行验证

## 安装

### 1. 克隆仓库

```bash
git clone <仓库地址>
```

### 2. 配置 API Key

复制配置模板：

```bash
cp scripts/config.example.py scripts/config.py
```

编辑 `scripts/config.py`，填入你的 API Key：

```python
API_KEY = "你的元典API密钥"          # 前往 https://apiplatform.legalmind.cn/ 获取
TAVILY_API_KEY = "你的TavilyAPI密钥"  # 前往 https://www.tavily.com/ 获取
```

> 如果使用支持 Skill 的 agent（如 Claude Code），首次启动时会自动检测到未配置的 Key，引导你输入并写入配置文件。

### 3. 安装 Skill

将 `prc-legal-research/` 目录放入对应 agent 的 Skills 目录，例如 Claude Code：

```bash
cp -r prc-legal-research ~/.claude/skills/
```

### 4. 安装 Python 依赖

```bash
pip install requests tavily-python
```

## 输出格式

每次研究生成一份 Markdown 法律研究备忘录（`法律备忘录_{主题}_{日期}.md`）：

```
一、核心结论
二、研究前提与适用范围
三、主要规则依据（法条原文）
四、分析
五、实务观点（二手文献观点）
六、风险与不确定性
七、结论与实务建议
八、主要法规依据清单
九、关键资料溯引图（mermaid）

工具使用报告
```

## 目录结构

```
PRC-Legal-Research/
├── README.md                 # 本文件
├── evals/                    # Skill 评测数据与方案
├── examples/                 # 法律研究备忘录示例
└── prc-legal-research/       # Skill 主目录（安装到 ~/.claude/skills/）
    ├── SKILL.md              # Skill 主文件（工作流程与研究指令）
    ├── scripts/
    │   ├── config.example.py # API Key 配置模板
    │   ├── config.py         # API Key 配置（本地使用，不提交 Git）
    │   ├── yuandian_api.py   # 元典 API 封装（权威法律渊源检索）
    │   └── tavily_search.py  # Tavily 封装（二手文献检索）
    └── references/
        └── 引用格式要求.md   # 法学引注规范
```

## 注意事项

- 本 skill 输出的备忘录仅供参考，不构成正式法律意见
- 建议将研究结论交由执业律师复核后使用
- API 调用会产生费用，请参考[元典 API](https://apiplatform.legalmind.cn/) 和 [Tavily](https://www.tavily.com/) 各自定价

## License

MIT
