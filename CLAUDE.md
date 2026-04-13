# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library for the 元典 (Yuandian) legal information API platform (`apiplatform.legalmind.cn`). It provides programmatic access to Chinese legal databases including statutes, case law, and company information.

## Running Scripts

```bash
cd /Users/jianjuntsai/Desktop/元典api
python 法条详细接口.py          # Test 法条详情 endpoint
python yuandian_api.py          # Run built-in quick tests
```

## Architecture

**`config.py`** — API key storage. All other scripts import `API_KEY` from here.

**`yuandian_api.py`** — The main reusable library. Import this in any new script:
```python
import sys, os
sys.path.insert(0, "/Users/jianjuntsai/Desktop/元典api")
from yuandian_api import search_fatiao, get_fagui_detail, search_ptal, ...
```

**`元典API接口文档.md`** — Complete reference for all 9 API interfaces. **Read this before making any API calls** — no need to visit the website.

## API Authentication

All requests use the `X-Api-Key` header (NOT `Authorization: Bearer`). This is handled automatically by `yuandian_api.py`'s `_post()` and `_get()` wrappers.

## Available API Functions

| Function | Method | Description |
|----------|--------|-------------|
| `search_fagui(keyword, ...)` | POST | 法规关键词检索 |
| `get_fagui_detail(id, fgmc, ...)` | POST | 法规详情（含全文） |
| `search_fatiao(keyword, ...)` | POST | 法条关键词检索 |
| `get_fatiao_detail(id, fgmc, ftnum, ...)` | POST | 法条详情 |
| `search_qwal(qw, ...)` | POST | 权威案例检索 |
| `search_ptal(qw, ...)` | POST | 普通案例检索 |
| `get_case_detail(type, id, ah)` | GET | 案例详情（type="ptal"或"qwal"） |
| `search_company_by_name(name, num)` | GET | 按名称搜索企业 |
| `get_company_detail(id, tyshxydm)` | GET | 按ID/信用代码查企业 |

## Typical Legal Research Workflow

1. `search_fatiao(keyword, sxx="现行有效", top_k=10)` — broad search, use `llm_content` field for LLM consumption
2. `search_fagui(keyword, sxx="现行有效", top_k=5)` — identify key regulations
3. `get_fagui_detail(fgmc="...")` — fetch full regulation text for detailed analysis

## Key API Response Notes

- All responses return `{"status": "success", "data": ...}` on success
- Case search `total` field is an integer (not a dict) — use `res.get('total', 0)`
- `llm_content` in fatiao/case search results is pre-formatted as `"- 《{fgmc}》{ft_num}##{content}"` for direct LLM use
- `search_qwal` and `search_ptal` return `{"total": int, "lst": [...]}` under `data`
