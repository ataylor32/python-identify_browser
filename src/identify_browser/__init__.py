import re
from typing import TypedDict

from ua_parser import user_agent_parser  # type: ignore

CH_UA_RE = re.compile(r'"([^"]+)";v="([^"]+)"')
NOT_A_BRAND_RE = re.compile(r"Not.A.Brand")


class BrowserIdentityDict(TypedDict):
    name: str
    version: str
    platform: str


def identify_browser(
    user_agent: str, sec_ch_ua: str = "", sec_ch_ua_platform: str = '"Unknown"'
) -> BrowserIdentityDict:
    browsers_and_versions = [
        (x.group(1), x.group(2)) for x in re.finditer(CH_UA_RE, sec_ch_ua)
    ]

    found = None
    chromium_version = None
    for browser_and_version in browsers_and_versions:
        if (
            re.search(NOT_A_BRAND_RE, browser_and_version[0])
            or browser_and_version[0] == "Android WebView"
        ):
            continue

        if browser_and_version[0] == "Chromium":
            chromium_version = browser_and_version[1]
            continue

        found = browser_and_version
        break

    if found is not None:
        name = found[0]
        version = found[1]

        if name == "OperaMobile":
            name = "Opera Mobile"

        return {
            "name": name,
            "version": version,
            "platform": sec_ch_ua_platform[1:-1],
        }

    if chromium_version is not None:
        aloha = re.search(r"AlohaBrowser/(\d+)", user_agent)

        if aloha:
            return {
                "name": "Aloha",
                "version": aloha.group(1),
                "platform": sec_ch_ua_platform[1:-1],
            }

        ecosia = re.search(r"Ecosia android@(\d+)", user_agent)

        if ecosia:
            return {
                "name": "Ecosia",
                "version": ecosia.group(1),
                "platform": sec_ch_ua_platform[1:-1],
            }

        hola = re.search(r"HiBrowser/v(\d+)", user_agent)

        if hola:
            return {
                "name": "Hola",
                "version": hola.group(1),
                "platform": sec_ch_ua_platform[1:-1],
            }

        opera_gx = re.search(r"OPX/(\d+)", user_agent)

        if opera_gx:
            return {
                "name": "Opera GX",
                "version": opera_gx.group(1),
                "platform": sec_ch_ua_platform[1:-1],
            }

    if chromium_version is not None:
        return {
            "name": "Chromium-based browser",
            "version": chromium_version,
            "platform": sec_ch_ua_platform[1:-1],
        }

    parsed_string = user_agent_parser.Parse(user_agent)
    name = parsed_string["user_agent"]["family"]
    version = parsed_string["user_agent"]["major"]
    platform = parsed_string["os"]["family"]

    if name in (
        "Chrome",
        "Chrome Mobile",
        "Chrome Mobile iOS",
        "Chrome Mobile WebView",
    ):
        name = "Google Chrome"
    elif name in ("Edge", "Edge Mobile"):
        name = "Microsoft Edge"
    elif name in ("Firefox iOS", "Firefox Mobile"):
        name = "Firefox"
    elif name == "Mobile Safari":
        name = "Safari"

    if platform == "Mac OS X":
        platform = "macOS"

    if platform == "Android":
        if name == "Firefox":
            ghostery = re.search(r"Ghostery:(\d+)", user_agent)

            if ghostery:
                name = "Ghostery"
                version = ghostery.group(1)
        elif name == "MiuiBrowser":
            name = "Mi Browser"
    elif platform == "iOS":
        if name == "Safari":
            aloha = re.search(r"AlohaBrowser/(\d+)", user_agent)

            if aloha:
                name = "Aloha"
                version = aloha.group(1)
            else:
                duckduckgo = re.search(r"Ddg/(\d+)", user_agent)

                if duckduckgo:
                    name = "DuckDuckGo"
                    version = duckduckgo.group(1)
                else:
                    ecosia = re.search(r"Ecosia ios@(\d+)", user_agent)

                    if ecosia:
                        name = "Ecosia"
                        version = ecosia.group(1)
                    elif "Ghostery Private Browser" in user_agent:
                        name = "Ghostery"
                    else:
                        opera = re.search(r"OPT/(\d+)", user_agent)

                        if opera:
                            name = "Opera"
                            version = opera.group(1)
                        else:
                            opera_gx = re.search(r"OPX/(\d+)", user_agent)

                            if opera_gx:
                                name = "Opera GX"
                                version = opera_gx.group(1)
        elif name == "Mobile Safari UI/WKWebView":
            avast = re.search(r"AvastSecureBrowser/(\d+)", user_agent)

            if avast:
                name = "Avast Secure Browser"
                version = avast.group(1)
    elif platform == "macOS":
        if name == "Safari":
            duckduckgo = re.search(r"Ddg/(\d+)", user_agent)

            if duckduckgo:
                name = "DuckDuckGo"
                version = duckduckgo.group(1)

    return {
        "name": name,
        "version": version,
        "platform": platform,
    }
