# Nyx

A night-sky theme for [T3 Code](https://t3.codes). The background is a starry sky with a purple aurora, drawn as tiny glowing dots like an LED screen. Menus and panels stay see-through like the default T3 look.

This is a fork of [Nyx](https://github.com/Deepusleepy/t3-nyx-theme) with my personal changes: T3's Nightly night sky in the sidebar header and on a glassy send button, a model picker laid out like [T3 Clawd](https://github.com/rohit3a/t3-clawd)'s, an icon-only access button, no T3 logo on the new thread screen, and easier-to-read chat cards. The screenshots below are from the original Nyx.

![New thread](previews/new-thread.png)
![A conversation](previews/thread.png)
![Model picker](previews/model-picker.png)
![Side panel](previews/side-panel.png)
![Pull requests](previews/pull-requests.png)
![Usage](previews/usage.png)
![Settings](previews/settings.png)

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/coledeb/t3-nyx-theme/main/nyx.json -o nyx.json
t3 theme set nyx.json
```

T3 switches to Nyx right away, in the desktop app and in the browser. To go back, pick another theme in the theme picker or run `t3 theme set t3-chat`.

### Let your agent install it

Paste this into a T3 Code thread:

> Install the Nyx theme from https://github.com/coledeb/t3-nyx-theme. Follow the "Instructions for agents" section of its README.

### Instructions for agents

1. Download `https://raw.githubusercontent.com/coledeb/t3-nyx-theme/main/nyx.json`.
2. If the `t3` command is available, run `t3 theme set <path to nyx.json>`.
3. Otherwise call the `t3_theme_set` tool with `themeId: "nyx"` and the file's JSON as `theme`.
4. Do not edit the file.

## Requirements

- A recent T3 Code Nightly (November 2026 or later).
- Works in the desktop app and the browser. The phone app doesn't use themes.

## Notes

- Nyx is dark only. It keeps T3 dark even when your computer is in light mode.
- The see-through look follows the Glass opacity slider in Settings › Appearance. It looks best at around 40%, which is what the screenshots use.
- The sky fills the window at any size.
- If a future T3 update changes its layout, a few small touches may fall back to T3's normal look. Nothing breaks.

## Change the theme yourself

`theme.css` holds the styles, `art.py` draws the sky, `send-orb.svg` and `sidebar-sky.svg` are the Nightly artwork for the send button and sidebar header, and `build.py` puts them together into `nyx.json`.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
```

## Credits

- [Nyx](https://github.com/Deepusleepy/t3-nyx-theme) by Deepusleepy, the original theme this fork builds on.
- [T3 Clawd](https://github.com/rohit3a/t3-clawd) by rohit3a, whose model picker layout this fork adapts.
- The send button and sidebar sky recreate the Nightly artwork from [T3 Code](https://t3.codes).

## License

[MIT](LICENSE)
