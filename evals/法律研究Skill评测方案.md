# 法律研究 Skill 评测方案

**版本**：v1.0
**日期**：2026-04-14
**适用 Skill**：法律研究（[PRC-Legal-Research](https://github.com/jianjuntsai/PRC-Legal-Research)）

---

## 一、评测目标

本方案用于评测「法律研究」Skill 在处理中国法律问题时的输出质量。

**核心指标**（按优先级排序）：

| 优先级 | 指标 | 说明 |
|--------|------|------|
| P0 | **结论准确性** | 核心法律结论是否与权威参考答案一致 |
| P0 | **关键法条覆盖** | 是否引用了参考答案中的关键法律条文 |
| P1 | **输出格式合规** | 是否符合九章节备忘录结构、含 mermaid 溯引图 |
| P1 | **研究流程完整** | 是否完整走完八阶段工作流（含二手文献检索、元典API验证） |

---

## 二、参考答案来源

评测使用**头部律所发布的权威文章**作为参考答案，原因：
1. 头部律所文章具有高度专业性，由资深律师撰写并经内部审核
2. 结论明确，法条引用清晰，便于逐条对比
3. 是 Skill 本身在二手文献检索阶段（第三阶段）应当发现的资料类型

### 三道题对应关系

| eval ID | 题目 | 参考答案机构 | 参考答案 URL |
|---------|------|------------|------------|
| eval-4 | 建设工程施工合同未备案是否影响效力 | 金杜律师事务所 | https://www.kingandwood.com/cn/zh/insights/latest-thinking/will-filing-affect-the-validity-of-a-construction-contract.html |
| eval-5 | 工伤复发停工留薪期（北京） | 金杜律师事务所 | https://www.kingandwood.com/cn/zh/insights/latest-thinking/faqs-on-the-recognition-of-work-related-injury-recurrence-and-related-issues-in-beijing.html |
| eval-6 | 有限公司简易注销后保证担保责任 | 通商律师事务所 | https://www.tongshang.com/Content/2025/12-19/1701439690.html |

---

## 三、评测断言设计

每道题设置两类断言：

- **通用断言**（所有 eval 共用）：检验格式和流程合规
- **专属断言**（每题独立）：检验结论准确性和关键法条覆盖

### 3.1 通用断言（适用于所有 eval）

| 断言 ID | 描述 | 判定标准 |
|---------|------|---------|
| `has_memo_file` | 输出了 .md 格式的法律备忘录文件 | 文件存在且为 Markdown 格式 |
| `has_nine_sections` | 备忘录包含九个章节（一至九） | 文中出现"## 一"至"## 九"的标题 |
| `cites_primary_law_text` | 所有引用法条均包含原文内容（非摘要） | 每条引用包含完整条文文字，非仅提及条号 |
| `has_tool_report` | 包含工具使用报告 | 文末有元典API和Tavily调用次数说明 |
| `has_mermaid` | 包含 mermaid 溯引图 | 文中有 \`\`\`mermaid 代码块 |

### 3.2 eval-4 专属断言：建设工程施工合同备案效力

**参考答案核心结论**（据金杜文章）：
1. 备案要求属"管理性规范"而非"效力性强制规定"，不影响合同效力
2. 强制备案制度已被正式删除（2018/2019年修订）
3. 合同有效仅需满足真实意思表示、不违反强制性规定

| 断言 ID | 描述 | 判定标准 |
|---------|------|---------|
| `conclusion_filing_not_affect_validity` | 核心结论为"备案不影响合同效力" | 备忘录明确得出"未备案合同有效"或等效表述 |
| `distinguishes_norm_types` | 区分了"管理性规范"与"效力性强制规定" | 文中出现该区分或等效论述 |
| `cites_construction_judicial_interpretation` | 引用《建设工程施工合同纠纷司法解释》相关条文 | 引用最高院司法解释（一）或（二）的具体条款原文 |

### 3.3 eval-5 专属断言：工伤复发停工留薪期（北京）

**参考答案核心结论**（据金杜文章）：
1. 北京实操中工伤复发认定以医院诊断证明为主要依据，无专门行政认定程序
2. 停工留薪期依据《北京市停工留薪期分类目录》确定，一般不超过12个月
3. 工伤职工在停工留薪期内原工资福利待遇不变

| 断言 ID | 描述 | 判定标准 |
|---------|------|---------|
| `conclusion_recurrence_entitles_treatment` | 结论支持工伤复发可获停工留薪待遇 | 备忘录结论明确甲公司应给予停工留薪待遇 |
| `cites_beijing_regulation` | 引用《北京市工伤职工停工留薪期管理办法》 | 引用该规章的具体条款原文 |
| `cites_work_injury_regulation` | 引用《工伤保险条例》相关条款 | 引用第33条（停工留薪期）或等效条款原文 |
| `identifies_12month_limit` | 提及停工留薪期12个月上限 | 文中出现"12个月"或"一年"的期限限制说明 |

### 3.4 eval-6 专属断言：简易注销后保证担保责任

**参考答案核心结论**（据通商文章）：
1. 保证债务具有独立性，不因保证人（公司）注销而当然消灭
2. 股东因承诺不实，依《公司法》第240条第3款承担连带责任，不以出资额为限
3. 股东可依《民法典》第700条向原债务人追偿

| 断言 ID | 描述 | 判定标准 |
|---------|------|---------|
| `conclusion_shareholder_liable` | 结论为股东须对保证债务承担连带/清偿责任 | 备忘录明确张某须承担连带责任 |
| `cites_company_law_240` | 引用《公司法》第240条 | 引用该条原文（含第3款关于承诺不实的连带责任） |
| `cites_judicial_interpretation_2` | 引用公司法司法解释二第20条 | 引用该条原文 |
| `identifies_unlimited_liability` | 指出股东责任不以出资额为限（或等效表述） | 文中出现该表述或"对注销前全部债务承担连带责任"等等效说明 |

---

## 四、评分方法

### 4.1 单题评分

对每条断言人工逐条判定，记录 `pass` / `fail` 及判定依据（`evidence`）。

```
单题得分 = 通过断言数 / 总断言数
```

### 4.2 维度得分

将断言分为两个维度单独统计：

| 维度 | 包含断言 |
|------|---------|
| **结论准确性** | `conclusion_*` 类断言 |
| **关键法条覆盖** | `cites_*` 类断言 |
| **格式合规** | 通用断言 |

### 4.3 整体评级

| 通过率 | 评级 |
|--------|------|
| ≥ 90% | A — 优秀 |
| 75%–89% | B — 良好 |
| 60%–74% | C — 合格 |
| < 60% | D — 需改进 |

---

## 五、评测文件组织规范

每道题在 `iteration-N/` 下建立独立目录，结构如下：

```
iteration-N/
└── eval-{id}-{题目}/
    ├── eval_metadata.json        # 断言定义（通用 + 专属）
    ├── with_skill/
    │   ├── outputs/
    │   │   └── 法律备忘录_*.md  # Skill 实际输出文件
    │   └── grading.json         # 逐条评分记录
    └── without_skill/            # 可选：无 Skill 的基础输出对比
        └── outputs/
            └── response.md
```

### grading.json 格式

```json
{
  "expectations": [
    {
      "text": "断言描述",
      "passed": true,
      "evidence": "具体引用输出中的内容作为判定依据"
    }
  ],
  "summary": {
    "passed": 8,
    "failed": 1,
    "total": 9,
    "pass_rate": 0.89
  },
  "dimension_scores": {
    "conclusion_accuracy": { "passed": 2, "total": 2 },
    "law_coverage": { "passed": 3, "total": 3 },
    "format_compliance": { "passed": 3, "total": 4 }
  },
  "claims": [
    {
      "claim": "引用的某法条为现行有效",
      "type": "factual",
      "verified": true,
      "evidence": "元典API返回 sxx=现行有效"
    }
  ]
}
```

---

## 六、与现有 eval-1~3 的关系

| 版本 | eval | 断言重心 |
|------|------|---------|
| iteration-1（已有） | eval-1~3 | 格式合规为主，少量内容断言 |
| **iteration-2（本方案）** | eval-4~6 | **内容准确性和法条覆盖为主**，有权威参考答案对照 |

**升级点**：eval-4~6 引入了外部权威参考答案，使"结论准确性"可以客观判定，而不仅依赖主观判断。

---

## 七、执行步骤

1. 将 Skill 输出（已存在的法律备忘录文件）复制到对应 `with_skill/outputs/` 目录
2. 按本方案的断言定义，创建各题的 `eval_metadata.json`
3. 对照参考答案和备忘录内容，人工填写 `grading.json`
4. 汇总各题得分，更新 `feedback.json`
5. 将新 eval 定义追加到 `evals/evals.json`

---

## 八、注意事项

- 参考答案本身不一定穷举所有正确结论，Skill 输出若包含**额外合理论证**，不应扣分
- 断言判定应以**实质内容**为准，不要求文字完全一致
- 若参考答案与法律原文存在出入，以**法律原文（元典API核实结果）为准**，参考答案降级为"实务观点参考"
