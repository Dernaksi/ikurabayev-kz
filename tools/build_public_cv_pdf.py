#!/usr/bin/env python3
"""Build deterministic RU/EN PDF CV exports and their provenance manifest."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from io import BytesIO
from pathlib import Path

try:
    import pypdf
    import reportlab
    from pypdf import PdfReader
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        KeepTogether,
        PageTemplate,
        Paragraph,
        Spacer,
    )
except ImportError as exc:  # pragma: no cover - environment-dependent failure path
    raise SystemExit(
        "PDF generation requires the approved offline reportlab and pypdf runtime: "
        f"{exc}"
    ) from exc

import build_public_cv as cv_builder


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "public-facts.json"
GRAPH_PATH = ROOT / "data" / "public-research-graph.json"
RU_PDF_PATH = ROOT / "site" / "output" / "pdf" / "IKurabayev_Public_CV_RU.pdf"
EN_PDF_PATH = ROOT / "site" / "output" / "pdf" / "IKurabayev_Public_CV_EN.pdf"
PROVENANCE_PATH = ROOT / "cv" / "IKurabayev_Public_CV_PDF_PROVENANCE.json"
PDF_PATHS = {
    "cv.pdf.ru": "site/output/pdf/IKurabayev_Public_CV_RU.pdf",
    "cv.pdf.en": "site/output/pdf/IKurabayev_Public_CV_EN.pdf",
}
BUNDLED_FONT_DIR = (
    Path(sys.executable).resolve().parents[1]
    / "native"
    / "poppler"
    / "Library"
    / "share"
    / "fonts"
)
FONT_CANDIDATES = (
    (BUNDLED_FONT_DIR / "Ubuntu-R.ttf", BUNDLED_FONT_DIR / "Ubuntu-B.ttf"),
    (
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf"),
    ),
    (
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ),
    (
        Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"),
    ),
)
FORBIDDEN_TEXT_PATTERNS = {
    "credential identifier": re.compile(r"KZ55VWE[0-9]{8}", re.IGNORECASE),
    "accreditation identifier": re.compile(r"KZ\.S\.", re.IGNORECASE),
    "12-digit civil identifier": re.compile(r"(?<![A-Za-z0-9])[0-9]{12}(?![A-Za-z0-9])"),
    "private file URL": re.compile(r"file://", re.IGNORECASE),
    "absolute Windows path": re.compile(r"[A-Za-z]:\\"),
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def normalize_pdf_text(value: str) -> str:
    """Use portable punctuation while preserving reviewed wording."""

    return (
        value.replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u00a0", " ")
    )


def resolve_fonts(regular_arg: str | None, bold_arg: str | None) -> tuple[Path, Path]:
    if regular_arg or bold_arg:
        if not regular_arg or not bold_arg:
            raise ValueError("--font-regular and --font-bold must be supplied together")
        regular = Path(regular_arg).resolve()
        bold = Path(bold_arg).resolve()
        if not regular.is_file() or not bold.is_file():
            raise ValueError("explicit font files must exist")
        return regular, bold
    for regular, bold in FONT_CANDIDATES:
        if regular.is_file() and bold.is_file():
            return regular, bold
    raise ValueError(
        "No approved Unicode font pair found; pass --font-regular and --font-bold"
    )


def inline_markup(value: str) -> str:
    """Render the CV's bounded Markdown subset as ReportLab paragraph markup."""

    value = normalize_pdf_text(value[2:] if value.startswith("- ") else value)
    parts: list[str] = []
    offset = 0
    for match in cv_builder.INLINE_PATTERN.finditer(value):
        parts.append(html.escape(value[offset:match.start()]))
        strong = match.group("strong")
        label = match.group("label")
        link = match.group("link")
        bare_url = match.group("url")
        if strong is not None:
            parts.append(f"<b>{html.escape(strong)}</b>")
        elif label is not None and link is not None:
            parts.append(
                f'<link href="{html.escape(link, quote=True)}" color="#087f75">'
                f"{html.escape(label)}</link>"
            )
        elif bare_url is not None:
            escaped = html.escape(bare_url, quote=True)
            parts.append(f'<link href="{escaped}" color="#087f75">{escaped}</link>')
        offset = match.end()
    parts.append(html.escape(value[offset:]))
    return "".join(parts)


