"""Bounded HTTP GET for official public hosts only."""

from __future__ import annotations

from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ALLOWED_HOSTS = frozenset(
    {
        "api.stlouisfed.org",
        "home.treasury.gov",
        "www.federalreserve.gov",
    }
)

DEFAULT_TIMEOUT_SECONDS = 30.0
_USER_AGENT = "DeWittResearchWorkshop-public-feeds/1.0 (+https://www.dewitt-labs.com)"


class FeedFetchError(RuntimeError):
    """A refused or failed official-feed request."""


def require_allowed_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise FeedFetchError(f"refusing non-HTTPS feed URL: {parsed.scheme}")
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise FeedFetchError(f"host {host!r} is not on the official-feed allowlist")


def fetch_text(url: str, *, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> str:
    """GET an allowlisted HTTPS URL. Never follows a redirect off the list."""
    require_allowed_url(url)
    request = Request(  # noqa: S310
        url, headers={"User-Agent": _USER_AGENT, "Accept": "*/*"}
    )
    try:
        # Allowlist is enforced before the call; urllib is the stdlib client.
        with urlopen(request, timeout=timeout) as response:  # noqa: S310  # nosec B310
            final = response.geturl()
            require_allowed_url(final)
            raw = bytes(response.read())
    except HTTPError as exc:
        raise FeedFetchError(f"HTTP {exc.code} from {urlparse(url).hostname}") from exc
    except URLError as exc:
        raise FeedFetchError(f"network error contacting {urlparse(url).hostname}") from exc
    return raw.decode("utf-8", errors="replace")
