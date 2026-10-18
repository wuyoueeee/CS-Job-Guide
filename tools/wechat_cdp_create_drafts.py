from __future__ import annotations

import argparse
import base64
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "wechat-ai-rd"
PAYLOADS = OUTPUT_DIR / "draft-payloads.json"
RESULTS = OUTPUT_DIR / "draft-results.json"
PROXY = "http://localhost:3456"


def proxy_json(path: str, data: str | None = None, timeout: int = 120) -> dict:
    request = urllib.request.Request(
        f"{PROXY}{path}",
        data=data.encode("utf-8") if data is not None else None,
        headers={"Content-Type": "text/plain; charset=utf-8"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def proxy_eval(target: str, expression: str) -> str:
    payload = proxy_json(f"/eval?target={urllib.parse.quote(target)}", expression)
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["value"]


def click_at(target: str, selector: str) -> None:
    payload = proxy_json(f"/clickAt?target={urllib.parse.quote(target)}", selector)
    if not payload.get("clicked"):
        raise RuntimeError(f"Click failed: {selector}: {payload}")


def close(target: str) -> None:
    proxy_json(f"/close?target={urllib.parse.quote(target)}")


def targets() -> list[dict]:
    payload = proxy_json("/targets")
    return payload["value"] if isinstance(payload, dict) else payload


def wait_until(check: Callable[[], object], timeout: float = 30, interval: float = 0.5) -> object:
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            last = check()
            if last:
                return last
        except Exception as error:  # Browser pages are briefly unavailable during navigation.
            last = error
        time.sleep(interval)
    raise TimeoutError(f"Timed out waiting for browser state. Last value: {last}")


def wait_eval(target: str, expression: str, timeout: float = 30) -> str:
    return str(wait_until(lambda: proxy_eval(target, expression), timeout=timeout))


def utf8_b64(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def create_editor_tab(list_target: str) -> str:
    token = proxy_eval(list_target, "new URLSearchParams(location.search).get('token')")
    timestamp = int(time.time() * 1000)
    url = (
        "https://mp.weixin.qq.com/cgi-bin/appmsg?"
        f"t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={token}&lang=zh_CN&timestamp={timestamp}"
    )
    target = proxy_json("/new", url)["targetId"]
    wait_eval(target, "document.querySelector('#title')?'ok':''", timeout=45)
    wait_eval(target, "document.querySelector('#js_cover_area')?'ok':''", timeout=45)
    return target


def fill_editor(target: str, payload: dict[str, object]) -> None:
    wait_eval(target, "window.__mpTitleEditor&&typeof window.__mpTitleEditor.setContent==='function'?'ok':''", timeout=45)
    title = utf8_b64(str(payload["title"]))
    digest = utf8_b64(str(payload["digest"]))
    body = utf8_b64(str(payload["bodyHtml"]))
    result = json.loads(
        proxy_eval(
            target,
            f"""
(()=>{{
  const dec=s=>new TextDecoder().decode(Uint8Array.from(atob(s),c=>c.charCodeAt(0)));
  const setValue=(el,value)=>{{
    const setter=Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el),'value').set;
    setter.call(el,value);
    el.dispatchEvent(new Event('input',{{bubbles:true}}));
    el.dispatchEvent(new Event('change',{{bubbles:true}}));
  }};
  const title=dec('{title}');
  setValue(document.querySelector('#title'),title);
  window.__mpTitleEditor.setContent(title);
  setValue(document.querySelector('#js_description'),dec('{digest}'));
  const editor=[...document.querySelectorAll('[contenteditable=true].ProseMirror')].find(x=>!x.classList.contains('mpa-title-input'));
  editor.focus();
  editor.innerHTML=dec('{body}');
  editor.dispatchEvent(new InputEvent('input',{{bubbles:true,inputType:'insertFromPaste'}}));
  return JSON.stringify({{title:document.querySelector('#title').value}});
}})()
""",
        )
    )
    if result["title"] != payload["title"]:
        raise RuntimeError(f"Editor fill verification failed: {result}")
    wait_eval(
        target,
        "window.__mpTitleEditor&&window.__mpTitleEditor.getContent()===document.querySelector('#title').value?'ok':''",
    )
    wait_eval(
        target,
        "(()=>{const e=[...document.querySelectorAll('[contenteditable=true].ProseMirror')].find(x=>!x.classList.contains('mpa-title-input'));return e&&e.querySelectorAll('img[src*=\"mmbiz.\"]').length===3?'ok':''})()",
    )


def set_cover_from_first_image(target: str) -> None:
    proxy_eval(target, "(()=>{document.querySelector('#js_cover_area .js_cover_btn_area').click();return 'ok'})()")
    wait_eval(
        target,
        """(()=>{const x=document.querySelector('#js_cover_null .js_selectCoverFromContent');return x&&getComputedStyle(document.querySelector('#js_cover_null')).display!=='none'?'ok':''})()""",
    )
    proxy_eval(target, "(()=>{document.querySelector('#js_cover_null .js_selectCoverFromContent').click();return 'ok'})()")
    wait_eval(target, "document.querySelector('.weui-desktop-dialog_img-picker .appmsg_content_img_item')?'ok':''")
    proxy_eval(target, "(()=>{document.querySelector('.weui-desktop-dialog_img-picker .appmsg_content_img_item').click();return 'ok'})()")
    proxy_eval(
        target,
        """
(()=>{const b=[...document.querySelectorAll('.weui-desktop-dialog_img-picker button')].find(x=>(x.innerText||'').trim()==='下一步');
if(!b)return '';b.click();return 'ok'})()
""",
    )
    wait_eval(
        target,
        """(()=>{const b=[...document.querySelectorAll('.weui-desktop-dialog__wrp button')].find(x=>(x.innerText||'').trim()==='确认'&&getComputedStyle(x.parentElement).display!=='none');return b?'ok':''})()""",
    )
    proxy_eval(
        target,
        """
(()=>{const b=[...document.querySelectorAll('.weui-desktop-dialog__wrp button')].find(x=>(x.innerText||'').trim()==='确认'&&getComputedStyle(x.parentElement).display!=='none');
if(!b)return '';b.click();return 'ok'})()
""",
    )
    wait_eval(target, "window.__coverImageInfo__&&window.__coverImageInfo__[0]&&window.__coverImageInfo__[0].check?'ok':''")


def save_draft(target: str) -> str:
    proxy_eval(
        target,
        """
(()=>{const b=[...document.querySelectorAll('button')].find(x=>(x.innerText||'').trim()==='保存为草稿');
if(!b)return '';b.click();return 'ok'})()
""",
    )
    try:
        url = wait_eval(target, "location.href.includes('appmsgid=')?location.href:''", timeout=90)
    except TimeoutError as error:
        diagnostics = proxy_eval(
            target,
            """
JSON.stringify({
  url:location.href,
  dialogs:[...document.querySelectorAll('.weui-desktop-dialog__wrp')].map(x=>({text:(x.innerText||'').trim(),rect:(()=>{const r=x.getBoundingClientRect();return {w:r.width,h:r.height}})()})).filter(x=>x.rect.w||x.rect.h),
  errors:[...document.querySelectorAll('.js_error_msg,.frm_msg.fail,.page_msg')].map(x=>({text:(x.innerText||'').trim(),display:getComputedStyle(x).display})).filter(x=>x.display!=='none'),
  saveButtons:[...document.querySelectorAll('button')].map(x=>({text:(x.innerText||'').trim(),disabled:x.disabled,class:x.className})).filter(x=>x.text.includes('保存'))
})
""",
        )
        raise TimeoutError(f"{error} Diagnostics: {diagnostics}") from error
    match = re.search(r"[?&]appmsgid=(\d+)", url)
    if not match:
        raise RuntimeError(f"Draft saved but appmsgid was not found: {url}")
    time.sleep(2)
    return match.group(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-target", required=True, help="CDP target id for the authenticated draft list tab")
    parser.add_argument("--start", type=int, default=1, help="1-based article index to start creating")
    parser.add_argument("--first-appmsg-id", help="Existing appmsg id for article 1 when resuming from article 2")
    args = parser.parse_args()

    payloads: list[dict[str, object]] = json.loads(PAYLOADS.read_text(encoding="utf-8"))
    results: list[dict[str, object]] = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else []
    if args.first_appmsg_id and not any(item["number"] == payloads[0]["number"] for item in results):
        results.append({"number": payloads[0]["number"], "title": payloads[0]["title"], "appmsgId": args.first_appmsg_id})

    for index, payload in enumerate(payloads[args.start - 1 :], start=args.start):
        editor_target = create_editor_tab(args.list_target)
        saved = False
        try:
            fill_editor(editor_target, payload)
            set_cover_from_first_image(editor_target)
            appmsg_id = save_draft(editor_target)
            results.append({"number": payload["number"], "title": payload["title"], "appmsgId": appmsg_id})
            RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[{index:02d}/{len(payloads):02d}] saved {payload['title']} as {appmsg_id}")
            saved = True
        finally:
            if saved:
                close(editor_target)
            else:
                print(f"Leaving failed editor tab open for inspection: {editor_target}")
    print(f"Saved {len(results)} draft results to {RESULTS}")


if __name__ == "__main__":
    main()
