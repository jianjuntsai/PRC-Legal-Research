# 元典 API 接口文档

**平台地址**：https://apiplatform.legalmind.cn
**认证方式**：所有接口请求头需携带 `X-Api-Key: {your_api_key}`
**通用响应结构**：

```json
{
  "status": "success",   // 或 "failed"、"notFound"
  "code": 200,           // 200 成功，500/501 失败，404 未找到
  "message": "请求成功",
  "data": {}             // 业务数据，失败时可能为 null
}
```

---

## 一、法律法规类

### 1. 法规关键词检索

- **URL**：`POST https://apiplatform.legalmind.cn/open/rh_fg_search`
- **用途**：按关键词搜索法规列表，支持多条件过滤。`keyword` 可不传，此时按过滤条件返回法规列表。

**请求参数（Body JSON）**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword` | string | 否 | 法规内容关键词（空格按 `search_mode` 拆分为 AND/OR） |
| `search_mode` | string | 否 | 关键词拼接模式：`AND`/`OR`，默认 `AND` |
| `fgmc` | string | 否 | 法规名称过滤（按空格拆分，需全部命中） |
| `sxx` | string | 否 | 时效性过滤（可选值：现行有效、失效、已被修改、部分失效、尚未生效；多值空格分隔，命中任一即可） |
| `xljb_1` | string | 否 | 效力级别过滤（可选值：宪法、法律、司法解释、行政法规、监察法规、部门规章、党内法规、军事法规规章、地方性法规等；多值空格分隔，命中任一即可） |
| `fbrq_start` | string | 否 | 发布日期起，格式 `yyyy-MM-dd` |
| `fbrq_end` | string | 否 | 发布日期止，格式 `yyyy-MM-dd` |
| `ssrq_start` | string | 否 | 实施日期起，格式 `yyyy-MM-dd` |
| `ssrq_end` | string | 否 | 实施日期止，格式 `yyyy-MM-dd` |
| `top_k` | number | 否 | 返回条数上限，默认 10，最大 50 |

> **注意**：请求体不能为空 JSON `{}`

**响应 `data` 字段**（数组，每条为法规摘要）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 法规 ID |
| `fgmc` | string | 法规名称 |
| `title` | string | 同 fgmc |
| `fbbm` | string | 发布部门 |
| `fwzh` | string | 发文字号 |
| `xljb_1` | string | 效力级别-一级 |
| `xljb_2` | string | 效力级别-二级 |
| `sxx` | string | 时效性 |
| `fbrq` | string | 发布日期 |
| `ssrq` | string | 实施日期 |
| `url` | string | 详情地址 `/zxt/statuteDetail/detailPage/{id}` |
| `content` | string | **可选**：仅当传入 `keyword` 且命中时返回高亮片段（非全文） |
| `_score` | number | ES 相关性分数 |

**curl 示例**：
```bash
curl -X POST "https://apiplatform.legalmind.cn/open/rh_fg_search" \
  -H "X-Api-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "合同违约", "sxx": "现行有效", "top_k": 5}'
```

---

### 2. 法规详情

- **URL**：`POST https://apiplatform.legalmind.cn/open/rh_fg_detail`
- **用途**：获取一部法规的完整详情，包含全文 `content`。

**请求参数（Body JSON）**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 否 | 法规 ID（与 `fgmc` 至少填一个） |
| `fgmc` | string | 否 | 法规名称（当 `id` 为空时必填） |
| `refer_date` | string | 否 | 参考日期（格式 `yyyy-MM-dd`），用于查询特定历史版本，不填则返回当前有效版本 |

**响应 `data` 字段**（法规详情对象）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 法规 ID |
| `fgid` | string | 同法规 ID |
| `type` | string | 固定为 `法规` |
| `fgmc` | string | 法规名称 |
| `xljb_1` | string | 效力级别-一级 |
| `xljb_2` | string | 效力级别-二级 |
| `sxx` | string | 时效性 |
| `fbrq` | string | 发布日期 |
| `ssrq` | string | 实施日期 |
| `fwzh` | string | 发文字号 |
| `fbbm` | string | 发布部门 |
| `content` | string | 法规全文内容 |
| `url` | string | 详情地址 `/zxt/statuteDetail/detailPage/{id}` |

**curl 示例**：
```bash
curl -X POST "https://apiplatform.legalmind.cn/open/rh_fg_detail" \
  -H "X-Api-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fgmc": "中华人民共和国民法典"}'
```

---

### 3. 法条关键词检索

- **URL**：`POST https://apiplatform.legalmind.cn/open/rh_ft_search`
- **用途**：按关键词检索法条内容，返回含 `llm_content` 的法条列表（适合 LLM 直接使用）。

