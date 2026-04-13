"""
Tavily 检索封装 — 用于法律研究中的二手资料检索
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from config import TAVILY_API_KEY
from tavily import TavilyClient

client = TavilyClient(api_key=TAVILY_API_KEY)


def search_secondary_sources(query, max_results=10, search_depth="advanced",
                             include_domains=None, exclude_domains=None):
    """
    检索二手法律资料
    - query: 检索关键词
    - max_results: 返回结果数，默认10
    - search_depth: "basic" 或 "advanced"（更深入），默认 advanced
    - include_domains: 限定域名列表（如律所网站）
    - exclude_domains: 排除域名列表
    返回: list[dict]，每条含 title/url/content/score
    """
    kwargs = {
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
    }
    if include_domains:
        kwargs["include_domains"] = include_domains
    if exclude_domains:
        kwargs["exclude_domains"] = exclude_domains

    result = client.search(**kwargs)
    return result.get("results", [])


def search_lawfirm_articles(query, max_results=5):
    """
    专门检索头部律所的法律分析文章
    优先：金杜、君合、方达、中伦、通商、环球、海问、竞天公诚、植德、汉坤
    """
    lawfirm_domains = [
        "kwm.com",              # 金杜
        "junhe.com",            # 君合
        "fangda-partners.com",  # 方达
        "zhonglun.com",         # 中伦
        "tongshang.com",        # 通商
        "haiwen-law.com",       # 海问
        "hankunlaw.com",        # 汉坤
        "jingtian.com",         # 竞天公诚
        "meritsandtree.com",    # 植德
        "globe-law.com",        # 环球
    ]
    return search_secondary_sources(
        query=query,
        max_results=max_results,
        include_domains=lawfirm_domains,
    )


def search_government_interpretations(query, max_results=5):
    """
    检索政府网站的政策解读、答记者问等
    """
    gov_domains = [
        "gov.cn",
        "npc.gov.cn",
        "court.gov.cn",
        "spp.gov.cn",
        "moj.gov.cn",
    ]
    return search_secondary_sources(
        query=query,
        max_results=max_results,
        include_domains=gov_domains,
    )


# ──────────────────────────────────────────────
# 快速测试
# ──────────────────────────────────────────────

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "合同违约责任 法律分析"

    print(f"=== 综合检索：{keyword} ===")
    results = search_secondary_sources(keyword, max_results=3)
    for r in results:
        print(f"- [{r.get('score', 0):.2f}] {r['title']}")
        print(f"  {r['url']}")
        print(f"  {r.get('content', '')[:100]}...")
        print()

    print(f"\n=== 律所文章检索：{keyword} ===")
    results = search_lawfirm_articles(keyword, max_results=3)
    for r in results:
        print(f"- {r['title']}")
        print(f"  {r['url']}")
        print()