class CvPdfTemplate(BaseDocTemplate):
    """A4 document with deterministic metadata, header, and page numbering."""

    def __init__(self, stream: BytesIO, *, language: str, title: str) -> None:
        super().__init__(
            stream,
            pagesize=A4,
            leftMargin=17 * mm,
            rightMargin=17 * mm,
            topMargin=20 * mm,
            bottomMargin=17 * mm,
            title=title,
            author="Iskander Kurabayev",
            subject="Reviewed Living Public CV",
            creator="IKurabayev.kz offline PDF generator v0.1",
            invariant=1,
            pageCompression=1,
        )
        self.language = language
        self.document_title = title
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="content",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="cv", frames=(frame,), onPage=self.draw_page))

    def draw_page(self, page_canvas: canvas.Canvas, _: BaseDocTemplate) -> None:
        width, height = A4
        page_canvas.saveState()
        page_canvas.setTitle(self.document_title)
        page_canvas.setAuthor("Iskander Kurabayev")
        page_canvas.setSubject("Reviewed Living Public CV")
        page_canvas.setCreator("IKurabayev.kz offline PDF generator v0.1")
        page_canvas.setStrokeColor(colors.HexColor("#0f766e"))
        page_canvas.setLineWidth(0.8)
        page_canvas.line(17 * mm, height - 13 * mm, width - 17 * mm, height - 13 * mm)
        page_canvas.setFont("IKSansBold", 7.5)
        page_canvas.setFillColor(colors.HexColor("#0f766e"))
        page_canvas.drawString(17 * mm, height - 10.5 * mm, "IKURABAYEV.KZ")
        page_canvas.setFont("IKSans", 7.5)
        page_canvas.setFillColor(colors.HexColor("#52615f"))
        locale_label = "PUBLIC CV / RU" if self.language == "ru" else "PUBLIC CV / EN"
        page_canvas.drawRightString(width - 17 * mm, height - 10.5 * mm, locale_label)
        footer = (
            f"IKurabayev.kz | {self.language.upper()} | "
            f"{page_canvas.getPageNumber()}"
        )
        page_canvas.setFillColor(colors.HexColor("#687673"))
        page_canvas.setFont("IKSans", 7.2)
        page_canvas.drawCentredString(width / 2, 8.5 * mm, footer)
        page_canvas.restoreState()


def build_styles() -> dict[str, ParagraphStyle]:
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow",
            fontName="IKSansBold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#0f766e"),
            spaceAfter=3 * mm,
        ),
        "title": ParagraphStyle(
            "title",
            fontName="IKSansBold",
            fontSize=23,
            leading=27,
            textColor=colors.HexColor("#12211f"),
            spaceAfter=3 * mm,
        ),
        "lead": ParagraphStyle(
            "lead",
            fontName="IKSans",
            fontSize=10.5,
            leading=14.5,
            textColor=colors.HexColor("#334744"),
            spaceAfter=2.5 * mm,
        ),
        "scope": ParagraphStyle(
            "scope",
            fontName="IKSans",
            fontSize=8.4,
            leading=11.5,
            textColor=colors.HexColor("#63716f"),
            spaceAfter=4 * mm,
        ),
        "reviewed": ParagraphStyle(
            "reviewed",
            fontName="IKSansBold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#0f766e"),
            spaceAfter=6 * mm,
        ),
        "section": ParagraphStyle(
            "section",
            fontName="IKSansBold",
            fontSize=9.2,
            leading=12,
            textColor=colors.HexColor("#0f766e"),
            spaceBefore=3.5 * mm,
            spaceAfter=1.8 * mm,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="IKSans",
            fontSize=8.65,
            leading=12.2,
            leftIndent=4.5 * mm,
            firstLineIndent=-3.2 * mm,
            bulletIndent=0,
            bulletFontName="IKSans",
            bulletFontSize=8.65,
            textColor=colors.HexColor("#253734"),
            alignment=TA_LEFT,
            spaceAfter=1.8 * mm,
            allowWidows=0,
            allowOrphans=0,
        ),
        "source": ParagraphStyle(
            "source",
            fontName="IKSans",
            fontSize=7.7,
            leading=10.5,
            textColor=colors.HexColor("#61706d"),
            spaceBefore=5 * mm,
        ),
    }


