from markdown_utils import markdown_to_text


def test_markdown_to_text_preserves_existing_cleanup_behavior() -> None:
    markdown = "# Title\n\n**Bold** `code`\n- item\n"

    assert markdown_to_text(markdown) == "Title\nBold code\n- item\n"
