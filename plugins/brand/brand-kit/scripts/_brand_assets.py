"""_brand_assets.py - shared image allowlist and resolver for build-doc-pdf.py
and build-deck.py.

Both scripts embed local image files as base64 data URIs. This module provides
a single source of truth for:
  - Recognised image extensions and their MIME types
  - Allowlisted root directories
  - The resolve_local_image() helper used by both callers

Import as:
    from _brand_assets import IMAGE_EXTS, IMAGE_MIME, resolve_local_image
"""

import base64
import pathlib

IMAGE_EXTS = {'jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'}

IMAGE_MIME = {
    'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'svg': 'image/svg+xml',
    'webp': 'image/webp',
}

# /tmp (resolved) - a common scratch location for generated/extracted images
_TMP = pathlib.Path('/tmp').resolve()


def _kit_root_from_caller(caller_file: str) -> pathlib.Path:
    """Walk up from the calling script's location to the brand-kit root.

    Scripts live at <brand-kit>/scripts/<script>.py, so the kit root is two
    levels up.
    """
    return pathlib.Path(caller_file).resolve().parent.parent


def make_allowed_roots(caller_file: str) -> tuple:
    """Return the tuple of allowlisted Path roots for a given caller script.

    Both /tmp (resolved, handles macOS symlink /tmp -> /private/tmp) and the
    brand-kit root are allowed so that bundled kit assets and generated/
    extracted images can both be embedded.
    """
    return (_TMP, _kit_root_from_caller(caller_file))


def pick_browser_channel():
    """Return a Playwright launch channel for a system browser, or None.

    Fallback for when Playwright's bundled Chromium isn't installed and can't
    be downloaded (some networks block the Playwright CDN). Chrome and Edge
    are both Chromium, so rendering output is identical.
    """
    import shutil
    candidates = (
        ('chrome', ('/Applications/Google Chrome.app',
                    'google-chrome', 'google-chrome-stable')),
        ('msedge', ('/Applications/Microsoft Edge.app', 'microsoft-edge')),
    )
    for channel, probes in candidates:
        for probe in probes:
            if pathlib.Path(probe).exists() or shutil.which(probe):
                return channel
    return None


def resolve_local_image(src: str, allowed_roots: tuple) -> str:
    """Resolve a local file path to a base64 data URI.

    Returns an empty string if:
      - src is already a data: or http URL (caller should handle those)
      - the extension is not in IMAGE_EXTS
      - the resolved path is outside all allowed_roots
      - the file does not exist

    Uses resolved paths throughout to handle OS-level symlinks correctly
    (e.g. macOS /tmp -> /private/tmp).
    """
    if src.startswith('data:') or src.startswith('http'):
        return ''
    path = pathlib.Path(src).resolve()
    ext = path.suffix.lower().lstrip('.')
    if ext not in IMAGE_EXTS:
        return ''
    if not any(path.is_relative_to(root.resolve()) for root in allowed_roots):
        return ''
    if not path.exists():
        return ''
    mime = IMAGE_MIME[ext]
    data = base64.b64encode(path.read_bytes()).decode()
    return f'data:{mime};base64,{data}'
