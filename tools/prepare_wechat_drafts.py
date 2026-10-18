from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "wechat-ai-rd"
ARTICLE_DIR = OUTPUT_DIR / "articles"


def main() -> None:
    manifest = json.loads((OUTPUT_DIR / "manifest.json").read_text(encoding="utf-8"))
    uploaded = json.loads((OUTPUT_DIR / "uploaded-assets.json").read_text(encoding="utf-8"))
    drafts: list[dict[str, object]] = []
    for article in manifest:
        document = (ARTICLE_DIR / article["html"]).read_text(encoding="utf-8")
        soup = BeautifulSoup(document, "html.parser")
        body = soup.select_one("article.article")
        if body is None:
            raise RuntimeError(f"Missing article body in {article['html']}")
        for image in body.find_all("img"):
            filename = Path(image["src"]).name
            image["src"] = uploaded[filename]["url"]
            image["data-wx-src"] = uploaded[filename]["url"]
        drafts.append(
            {
                "number": article["number"],
                "title": article["title"],
                "digest": article["digest"],
                "bodyHtml": body.decode_contents(),
                "coverAsset": article["assets"][0],
                "coverUrl": uploaded[article["assets"][0]]["url"],
                "coverFileId": uploaded[article["assets"][0]]["fileId"],
            }
        )
    output = OUTPUT_DIR / "draft-payloads.json"
    output.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Prepared {len(drafts)} draft payloads at {output}")


if __name__ == "__main__":
    main()
