import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_direct_dashboard_id_references_exist_in_current_markup() -> None:
    app_js = (ROOT / "dashboard" / "app.js").read_text(encoding="utf-8")
    index_html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")

    markup_ids = set(re.findall(r'id=["\']([^"\']+)["\']', index_html))
    required_ids = set(
        re.findall(
            r'document\.getElementById\(["\']([^"\']+)["\']\)(?!\?)\.',
            app_js,
        )
    )

    assert required_ids <= markup_ids, f"Dashboard JavaScript directly references missing IDs: {sorted(required_ids - markup_ids)}"