**请求参数（Body JSON）**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword` | string | **是** | 法条内容关键词 |
| `search_mode` | string | 否 | 关键词拼接模式：`AND`/`OR`，默认 `AND` |
| `fgmc` | string | 否 | 法规名称过滤 |
| `xljb_1` | string | 否 | 效力级别过滤（同法规检索可选值） |
| `sxx` | string | 否 | 时效性过滤（同法规检索可选值） |
| `fbrq_start` | string | 否 | 发布日期起 |
| `fbrq_end` | string | 否 | 发布日期止 |
| `ssrq_start` | string | 否 | 实施日期起 |
| `ssrq_end` | string | 否 | 实施日期止 |
| `top_k` | number | 否 | 返回条数上限，默认 10，最大 50 |

**响应 `data` 字段**（数组，每条为法条摘要）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 法条文档 ID |
| `fgid` | string | 所属法规 ID |
| `ftmc` | string | 法条名称（含法规名，如：《民法典》第一条） |
| `ft_num` | string | 法条号/名称（如：第一条） |
| `fgmc` | string | 法规名称 |
| `content` | string | 法条内容 |
| `llm_content` | string | **LLM 专用字段**，格式：`- 《{fgmc}》{ft_num}##{content}`（`##` 为分隔符） |
| `sxx` | string | 所属法规时效性 |
| `xljb_1` | string | 所属法规效力级别-一级 |
| `xljb_2` | string | 所属法规效力级别-二级 |
| `fbrq` | string | 所属法规发布日期 |
| `ssrq` | string | 所属法规实施日期 |
| `fbbm` | string | 所属法规发布部门 |
| `fwzh` | string | 所属法规发文字号 |
| `url` | string | 详情地址 |
| `_score` | number | ES 相关性分数 |

**curl 示例**：
```bash
curl -X POST "https://apiplatform.legalmind.cn/open/rh_ft_search" \
  -H "X-Api-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "合同违约责任", "sxx": "现行有效", "top_k": 10}'
```

---

### 4. 法条详情

- **URL**：`POST https://apiplatform.legalmind.cn/open/rh_ft_detail`
- **用途**：获取指定法条的详情内容。

**请求参数（Body JSON）**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 否 | 法条文档 ID（与 `fgmc`+`ftnum` 至少填一组） |
| `fgmc` | string | 否 | 法规名称（当 `id` 为空时必填） |
| `ftnum` | string | 否 | 法条号/名称（当 `id` 为空时必填，如"第一百条"） |
| `refer_date` | string | 否 | 参考日期（格式 `yyyy-MM-dd`） |

**响应 `data` 字段**（法条详情对象）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 法条文档 ID |
| `fgid` | string | 所属法规 ID |
| `type` | string | 固定为 `法条` |
| `tid` | string | 条编号（如：100） |
| `ftmc` | string | 法条名称（含法规名，如：民法典第一百条） |
| `ft_num` | string | 法条号/名称（如：第一百条） |
| `fgmc` | string | 法规名称 |
| `content` | string | 法条内容 |
| `sxx` | string | 所属法规时效性 |
| `xljb_1` | string | 所属法规效力级别-一级 |
| `xljb_2` | string | 所属法规效力级别-二级 |
| `fbrq` | string | 所属法规发布日期 |
| `ssrq` | string | 所属法规实施日期 |
| `url` | string | 详情地址 `/zxt/statuteDetail/detailPage/{fgid}?text={tid}` |

**curl 示例**：
```bash
curl -X POST "https://apiplatform.legalmind.cn/open/rh_ft_detail" \
  -H "X-Api-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fgmc": "中华人民共和国民法典", "ftnum": "第二百零一条"}'
```

---

## 二、案例文书类

### 5. 权威案例关键词检索

- **URL**：`POST https://apiplatform.legalmind.cn/open/rh_qwal_search`
- **用途**：检索"权威案例"库（指导性案例、典型案例等），优先返回要旨/摘要。

**请求参数（Body JSON，所有字段可选，但请求体不能为空）**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `qw` | string | 全文关键词（按 `search_mode` 拆分） |
| `search_mode` | string | `and`/`or`，默认 `and` |
| `title` | string | 标题精确短语匹配 |
| `ah` | string | 案号 |
| `ay` | string[] | 案由数组（多值为或关系） |
| `jbdw` | string[] | 经办法院数组（多值为或关系） |
| `xzqh_p` | string[] | 省级行政区数组（可选值：北京、上海、广东等全部省份及最高） |
| `wszl` | string[] | 文书种类（可选值：判决书、裁定书、调解书、决定书） |
| `ajlb` | string | 案件类别（可选值：刑事案件、民事案件、行政案件、执行案件等） |
| `ja_start` | string | 裁判日期起，格式 `yyyy-MM-dd` |
| `ja_end` | string | 裁判日期止，格式 `yyyy-MM-dd` |
| `top_k` | number | 返回条数上限，默认 10，最大 50 |

