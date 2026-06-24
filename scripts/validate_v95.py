"""Validate V9.5 localization and input mode upgrades."""

from __future__ import annotations

from pathlib import Path
import sys

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402
from localization import localized_question_intent, translate_text  # noqa: E402
from output_adapter import adapt_output  # noqa: E402


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_localization() -> None:
    sample = "\n".join(
        [
            "# Executive Intelligence Brief",
            "## Strategic Lessons",
            "- Supply chain diversification frequently appears after export-control or disruption shocks.",
            "## Current Event Context",
            "- **Confidence:** Medium",
        ]
    )
    simplified = translate_text(sample, "zh-CN")
    traditional = translate_text(sample, "zh-TW")
    require("战略经验" in simplified, "Simplified Chinese strategic lesson heading missing.")
    require("供应链多元化" in simplified, "Simplified Chinese strategic lesson sentence missing.")
    require("策略經驗" in traditional, "Traditional Chinese strategic lesson heading missing.")
    require("供應鏈多元化" in traditional, "Traditional Chinese strategic lesson sentence missing.")
    require("Medium" not in traditional, "Traditional Chinese output left confidence label in English.")
    require(localized_question_intent("Historical Comparison", "zh-CN") == "历史比较", "zh-CN question intent missing.")
    require(localized_question_intent("Decision Support", "zh-TW") == "決策支持", "zh-TW question intent missing.")

    adapted = adapt_output(sample, mode="analyst", language="zh-TW")
    require("高階主管情報簡報" in adapted or "分析師推理簡報" in adapted, "Adapted zh-TW brief missing localized title.")
    require("Strategic Lessons" not in adapted, "Adapted zh-TW brief left major heading in English.")


def validate_dashboard_modes() -> None:
    index = read("dashboard/index.html")
    app_js = read("dashboard/app.js")
    styles = read("dashboard/styles.css")
    for text in ["Paste Text", "Upload File", "Paste Link"]:
        require(text in index, f"Dashboard missing input mode: {text}.")
    require('id="source-url-input"' in index, "Dashboard missing source URL input.")
    require('accept=".md,.markdown,.txt,.pdf' in index, "Dashboard upload accept list missing PDF.")
    require("/extract-file" in app_js, "Dashboard missing backend file extraction call.")
    require("content_base64" in app_js, "Dashboard missing base64 file upload payload.")
    require("source_url" in app_js, "Dashboard missing source_url payload.")
    require(".input-mode-tabs" in styles, "Dashboard missing input mode tab styles.")


def validate_backend_and_requirements() -> None:
    app_source = read("app.py")
    requirements = read("requirements.txt")
    require("pypdf" in requirements.lower(), "requirements.txt missing pypdf.")
    require("@app.post(\"/extract-file\")" in app_source, "Backend missing /extract-file endpoint.")
    require("PdfReader" in app_source, "Backend missing PDF extraction code path.")
    require("source_url" in app_source, "Backend missing source_url artifact support.")

    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": "Export controls affect advanced chip suppliers and customer screening.",
            "language": "zh-TW",
            "output_mode": "analyst",
            "question_text": "這和哪些歷史事件相似？",
            "source_url": "https://example.com/source",
            "input_mode": "paste_link",
            "uploaded_filename": "",
            "file_type": "url",
        },
    )
    require(response.status_code == 200, f"Analyze with source_url failed: {response.text}")
    payload = response.json()
    require(payload["metadata"]["source_url"] == "https://example.com/source", "metadata missing source_url.")
    require(payload["analysis"]["source_url"] == "https://example.com/source", "analysis missing source_url.")
    require("來源連結" in payload["brief_markdown"], "localized brief missing source link label.")
    require("Strategic Lessons" not in payload["brief_markdown"], "zh-TW brief left major heading in English.")

    link_only = client.post(
        "/analyze",
        json={
            "text": "",
            "language": "en",
            "source_url": "https://example.com/link-only",
            "input_mode": "paste_link",
        },
    )
    require(link_only.status_code == 200, f"Link-only analyze failed: {link_only.text}")
    link_payload = link_only.json()
    require(link_payload["metadata"]["status"] == "link_only", "Link-only run status not recorded.")
    require("Live web retrieval is not enabled" in link_payload["analysis"]["message"], "Link-only message missing.")


def validate_docs() -> None:
    readme = read("README.md")
    doc = ROOT / "docs" / "v95_localization_input_modes.md"
    require(doc.exists(), "docs/v95_localization_input_modes.md missing.")
    require("Supported Input Modes" in readme, "README missing supported input modes.")
    require("text-based `.pdf`" in readme, "README missing text-based PDF support.")
    require("Live web retrieval is not enabled" in readme, "README missing no-live-web statement.")


def main() -> None:
    validate_localization()
    validate_dashboard_modes()
    validate_backend_and_requirements()
    validate_docs()
    print("V9.5 validation passed.")


if __name__ == "__main__":
    main()
