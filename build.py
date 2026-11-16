import json
import re
import sys
from pathlib import Path

from art import build_art_data_url

ROOT = Path(__file__).parent
THEME_ID = "nyx"
THEME_NAME = "Nyx"
CSS_LIMIT = 50_000

COLORS = {
    "canvas": "#000000",
    "chrome": "#000000",
    "toolbar": "#000000",
    "sidebar": "#000000",
    "sidebarBorder": "#16161d",
    "border": "#1f1f27",
    "accent": "#8a7fe8",
    "accentForeground": "#06061a",
    "focus": "#8a7fe8",
    "surface": "#0d0c20",
    "surfaceRaised": "#110f2a",
    "surfaceOverlay": "#0c0b1c",
    "input": "#24224a",
    "messageSurface": "#1e1b48",
    "messageAction": "#7f78e6",
    "messageActionForeground": "#ffffff",
    "messageActionHover": "#948df0",
    "update": "#8a7fe8",
    "updateForeground": "#b4aaff",
    "updateSurface": "#17152e",
    "muted": "#1a1840",
    "secondary": "#16143a",
    "secondaryForeground": "#f1f0ff",
    "mutedForeground": "#a6a3c0",
    "secondaryLabel": "#a6a3c0",
    "sidebarMutedForeground": "#9d9ab8",
    "sidebarControlSurface": "#000000",
    "codeBackground": "#08071a",
    "terminalBackground": "#06051a",
    "terminalCursor": "#b4aaff",
    "terminalSelection": "#2a2660",
}


SHORT_VARIABLES = {
    "--nyx-key-glow": "--kg",
    "--nyx-key-rim": "--kr",
    "--nyx-key": "--k",
    "--nyx-art-width": "--w",
    "--nyx-sheen-edge": "--s",
    "--nyx-grid": "--g",
    "--nyx-dot": "--d",
    "--nyx-art": "--a",
}


def minify(css: str) -> str:
    strings: list[str] = []

    def stash(match: re.Match) -> str:
        strings.append(match.group(0))
        return f"\x00{len(strings) - 1}\x00"

    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r'="([A-Za-z_][\w-]*)"\]', r"=\1]", css)
    css = re.sub(r'"[^"]*"', stash, css)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    # A space before `:` is a descendant combinator in selectors (`.dark :has(...)`), so keep it.
    css = re.sub(r":\s+", ":", css)
    css = re.sub(r"\s*!important", "!important", css)
    css = css.replace(";}", "}")
    css = re.sub(r"\btransparent\b", "#0000", css)
    css = re.sub(r"(?<![\w.])0\.(\d)", r".\1", css)
    for long_name in sorted(SHORT_VARIABLES, key=len, reverse=True):
        css = css.replace(long_name, SHORT_VARIABLES[long_name])
    css = re.sub(r"\x00(\d+)\x00", lambda m: strings[int(m.group(1))], css)
    return css.strip()


def split_rules(css: str) -> list[tuple[str, str]]:
    rules, depth, start, brace = [], 0, 0, 0
    for i, ch in enumerate(css):
        if ch == "{":
            if depth == 0:
                brace = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                rules.append((css[start:brace], css[brace + 1 : i]))
                start = i + 1
    return rules


def nest_dark(css: str) -> str:
    """Fold runs of `.dark X` rules into one nested `.dark{X{...}}` block."""
    out, run = [], []

    def flush() -> None:
        if run:
            out.append(".dark{" + "".join(run) + "}")
            run.clear()

    for selector, body in split_rules(css):
        parts = selector.split(",")
        if all(p.startswith(".dark ") for p in parts):
            # `&` keeps selectors like `:has(...)` from being read as declarations.
            run.append(",".join("& " + p[6:] for p in parts) + "{" + body + "}")
        else:
            flush()
            out.append(selector + "{" + body + "}")
    flush()
    return "".join(out)


def svg_data_url(path: Path) -> str:
    svg = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
    svg = re.sub(r">\s+<", "><", svg).strip().replace('"', "'")
    for ch, code in (("%", "%25"), ("#", "%23"), ("<", "%3C"), (">", "%3E")):
        svg = svg.replace(ch, code)
    return f'"data:image/svg+xml,{svg}"'


def build() -> dict:
    css = nest_dark(minify((ROOT / "theme.css").read_text()))
    css = css.replace("__ART__", build_art_data_url())
    css = css.replace("__ORB__", svg_data_url(ROOT / "send-orb.svg"))
    css = css.replace("__SKY__", svg_data_url(ROOT / "sidebar-sky.svg"))
    if len(css) > CSS_LIMIT:
        sys.exit(f"theme css is {len(css)} characters; T3 accepts at most {CSS_LIMIT}")
    return {"version": 1, "name": THEME_NAME, "appearance": "dark", "colors": COLORS, "css": css}


if __name__ == "__main__":
    theme = build()
    out = ROOT / f"{THEME_ID}.json"
    out.write_text(json.dumps(theme, indent=2) + "\n")
    print(f"{out.name}: {len(theme['css'])} css characters")
