#!/usr/bin/env python3
"""Render a validated design-token proposal JSON file as one review HTML page.

The page reuses the stylesheet, localized chrome strings, and behavior script
from assets/token-proposal-template.html, so hand-filled and rendered pages
share one design. Invalid proposals are not rendered.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any

# Import the sibling validator without leaving bytecode in installed skill folders.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_token_proposal import (  # noqa: E402
    FOUNDATIONS,
    TYPE_FIELDS,
    UNKNOWN,
    contrast_ratio,
    die,
    read_json,
    resolve_color,
    validate,
    validate_html,
)

# Keep UTF-8 output stable on Windows consoles with legacy code pages.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "token-proposal-template.html"
SHELL = re.compile(r"<!-- shell:start -->.*?<!-- shell:end -->", re.S)
STRINGS = re.compile(r'<script type="application/json" id="chrome-strings">(.*?)</script>', re.S)
SECTION_KEYS = {
    "color": ("color_intro", "color_primitives_caption", "color_semantic_caption"),
    "typography": ("typography_intro", "type_primitives_caption", "type_semantic_caption"),
    "spacing": ("spacing_intro", "space_primitives_caption", "space_semantic_caption"),
    "layout": ("layout_intro", "layout_primitives_caption", "layout_semantic_caption"),
    "radius": ("radius_intro", "radius_primitives_caption", "radius_semantic_caption"),
}


class Page:
    """Small helpers that turn proposal data into escaped markup."""

    def __init__(self, data: dict[str, Any], strings: dict[str, str], report: dict[str, Any]) -> None:
        self.data = data
        self.s = strings
        self.report = report
        self.foundations = data["foundations"]
        self.primitives: dict[str, Any] = {}
        self.semantic: dict[str, dict[str, Any]] = {}
        for foundation in FOUNDATIONS:
            block = self.foundations.get(foundation) or {}
            for item in block.get("primitives", []):
                self.primitives[item["name"]] = item.get("value")
            for item in block.get("semantic", []):
                self.semantic[item["name"]] = item

    def t(self, key: str) -> str:
        return escape(self.s.get(key, key))

    def unknown(self) -> str:
        return f'<span class="unknown">{self.t("unknown")}</span>'

    def value(self, value: Any) -> str:
        if value in (None, "", UNKNOWN):
            return self.unknown()
        return escape(str(value))

    @staticmethod
    def style(**properties: Any) -> str:
        """Inline custom properties for known values only; values were validated as safe."""
        parts = [
            f"--{name.replace('_', '-')}: {value}"
            for name, value in properties.items()
            if isinstance(value, str) and value and value != UNKNOWN
        ]
        return escape("; ".join(parts), quote=True)

    def evidence(self, items: list[str] | None) -> str:
        if not items:
            return self.unknown()
        return "<br>".join(escape(item) for item in items)

    def listing(self, items: list[str] | None) -> str:
        if not items:
            return f'<span class="muted-small">{self.t("none")}</span>'
        return ", ".join(escape(item) for item in items)

    def status(self, status: str) -> str:
        return self.t(f"status_{status}")

    @staticmethod
    def context_columns(items: list[dict[str, Any]]) -> list[str]:
        """Ordered union of reference contexts, shown as one column each."""
        columns: list[str] = []
        for item in items:
            for context in item.get("references", {}):
                if context not in columns:
                    columns.append(context)
        return columns

    def ref(self, target: str | None, context: str, swatch: bool = False) -> str:
        if target is None:
            return '<span class="muted-small">—</span>'
        if target == UNKNOWN:
            return self.unknown()
        dark = " is-dark" if "dark" in context.lower() else ""
        chip = ""
        color = self.primitives.get(target)
        if swatch and isinstance(color, str) and color != UNKNOWN:
            chip = f'<span class="chip" style="{self.style(token_value=color)}" aria-hidden="true"></span>'
        return f'<span class="ref{dark}">{chip}{escape(target)}</span>'

    def ref_cells(self, item: dict[str, Any], columns: list[str], swatch: bool = False) -> str:
        references = item["references"]
        if list(references) == ["default"] and len(columns) > 1:
            # A default-only mapping applies in every context; span the columns instead of implying gaps.
            return f'<td colspan="{len(columns)}">{self.ref(references["default"], "default", swatch)}</td>'
        return "".join(f"<td>{self.ref(references.get(column), column, swatch)}</td>" for column in columns)

    def role(self, item: dict[str, Any]) -> str:
        notes = ""
        if item.get("owner"):
            notes += f'<p class="muted-small">{self.t("th_owner")}: {escape(item["owner"])}</p>'
        if item.get("usage"):
            notes += f'<p class="muted-small">{escape(item["usage"])}</p>'
        return f'<td class="role"><p>{escape(item["role"])}</p>{notes}<p class="tag">{self.status(item["status"])}</p></td>'

    def table(self, ident: str, caption_key: str, headers: list[str], rows: list[str]) -> str:
        # Header keys are chrome strings; "=" marks literal text such as a context name.
        head = "".join(
            f'<th scope="col">{escape(key[1:]) if key.startswith("=") else self.t(key)}</th>' for key in headers
        )
        return (
            f'<div class="table-wrap" role="region" aria-labelledby="{ident}-caption" tabindex="0">'
            f'<table><caption id="{ident}-caption">{self.t(caption_key)}</caption>'
            f"<thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
        )

    def sub(self, title_key: str, body: str, note_key: str | None = None) -> str:
        note = f"<p>{self.t(note_key)}</p>" if note_key else ""
        return f'<div class="sub"><h3>{self.t(title_key)}</h3>{note}{body}</div>'

    # Sections -----------------------------------------------------------

    def overview(self) -> str:
        model = (
            '<figure class="stage"><ol class="model">'
            f'<li><strong>{self.t("model_primitive")}</strong><span>{self.t("model_primitive_desc")}</span></li>'
            f'<li><strong>{self.t("model_semantic")}</strong><span>{self.t("model_semantic_desc")}</span></li>'
            f'<li><strong>{self.t("model_component")}</strong><span>{self.t("model_component_desc")}</span></li>'
            "</ol></figure>"
        )
        parts = [
            f'<h2 id="overview-title">{self.t("model_title")}</h2>',
            f'<p>{self.t("model_intro")}</p>',
            model,
        ]
        naming = self.data.get("naming") or {}
        figures = []
        for kind in ("primitive", "semantic"):
            spec = naming.get(kind)
            if not spec:
                continue
            separator = escape(spec.get("separator", "-"))
            pieces = []
            for index, part in enumerate(spec["parts"]):
                if index:
                    pieces.append(f'<span class="anatomy-sep" aria-hidden="true">{separator}</span>')
                pieces.append(
                    f'<div class="anatomy-part"><span class="anatomy-text">{escape(part["text"])}</span>'
                    f'<span class="anatomy-label">{escape(part["label"])}</span></div>'
                )
            figures.append(
                f'<figure class="stage"><div class="anatomy" role="group" aria-labelledby="anatomy-{kind}-label">'
                f'{"".join(pieces)}</div><figcaption id="anatomy-{kind}-label" class="muted-small">'
                f'{self.t("anatomy_" + kind)}</figcaption></figure>'
            )
        if figures:
            parts.append(
                f'<div class="sub"><h3>{self.t("naming_title")}</h3><p>{self.t("naming_intro")}</p>{"".join(figures)}</div>'
            )
        stats = []
        for foundation, counts in self.report["foundation_counts"].items():
            if foundation == "layout" or not counts["primitives"]:
                continue
            stats.append(
                f'<div class="stat"><dt>{self.t(foundation)}</dt>'
                f'<dd>{counts["current_values"]} → {counts["primitives"]}</dd></div>'
            )
        if stats:
            parts.append(
                f'<div class="sub"><h3>{self.t("summary_title")}</h3><dl class="stats">{"".join(stats)}</dl>'
                f'<p class="muted-small">{self.t("stats_note")}</p></div>'
            )
        return self.section("overview", "".join(parts), titled=False)

    def section(self, ident: str, body: str, titled: bool = True) -> str:
        heading = ""
        if titled:
            intro_key = SECTION_KEYS[ident][0] if ident in SECTION_KEYS else f"{ident}_intro"
            heading = f'<h2 id="{ident}-title">{self.t(ident)}</h2><p>{self.t(intro_key)}</p>'
        return f'<section id="{ident}" class="doc-section" aria-labelledby="{ident}-title">{heading}{body}</section>'

    def primitive_rows(self, foundation: str, preview_class: str | None) -> list[str]:
        rows = []
        for item in self.foundations[foundation].get("primitives", []):
            value = item.get("value")
            preview = ""
            if preview_class:
                inner = ""
                if value != UNKNOWN:
                    inner = f'<span class="{preview_class}" style="{self.style(token_value=value)}" aria-hidden="true"></span>'
                preview = f'<td class="preview">{inner}</td>'
            rows.append(
                f'<tr><th scope="row"><code class="token">{escape(item["name"])}</code></th>{preview}'
                f'<td class="value">{self.value(value)}</td>'
                f'<td class="value">{self.listing(item.get("current_values"))}</td>'
                f'<td class="evidence">{self.evidence(item.get("evidence"))}</td></tr>'
            )
        return rows

    def semantic_table(self, foundation: str, ident: str, caption_key: str, extra: str | None = None) -> str:
        items = self.foundations[foundation].get("semantic", [])
        columns = self.context_columns(items)
        headers = ["th_name"] + [f"={column}" for column in columns]
        if extra == "relationship":
            headers.append("th_relationship")
        headers.append("th_role")
        rows = []
        for item in items:
            cells = self.ref_cells(item, columns)
            if extra == "relationship":
                cells += f'<td>{self.t("relationship_" + item.get("relationship", ""))}</td>'
            rows.append(f'<tr><th scope="row"><code class="token">{escape(item["name"])}</code></th>{cells}{self.role(item)}</tr>')
        return self.table(ident, caption_key, headers, rows)

    def color(self) -> str:
        block = self.foundations["color"]
        groups: dict[str, list[dict[str, Any]]] = {}
        for item in block.get("primitives", []):
            group = item.get("group") or item["name"].rsplit("-", 1)[0]
            groups.setdefault(group, []).append(item)
        ramps = []
        for group, items in groups.items():
            steps = []
            for item in items:
                value = item.get("value")
                step = item.get("step") or item["name"].rsplit("-", 1)[-1]
                state = " is-unknown" if value == UNKNOWN else ""
                style = f' style="{self.style(token_value=value)}"' if value != UNKNOWN else ""
                label = self.t("unknown") if value == UNKNOWN else escape(str(value))
                steps.append(f'<li class="ramp-step{state}"{style}><strong>{escape(str(step))}</strong><span>{label}</span></li>')
            ramps.append(
                f'<div class="ramp-group"><h4>{escape(group)}</h4>'
                f'<ol class="ramp" aria-label="{escape(group, quote=True)}">{"".join(steps)}</ol></div>'
            )
        primitives = "".join(ramps) + self.table(
            "color-primitives", "color_primitives_caption",
            ["th_name", "th_value", "th_consolidates", "th_evidence"],
            self.primitive_rows("color", None),
        )
        contrast = {item["token"]: item for item in self.report["contrast"]}
        color_primitives = {
            item["name"]: item.get("value") for item in block.get("primitives", [])
        }
        color_semantic = {item["name"]: item for item in block.get("semantic", [])}
        items = block.get("semantic", [])
        columns = self.context_columns(items)
        rows = []
        for item in items:
            check = contrast.get(item["name"])
            cell = '<span class="muted-small">—</span>'
            if check:
                if check["status"] == "unknown":
                    cell = self.unknown()
                else:
                    foreground = resolve_color(item["name"], color_primitives, color_semantic)
                    background = resolve_color(check["against"], color_primitives, color_semantic)
                    verdict = self.t("contrast_pass") if check["status"] == "pass" else self.t("contrast_fail")
                    cell = (
                        f'<span class="pair" style="{self.style(token_fg=foreground, token_bg=background)}" aria-hidden="true">Aa 가 あ</span>'
                        f'<p class="value">{contrast_ratio(foreground, background)}:1 · ≥ {check["minimum"]} {verdict}</p>'
                        f'<p class="muted-small">{escape(check["against"])}</p>'
                    )
            refs = self.ref_cells(item, columns, swatch=True)
            rows.append(
                f'<tr><th scope="row"><code class="token">{escape(item["name"])}</code></th>{refs}'
                f'<td>{cell}</td>{self.role(item)}</tr>'
            )
        semantic = self.table(
            "color-semantic", "color_semantic_caption",
            ["th_name"] + [f"={column}" for column in columns] + ["th_contrast", "th_role"], rows,
        )
        return self.section("color", self.sub("primitives", primitives) + self.sub("semantic", semantic))

    def typography(self) -> str:
        block = self.foundations["typography"]
        default_text = self.data.get("specimen_text") or self.s.get("specimen_text", "")
        rows = []
        for item in block.get("primitives", []):
            value = item.get("value") or {}
            style = self.style(**{f"token_{field}": value.get(field) for field in TYPE_FIELDS})
            order = ("font_size", "font_weight", "line_height", "letter_spacing", "font_family")
            values = "".join(
                f'<div><dt>{self.t(field)}</dt><dd>{self.value(value.get(field))}</dd></div>' for field in order
            )
            specimen = escape(item.get("specimen") or default_text)
            rows.append(
                f'<tr><th scope="row"><code class="token">{escape(item["name"])}</code>'
                f'<p class="muted-small">{self.evidence(item.get("evidence"))}</p></th>'
                f'<td><p class="specimen" style="{style}">{specimen}</p><dl class="type-values">{values}</dl></td></tr>'
            )
        primitives = self.table(
            "type-primitives", "type_primitives_caption", ["th_name", "th_specimen"], rows,
        )
        semantic = self.semantic_table("typography", "type-semantic", "type_semantic_caption")
        return self.section("typography", self.sub("primitives", primitives) + self.sub("semantic", semantic))

    def spacing(self) -> str:
        primitives = self.table(
            "space-primitives", "space_primitives_caption",
            ["th_name", "th_preview", "th_value", "th_consolidates", "th_evidence"],
            self.primitive_rows("spacing", "space-bar"),
        )
        semantic = self.semantic_table("spacing", "space-semantic", "space_semantic_caption")
        return self.section(
            "spacing", self.sub("primitives", primitives, "space_note") + self.sub("semantic", semantic),
        )

    def layout(self) -> str:
        block = self.foundations["layout"]
        body = ""
        frames = []
        diagram = {item.get("diagram"): item for item in block.get("semantic", []) if item.get("diagram")}
        for breakpoint in self.data.get("breakpoints", []):
            name = breakpoint["name"]

            def resolve(kind: str) -> str:
                item = diagram.get(kind)
                if not item:
                    return self.unknown()
                target = item["references"].get(name) or item["references"].get("default")
                value = self.primitives.get(target) if target and target != UNKNOWN else None
                return self.value(value)

            frames.append(
                '<figure class="frame"><div class="frame-canvas"><div class="frame-content">'
                f'{self.t("frame_width")} {resolve("content-width")}</div></div>'
                f'<figcaption><strong>{escape(name)} · {self.value(breakpoint.get("min_width"))}</strong>'
                f'{self.t("frame_padding")} {resolve("page-padding")}</figcaption></figure>'
            )
        if frames:
            body += self.sub("breakpoints", f'<div class="frames">{"".join(frames)}</div>')
        if block.get("primitives"):
            body += self.sub("primitives", self.table(
                "layout-primitives", "layout_primitives_caption",
                ["th_name", "th_value", "th_consolidates", "th_evidence"],
                self.primitive_rows("layout", None),
            ))
        body += self.sub("semantic", self.semantic_table("layout", "layout-semantic", "layout_semantic_caption", "owner"))
        return self.section("layout", body)

    def radius(self) -> str:
        primitives = self.table(
            "radius-primitives", "radius_primitives_caption",
            ["th_name", "th_preview", "th_value", "th_consolidates", "th_evidence"],
            self.primitive_rows("radius", "radius-corner"),
        )
        semantic = self.semantic_table("radius", "radius-semantic", "radius_semantic_caption", "relationship")
        return self.section("radius", self.sub("primitives", primitives, "radius_note") + self.sub("semantic", semantic))

    def changes(self) -> str:
        rows = []
        for change in self.data.get("changes", []):
            proposed = change.get("proposed")
            target = f'<code class="token">{escape(proposed)}</code>' if proposed else "—"
            rows.append(
                f'<tr><td class="value">{escape(change["current"])}</td><td>{target}</td>'
                f'<td>{self.t("action_" + change["action"])}</td>'
                f'<td class="evidence">{self.evidence(change.get("evidence"))}</td></tr>'
            )
        if not rows:
            rows.append(f'<tr><td colspan="4" class="muted-small">{self.t("none")}</td></tr>')
        table = self.table("changes", "changes_caption", ["th_current", "th_proposed", "th_action", "th_evidence"], rows)
        return self.section("changes", f'<div class="sub">{table}</div>')

    def decisions(self) -> str:
        cards = []
        decisions = self.data.get("decisions", {})
        for group in ("proposed", "retained", "rejected", "open"):
            items = decisions.get(group) or []
            body = "".join(f"<li>{escape(item)}</li>" for item in items) or f'<li>{self.t("none")}</li>'
            cards.append(f'<div class="decision"><h3 class="tag">{self.t("decision_" + group)}</h3><ul>{body}</ul></div>')
        return self.section("decisions", f'<div class="sub decisions">{"".join(cards)}</div>')

    def shell(self) -> str:
        order = ["overview"] + [name for name in FOUNDATIONS if name in self.foundations] + ["changes", "decisions"]
        nav = "".join(f'<li><a href="#{name}">{self.t(name)}</a></li>' for name in order)
        sections = [self.overview()] + [getattr(self, name)() for name in FOUNDATIONS if name in self.foundations]
        sections += [self.changes(), self.decisions()]
        data = self.data
        basis = "<br>".join(escape(item) for item in data["evidence_basis"])
        return f"""<!-- shell:start -->
  <a class="skip-link" href="#content">{self.t("skip")}</a>
  <div class="app">
    <aside class="sidebar">
      <div class="brand">
        <strong>{escape(data["project"])}</strong>
        <span>{self.t("brand_suffix")}</span>
        <span class="badge">{self.t("status_badge")}</span>
      </div>
      <nav class="nav" aria-labelledby="nav-label">
        <p id="nav-label" class="nav-group">{self.t("nav_label")}</p>
        <ul>{nav}</ul>
      </nav>
    </aside>
    <main id="content" class="panel" tabindex="-1">
      <div class="doc">
        <header class="intro">
          <p class="eyebrow">{self.t("breadcrumb")}</p>
          <h1>{escape(data["title"])}</h1>
          <p class="lede">{escape(data["summary"])}</p>
          <dl class="meta">
            <div><dt>{self.t("meta_basis")}</dt><dd>{basis}</dd></div>
            <div><dt>{self.t("meta_prepared")}</dt><dd>{escape(data["prepared"])}</dd></div>
            <div><dt>{self.t("meta_status")}</dt><dd>{self.t("status_value")}</dd></div>
          </dl>
          <div class="notice"><strong>{self.t("boundary_title")}</strong><p>{self.t("boundary_text")}</p></div>
        </header>
        {"".join(sections)}
        <footer class="doc-footer">{self.t("footer")}</footer>
      </div>
    </main>
  </div>
  <!-- shell:end -->"""


def render(data: dict[str, Any], template: str, report: dict[str, Any]) -> str:
    match = STRINGS.search(template)
    if not match:
        die("template is missing the chrome-strings JSON block")
    catalog = json.loads(match.group(1))
    language = data["language"].lower().split("-")[0]
    strings = catalog.get(language, catalog["en"])
    page = Page(data, strings, report)
    html = SHELL.sub(lambda _: page.shell(), template, count=1)
    html = html.replace("{{DOCUMENT_LANGUAGE}}", escape(data["language"], quote=True), 1)
    html = html.replace("{{DOCUMENT_TITLE}}", escape(data["title"]), 1)
    # The hand-fill instructions mention placeholders; the rendered page does not need them.
    html = re.sub(r"\n  <!--\n    Manual fill:.*?-->", "", html, count=1, flags=re.S)
    return html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a design-token proposal JSON file as one HTML page.")
    parser.add_argument("input", type=Path, help="Path to token proposal JSON")
    parser.add_argument("--output", type=Path, required=True, help="HTML file to write")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="Template providing styles and strings")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = read_json(args.input)
    report = validate(data)
    if not report["valid"]:
        sys.stdout.write(json.dumps({"rendered": False, "proposal": report}, ensure_ascii=False, indent=2) + "\n")
        return 1
    try:
        template = args.template.read_text(encoding="utf-8")
    except FileNotFoundError:
        die(f"template not found: {args.template}")
    html = render(data, template, report)
    page_check = validate_html(html)
    if page_check["valid"]:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding="utf-8")
    result = {
        "rendered": page_check["valid"],
        "output": str(args.output) if page_check["valid"] else None,
        "unknown_values": report["unknown_values"],
        "warnings": report["warnings"],
        "html": page_check,
    }
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return 0 if page_check["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
