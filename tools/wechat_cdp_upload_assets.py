from __future__ import annotations

import argparse
import base64
import json
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "wechat-ai-rd" / "assets"
OUTPUT = ROOT / "wechat-ai-rd" / "uploaded-assets.json"
PROXY = "http://localhost:3456"


def proxy_eval(target: str, expression: str) -> str:
    request = urllib.request.Request(
        f"{PROXY}/eval?target={urllib.parse.quote(target)}",
        data=expression.encode("utf-8"),
        headers={"Content-Type": "text/plain; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = json.load(response)
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["value"]


def upload_expression(filename: str, content: bytes) -> str:
    encoded = base64.b64encode(content).decode("ascii")
    quoted_name = json.dumps(filename, ensure_ascii=False)
    return f"""
(async()=>{{
  const b64={json.dumps(encoded)};
  const raw=atob(b64);
  const bytes=new Uint8Array(raw.length);
  for(let i=0;i<raw.length;i++) bytes[i]=raw.charCodeAt(i);
  const blob=new Blob([bytes],{{type:'image/png'}});
  const fd=new FormData();
  fd.append('id','WU_FILE_0');
  fd.append('name',{quoted_name});
  fd.append('type','image/png');
  fd.append('lastModifiedDate',new Date().toString());
  fd.append('size',String(blob.size));
  fd.append('upfile',blob,{quoted_name});
  const token=new URLSearchParams(location.search).get('token');
  const url='/cgi-bin/uploadimg2cdn?lang=zh_CN&token='+token+'&t='+Math.random()+'&watermark_free=1';
  const response=await fetch(url,{{method:'POST',body:fd,credentials:'include'}});
  return JSON.stringify({{status:response.status,text:await response.text()}});
}})()
"""


def upload_file(target: str, path: Path) -> dict[str, object]:
    outer = json.loads(proxy_eval(target, upload_expression(path.name, path.read_bytes())))
    if outer["status"] != 200:
        raise RuntimeError(f"Upload failed for {path.name}: HTTP {outer['status']}")
    payload = json.loads(outer["text"])
    if payload.get("errcode") != 0 or not payload.get("url"):
        raise RuntimeError(f"Upload failed for {path.name}: {payload}")
    return {
        "fileId": payload.get("file_id"),
        "format": payload.get("img_format"),
        "url": payload["url"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="CDP target id for an authenticated mp.weixin.qq.com editor tab")
    args = parser.parse_args()

    uploaded: dict[str, dict[str, object]] = {}
    paths = sorted(ASSET_DIR.glob("*.png"))
    for index, path in enumerate(paths, start=1):
        uploaded[path.name] = upload_file(args.target, path)
        print(f"[{index:02d}/{len(paths):02d}] uploaded {path.name}")
    OUTPUT.write_text(json.dumps(uploaded, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(uploaded)} asset URLs to {OUTPUT}")


if __name__ == "__main__":
    main()
