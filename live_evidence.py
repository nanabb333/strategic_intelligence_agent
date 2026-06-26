import requests
import trafilatura


def fetch_url_text(url: str) -> str:
    """
    Fetch readable text from a public URL.

    This function is used as an evidence source.
    It does not make decisions by itself.
    """
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )

    response.raise_for_status()

    extracted = trafilatura.extract(response.text)

    if not extracted or len(extracted.strip()) < 20:
        raise ValueError("Could not extract enough readable text from this URL.")

    return extracted.strip()
    
if __name__ == "__main__":
    url = "https://example.com"

    text = fetch_url_text(url)

    print(text[:1000])
