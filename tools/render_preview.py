"""把图表流水线产出的 SVG 同步渲染成 PNG，用于肉眼验收。

约定：任何图表脚本跑完后，都必须用本工具看一眼 PNG，
确认标签没被裁切、数值没压线、占比计算正确，再算交付。

用法：
    python tools/render_preview.py tools/build_project_charts.py
    python tools/render_preview.py tools/build_llm_project_charts.py
    python tools/render_preview.py tools/build_charts.py

产物写到 .workbuddy/preview/，不进仓库。
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = ROOT / ".workbuddy" / "preview"


def _patch(module_name: str) -> None:
    """给指定模块的 _save 打补丁：写 SVG 的同时写一份 PNG。"""
    mod = __import__(module_name, fromlist=["_save"])
    original = mod._save

    def patched(fig, out: Path) -> Path:
        result = original(fig, out)
        png = PREVIEW / out.relative_to(ROOT).with_suffix(".png")
        png.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(png, format="png", dpi=110)
        return result

    mod._save = patched


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(1)
    for name in ("content_kit.chartkit", "content_kit.diagramkit"):
        try:
            _patch(name)
        except ImportError:
            pass
    sys.path.insert(0, str(ROOT / "tools"))
    PREVIEW.mkdir(parents=True, exist_ok=True)
    for script in sys.argv[1:]:
        print(f"--- {script}")
        runpy.run_path(ROOT / script, run_name="__main__")
    print(f"PNG 预览目录：{PREVIEW}")


if __name__ == "__main__":
    main()
