#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把固定舞台 HTML 演讲页导出为 1280×720 的 16:9 PDF。

原理：Playwright 驱动系统 Chromium，逐页调用页面内 show(i) 激活，对 #stage
按 2 倍缩放截图，再用 PyMuPDF 把每张贴满一页。非当前页 display:none，
因此不能用浏览器自带打印分页。

依赖：pip install pymupdf playwright；系统需有 chromium/chrome 与中文字体。
"""
import argparse
import os
import re
import shutil
import tempfile

import fitz  # PyMuPDF


def find_chromium():
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        path = shutil.which(name)
        if path:
            return path
    return None


def rewrite_to_local(html_text, mappings):
    """把在线图 URL 替换为本地 file 绝对路径（仅用于渲染，不改动交付文件）。"""
    for pair in mappings:
        if "|" not in pair:
            raise SystemExit(f"--map 参数格式应为 'URL|本地路径'，收到：{pair}")
        url, local = pair.split("|", 1)
        local = os.path.abspath(local)
        if not os.path.exists(local):
            raise SystemExit(f"本地资源不存在：{local}")
        html_text = html_text.replace(url, "file://" + local)
    return html_text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--wait", type=int, default=220, help="切页后等待毫秒")
    ap.add_argument("--map", action="append", default=[], help="URL|本地路径，可重复")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    src = os.path.abspath(args.html)
    with open(src, "r", encoding="utf-8") as f:
        html = f.read()
    html = rewrite_to_local(html, args.map)

    tmpdir = tempfile.mkdtemp(prefix="stage_pdf_")
    render_html = os.path.join(tmpdir, "render.html")
    with open(render_html, "w", encoding="utf-8") as f:
        f.write(html)

    chromium = find_chromium()
    launch_kwargs = {"args": ["--no-sandbox", "--force-color-profile=srgb"]}
    if chromium:
        launch_kwargs["executable_path"] = chromium

    shots = []
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": args.width, "height": args.height},
                                device_scale_factor=args.scale)
        page.goto("file://" + render_html)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(args.wait)

        if not page.evaluate("typeof slides !== 'undefined' && typeof show === 'function'"):
            browser.close()
            raise SystemExit("页面未暴露全局 slides / show(i)，请使用约定的固定舞台骨架。")

        total = page.evaluate("slides.length")
        stage = page.locator("#stage")
        for i in range(total):
            page.evaluate(f"show({i})")
            page.wait_for_timeout(args.wait)
            shot = os.path.join(tmpdir, f"p{i:03d}.png")
            stage.screenshot(path=shot)
            shots.append(shot)
        browser.close()

    # PyMuPDF 合成：每一页 1280×720 点，图片填满整页
    pdf = fitz.open()
    rect = fitz.Rect(0, 0, args.width, args.height)
    for shot in shots:
        page = pdf.new_page(width=args.width, height=args.height)
        page.insert_image(rect, filename=shot)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    pdf.save(args.out)
    pdf.close()
    shutil.rmtree(tmpdir, ignore_errors=True)
    print(f"已生成 {os.path.abspath(args.out)}，共 {len(shots)} 页")


if __name__ == "__main__":
    main()