**响应 `data` 字段**（包含两个子字段）：

- `data.total`：命中总数
- `data.lst`：命中列表，每条字段如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 案例 ID |
| `type` | string | 固定为 `权威案例` |
| `ah` | string | 案号 |
| `title` | string | 标题 |
| `ay` | string | 案由 |
| `jbdw` | string | 经办法院 |
| `ajlb` | string | 案件类别 |
| `xzqh_p` | string | 省级行政区 |
| `wszl` | string | 文书种类 |
| `cprq` | string | 裁判日期 |
| `content` | string | 内容：优先取要旨/摘要，为空则回退全文 |
| `llm_content` | string | **LLM 专用字段**，格式：`{ah}##{content}` |
| `url` | string | 详情 URL |
| `score` | number | 相关性分数 |

**curl 示例**：
```bash
curl -X POST "https://apiplatform.legalmind.cn/open/rh_qwal_search" \
  -H "X-Api-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"qw": "合同违约", "ajlb": "民事案件", "top_k": 5}'
```

---

### 6. 普通案例关键词检索

- **URL**：`POST https://apiplatform.legalmind.cn/open/rh_ptal_search`
- **用途**：检索"普通案例"库（裁判文书网等），返回内容片段/摘要。

**请求参数（Body JSON，所有字段可选，但请求体不能为空）**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `qw` | string | 全文关键词 |
| `fxgc` | string | 分析过程关键词（独立检索字段） |
| `search_mode` | string | `and`/`or`，默认 `and` |
| `title` | string | 标题精确匹配 |
| `ah` | string | 案号 |
| `ay` | string[] | 案由数组（多值为或关系） |
| `jbdw` | string[] | 经办法院/承办单位数组 |
| `xzqh_p` | string[] | 省级行政区数组 |
| `wszl` | string[] | 文书种类（判决书、裁定书、调解书、决定书） |
| `ajlb` | string | 案件类别 |
| `ja_start` | string | 结案/裁判日期起 |
| `ja_end` | string | 结案/裁判日期止 |
| `yyft` | string[] | 援引法条数组（如 `["中华人民共和国刑法第二条"]`，法条号需为中文格式） |
| `ft_search_mode` | string | `yyft` 的拼接模式：`and`/`or`，默认 `and` |
| `top_k` | number | 返回条数上限，默认 10，最大 50 |

**响应 `data` 字段**（同权威案例，包含 `total` 和 `lst`）：

`lst` 每条字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 案例 ID |
| `type` | string | 固定为 `普通案例` |
| `ah` | string | 案号 |
| `title` | string | 标题 |
| `ay` | string | 案由 |
| `jbdw` | string | 经办法院/承办单位 |
| `ajlb` | string | 案件类别 |
| `xzqh_p` | string | 省级行政区 |
| `wszl` | string | 文书种类 |
| `cprq` | string | 裁判/结案日期 |
| `content` | string | 内容片段（有关键词时优先高亮片段，否则优先摘要，最后回退分析过程） |
| `llm_content` | string | **LLM 专用字段**，格式：`{ah}##{content}` |
| `url` | string | 详情 URL |
| `score` | number | 相关性分数 |

**curl 示例**：
```bash
curl -X POST "https://apiplatform.legalmind.cn/open/rh_ptal_search" \
  -H "X-Api-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"qw": "合同违约损害赔偿", "ajlb": "民事案件", "top_k": 5}'
```

---

### 7. 案例详情

- **URL**：`GET https://apiplatform.legalmind.cn/open/rh_case_details`
- **用途**：按 ID 或案号获取普通案例或权威案例的完整详情（含正文全文）。

**请求参数（Query 参数）**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 否 | 案例 ID（与 `ah` 至少填一个） |
| `ah` | string | 否 | 案号（当 `id` 为空时用于查询） |
| `type` | string | **是** | 案例类型：`ptal`（普通案例）或 `qwal`（权威案例） |

**响应 `data` 字段**（列表，最多 10 条）：

**普通案例（type=ptal）主要字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 案例 ID |
| `type` | string | 固定为 `普通案例` |
| `ah` | string | 案号 |
| `title` | string | 标题 |
| `jbdw` | string | 经办法院 |
| `ajlb` | string | 案件类别 |
| `ajlx` | string | 案件类型 |
| `spcx` | string | 审判程序 |
| `wszl` | string | 文书种类 |
| `ay` | string | 案由 |
| `cprq` | string | 日期 |
| `xzqh_p` | string | 省级行政区 |
| `yyft` | string | 援引法条 |
| `content` | string | 正文全文 |
| `dsr` | string | 当事人段 |
| `ssjl` | string | 诉讼记录段 |
| `ajjbqk` | string | 案件基本情况段 |
| `fxgc` | string | 分析过程段 |
| `pjjg` | string | 判决结果段 |
| `cmss` | string | 查明事实段 |
| `ww` | string | 文尾 |
| `url` | string | 详情 URL：`/ydzk/caseDetail/case/{id}` |

