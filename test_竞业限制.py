#!/usr/bin/env python3
"""Test script for 竞业限制 research"""
import sys, json
sys.path.insert(0, "/Users/jianjuntsai/Desktop/元典api")
from yuandian_api import search_fatiao, get_fatiao_detail, search_fagui, search_qwal, search_ptal

# Test 1: Search for 竞业限制 法条
print("=== 搜索竞业限制法条 ===")
result = search_fatiao("竞业限制", sxx="现行有效", top_k=15)
if result:
    for item in result.get("lst", [])[:5]:
        print(item.get("llm_content", "")[:200])
        print()