def build_story(
    language: str,
    blocks: list[cv_builder.Block],
    review_date: str,
) -> list[object]:
    styles = build_styles()
    if language == "ru":
        title = "Искандер Курабаев - публичное CV"
        lead = "Избранное публичное CV с проверяемым происхождением блоков."
        scope = (
            "Не исчерпывающий список. Частные данные, идентификаторы документов, "
            "метрики цитирования и неподтверждённые сведения исключены."
        )
        review = f"РЕЕСТР ПРОВЕРЕН: {review_date}"
        source = (
            "Источник фактов и связей: публичные JSON-реестры репозитория. "
            "Хеши и происхождение PDF записаны в сопроводительном манифесте; "
            "они не являются юридической или цифровой подписью."
        )
        locale = "LIVING PUBLIC CV / RU"
    else:
        title = "Iskander Kurabayev - Public CV"
        lead = "Selected public CV with traceable block-level provenance."
        scope = (
            "Not an exhaustive record. Private data, document identifiers, citation "
            "metrics, and unsupported claims are excluded."
        )
        review = f"REGISTRY REVIEWED: {review_date}"
        source = (
            "Fact and relationship sources: the repository's public JSON registries. "
            "PDF hashes and provenance are recorded in the companion manifest; they "
            "are not a legal or digital signature."
        )
        locale = "LIVING PUBLIC CV / EN"

    story: list[object] = [
        Spacer(1, 2 * mm),
        Paragraph(locale, styles["eyebrow"]),
        Paragraph(title, styles["title"]),
        Paragraph(lead, styles["lead"]),
        Paragraph(scope, styles["scope"]),
        Paragraph(review, styles["reviewed"]),
    ]
    current_section = ""
    section_flowables: list[object] = []

    def flush_section() -> None:
        if not section_flowables:
            return
        if current_section == "cv.section.patents":
            story.append(KeepTogether(section_flowables.copy()))
        else:
            story.extend(section_flowables)
        section_flowables.clear()

    for block in blocks:
        if block.section_id != current_section:
            flush_section()
            current_section = block.section_id
            heading = normalize_pdf_text(
                cv_builder.SECTION_HEADINGS[language][current_section]
            ).upper()
            section_flowables.append(Paragraph(html.escape(heading), styles["section"]))
        for line in block.lines(language):
            section_flowables.append(
                Paragraph(inline_markup(line), styles["bullet"], bulletText="-")
            )
    flush_section()
    story.extend((Spacer(1, 2 * mm), Paragraph(html.escape(source), styles["source"])))
    return story


def render_pdf(
    language: str,
    blocks: list[cv_builder.Block],
    review_date: str,
) -> bytes:
    title = (
        "Искандер Курабаев - публичное CV"
        if language == "ru"
        else "Iskander Kurabayev - Public CV"
    )
    stream = BytesIO()
    document = CvPdfTemplate(stream, language=language, title=title)
    document.build(
        build_story(language, blocks, review_date),
        canvasmaker=canvas.Canvas,
    )
    return stream.getvalue()


def inspect_pdf(document_id: str, content: bytes, language: str) -> tuple[int, str]:
    try:
        reader = PdfReader(BytesIO(content))
    except Exception as exc:  # pypdf exposes several parser exceptions
        raise ValueError(f"{document_id}: PDF cannot be reopened: {exc}") from exc
    if not 1 <= len(reader.pages) <= 8:
        raise ValueError(f"{document_id}: unexpected page count {len(reader.pages)}")
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    expected = (
        ("Курабаев Искандер Казбекович", "Сертифицированный энергоаудитор")
        if language == "ru"
        else ("Iskander Kurabayev", "Certified energy auditor")
    )
    for marker in (*expected, "2026-08-14", "2029-08-06", "2026-08-23"):
        if marker not in text:
            raise ValueError(f"{document_id}: extracted text marker is missing: {marker}")
    for label, pattern in FORBIDDEN_TEXT_PATTERNS.items():
        if pattern.search(text):
            raise ValueError(f"{document_id}: prohibited {label} found in PDF text")
    link_count = 0
    for page in reader.pages:
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            action = annotation.get("/A")
            uri = action.get("/URI") if action else None
            if not isinstance(uri, str) or not uri.startswith("https://"):
                raise ValueError(f"{document_id}: non-HTTPS or missing link target")
            link_count += 1
    if link_count < 8:
        raise ValueError(f"{document_id}: expected public hyperlinks are missing")
    return len(reader.pages), text