**权威案例（type=qwal）主要字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 案例 ID |
| `type` | string | 固定为 `权威案例` |
| `ah` | string | 案号 |
| `title` | string | 标题 |
| `jbdw` | string | 经办法院 |
| `ajlb` | string | 案件类别 |
| `spcx` | string | 审判程序 |
| `wszl` | string | 文书种类 |
| `ay` | string | 案由 |
| `cprq` | string | 裁判日期 |
| `xzqh_p` | string | 省级行政区 |
| `content` | string | 正文全文 |
| `url` | string | 详情 URL：`/ydzk/caseDetail/qwcase/{id}` |

**curl 示例**：
```bash
curl -G "https://apiplatform.legalmind.cn/open/rh_case_details" \
  -H "X-Api-Key: YOUR_KEY" \
  --data-urlencode "ah=(2021)最高法民终123号" \
  --data-urlencode "type=ptal"
```

---

## 三、企业信息类

### 8. 按名称查询企业详情

- **URL**：`GET https://apiplatform.legalmind.cn/open/rh_company_info`
- **用途**：按企业名称（含全称、曾用名、股票简称等）模糊搜索，返回多条企业详情。

**请求参数（Query 参数）**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | **是** | 企业名称或股票简称等检索词 |
| `num` | int | 否 | 返回条数上限，默认 2；取值范围 0-50（超出范围置为 10） |

**响应 `data` 字段**（企业详情对象列表）：

每条企业详情包含以下模块（字段名为中文 key）：

| 模块 | 主要字段 |
|------|---------|
| 基础标识 | 企业ID、企业名称 |
| 工商与登记信息 | 法定代表人、统一社会信用代码、注册资本、成立日期、经营状态、经营范围、核心成员 |
| 股东与分支机构 | 股东列表、分支机构列表 |
| 变更与对外投资 | 历史变更记录、对外投资情况 |
| 知识产权 | 商标、软件著作权、作品著作权、专利列表 |
| 涉诉信息 | 涉诉列表（案号、案由、文书id、诉讼地位） |
| 风险 | 风险标签 |

**curl 示例**：
```bash
curl -G "https://apiplatform.legalmind.cn/open/rh_company_info" \
  -H "X-Api-Key: YOUR_KEY" \
  --data-urlencode "name=阿里巴巴" \
  --data-urlencode "num=1"
```

---

### 9. 按 ID/统一社会信用代码查询企业详情

- **URL**：`GET https://apiplatform.legalmind.cn/open/rh_company_detail`
- **用途**：精确查询单家企业的完整详情。

**请求参数（Query 参数）**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 否 | 企业 ID（与 `tyshxydm` 至少填一个，优先用 id） |
| `tyshxydm` | string | 否 | 统一社会信用代码 |

**响应 `data` 字段**：同上，返回单条企业详情对象（非列表）。

**curl 示例**：
```bash
curl -G "https://apiplatform.legalmind.cn/open/rh_company_detail" \
  -H "X-Api-Key: YOUR_KEY" \
  --data-urlencode "tyshxydm=91310000677833266F"
```

---

## 附：接口速查表

| # | 接口名称 | 方法 | URL | 核心参数 |
|---|---------|------|-----|---------|
| 1 | 法规关键词检索 | POST | `/open/rh_fg_search` | keyword（可选）, sxx, xljb_1, top_k |
| 2 | 法规详情 | POST | `/open/rh_fg_detail` | id 或 fgmc（必填一个）, refer_date |
| 3 | 法条关键词检索 | POST | `/open/rh_ft_search` | keyword（必填）, fgmc, sxx, top_k |
| 4 | 法条详情 | POST | `/open/rh_ft_detail` | id 或 fgmc+ftnum（必填一组）, refer_date |
| 5 | 权威案例检索 | POST | `/open/rh_qwal_search` | qw, ay, ajlb, top_k |
| 6 | 普通案例检索 | POST | `/open/rh_ptal_search` | qw, fxgc, ay, ajlb, yyft, top_k |
| 7 | 案例详情 | GET | `/open/rh_case_details` | type（必填）, id 或 ah（必填一个） |
| 8 | 企业名称查询 | GET | `/open/rh_company_info` | name（必填）, num |
| 9 | 企业ID/信用代码查询 | GET | `/open/rh_company_detail` | id 或 tyshxydm（必填一个） |