def build_outputs(regular_font: Path, bold_font: Path) -> dict[Path, bytes]:
    pdfmetrics.registerFont(TTFont("IKSans", str(regular_font)))
    pdfmetrics.registerFont(TTFont("IKSansBold", str(bold_font)))
    registry_raw, registry = cv_builder.read_json_bytes(REGISTRY_PATH)
    graph_raw, graph = cv_builder.read_json_bytes(GRAPH_PATH)
    if graph.get("subject") != registry.get("subject", {}).get("id"):
        raise ValueError("graph subject does not match registry subject")
    blocks, _, _ = cv_builder.build_blocks(registry, graph)
    review_date = registry.get("generated_or_reviewed_at")
    if not isinstance(review_date, str):
        raise ValueError("registry review date must be a string")
    ru_pdf = render_pdf("ru", blocks, review_date)
    en_pdf = render_pdf("en", blocks, review_date)
    ru_pages, _ = inspect_pdf("cv.pdf.ru", ru_pdf, "ru")
    en_pages, _ = inspect_pdf("cv.pdf.en", en_pdf, "en")
    section_ids = cv_builder.ordered_unique([block.section_id for block in blocks])
    block_ids = [block.id for block in blocks]
    manifest = {
        "schema_version": "0.1",
        "pdf_cv_version": "0.1",
        "source_registry_sha256": sha256_bytes(registry_raw),
        "source_graph_sha256": sha256_bytes(graph_raw),
        "source_review_date": review_date,
        "hash_scope_note": (
            "SHA-256 values cover exact input, font, and PDF bytes for "
            "reproducibility; they are not a legal or digital signature."
        ),
        "generator": {
            "script": "tools/build_public_cv_pdf.py",
            "reportlab_version": reportlab.Version,
            "pypdf_version": pypdf.__version__,
            "font_regular": {
                "file": regular_font.name,
                "sha256": sha256_bytes(regular_font.read_bytes()),
            },
            "font_bold": {
                "file": bold_font.name,
                "sha256": sha256_bytes(bold_font.read_bytes()),
            },
            "portability_note": (
                "Byte-identical regeneration requires the recorded ReportLab "
                "version and exact font bytes; the deployed PDFs have no runtime dependency."
            ),
        },
        "documents": [
            {
                "id": "cv.pdf.ru",
                "language": "ru",
                "path": PDF_PATHS["cv.pdf.ru"],
                "sha256": sha256_bytes(ru_pdf),
                "page_count": ru_pages,
                "section_ids": section_ids,
                "block_ids": block_ids,
            },
            {
                "id": "cv.pdf.en",
                "language": "en",
                "path": PDF_PATHS["cv.pdf.en"],
                "sha256": sha256_bytes(en_pdf),
                "page_count": en_pages,
                "section_ids": section_ids,
                "block_ids": block_ids,
            },
        ],
        "privacy_note": (
            "Private contacts, credential identifiers, civil identifiers, QR "
            "content, addresses, signatures, seals, photographs, raw documents, "
            "and private paths are excluded."
        ),
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    return {
        RU_PDF_PATH: ru_pdf,
        EN_PDF_PATH: en_pdf,
        PROVENANCE_PATH: manifest_bytes,
    }


def write_outputs(outputs: dict[Path, bytes]) -> int:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        print(f"wrote {path.relative_to(ROOT)} ({len(content)} bytes)")
    return 0


def check_outputs(outputs: dict[Path, bytes]) -> int:
    drift: list[str] = []
    for path, expected in outputs.items():
        try:
            actual = path.read_bytes()
        except OSError:
            drift.append(f"missing {path.relative_to(ROOT)}")
            continue
        if actual != expected:
            drift.append(f"drift in {path.relative_to(ROOT)}")
    if drift:
        print("Public CV PDF generation check FAILED:", file=sys.stderr)
        for item in drift:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("Public CV PDF generation check PASS: both PDFs and manifest are byte-identical.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write PDF artifacts")
    mode.add_argument("--check", action="store_true", help="check PDF artifacts for drift")
    parser.add_argument("--font-regular", help="path to an approved Unicode regular TTF")
    parser.add_argument("--font-bold", help="path to an approved Unicode bold TTF")
    args = parser.parse_args()
    try:
        regular_font, bold_font = resolve_fonts(args.font_regular, args.font_bold)
        outputs = build_outputs(regular_font, bold_font)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"Public CV PDF generation FAILED: {exc}", file=sys.stderr)
        return 1
    return write_outputs(outputs) if args.write else check_outputs(outputs)


if __name__ == "__main__":
    raise SystemExit(main())
