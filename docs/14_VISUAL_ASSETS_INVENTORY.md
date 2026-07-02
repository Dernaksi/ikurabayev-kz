# Visual Assets Inventory v0.6

## Purpose

This document records the controlled review of owner-provided visual assets from
the local `img/` source drop zone. It explains which assets were selected for
the static site, which were excluded, how final web assets were optimized, and
what privacy checks were applied.

This inventory is not a biography source and does not add new substantive
claims about roles, publications, patents, products, metrics, or contact routes.

## Source folder inspected

`C:\Users\Teemo\GitHub\ikurabayev-kz\img`

The folder is treated as a source asset drop zone, not as final website output.
ZIP archives and oversized source PNGs were not copied blindly into
`site/assets/`.

## Source asset inventory

| Source file | Format | Dimensions | Size | Suitability | Likely purpose | Review status |
| --- | --- | ---: | ---: | --- | --- | --- |
| `img/ChatGPT Image 2 июл. 2026 г., 22_39_57.png` | PNG | 1254x1254 | 1.5 MB | Not selected | QR background candidate | Excluded: includes broad marketing wording such as `Global impact`; not needed for the cautious public profile. |
| `img/ChatGPT Image 2 июл. 2026 г., 22_40_08.png` | PNG | 1536x1024 | 1.8 MB | Not selected | Hero / brand background candidate | Excluded: contains stronger promotional wording such as `International Experience` and broad sustainability claims. |
| `img/ChatGPT Image 2 июл. 2026 г., 22_40_18.png` | PNG | 1024x1024 | 1.4 MB | Source reference only | Logo / mark candidate | Excluded from final assets as raster; replaced by a small hand-authored local SVG mark. |
| `img/ChatGPT Image 2 июл. 2026 г., 22_40_27.png` | PNG | 1024x1536 | 2.0 MB | Source reference only | Logo / mark background candidate | Excluded from final assets as oversized and less useful than SVG. |
| `img/ChatGPT Image 2 июл. 2026 г., 22_40_40.png` | PNG | 1536x1024 | 1.8 MB | Selected as source | Neutral Shift Lab background / QR background / OG source | Selected after visual review: no private contact details, document scans, seals, signatures, client/facility identifiers, or unsupported biography claims were visible. |
| `img/method-stack-assets/method-stack.svg` | SVG | 1200x360 | 6.8 KB | Selected | Method stack graphic | Selected; copied as `site/assets/method-stack.svg` with font stack adjusted to system fonts. |
| `img/method-stack-assets/method-stack.png` | PNG | 1200x360 | 80.6 KB | Not selected | Raster preview | Excluded because SVG is smaller and cleaner. |
| `img/method-stack-assets/method-stack-transparent.svg` | SVG | 1200x360 | 6.8 KB | Not selected | Alternate method stack graphic | Excluded as duplicate. |
| `img/method-stack-assets/method-stack-transparent.png` | PNG | 1200x360 | 56.2 KB | Not selected | Raster preview | Excluded because SVG is preferred. |
| `img/method-stack-assets/method-stack-compact.svg` | SVG | 600x760 | 3.4 KB | Not selected | Mobile method stack candidate | Excluded to keep the final asset set small. |
| `img/method-stack-assets/method-stack-compact.png` | PNG | 600x760 | 51.7 KB | Not selected | Raster preview | Excluded because SVG is preferred. |
| `img/ai-energy-auditor-concept-assets/ai-energy-auditor-concept.svg` | SVG | 1600x900 | 9.9 KB | Selected cautiously | AI Energy Auditor concept illustration | Selected for the existing roadmap / concept section; does not claim a launched product. |
| `img/ai-energy-auditor-concept-assets/ai-energy-auditor-concept.png` | PNG | 1600x900 | 295.4 KB | Not selected | Raster preview | Excluded because SVG is smaller and cleaner. |
| `img/ai-energy-auditor-concept-assets/ai-energy-auditor-concept-transparent.svg` | SVG | 1600x900 | 10.0 KB | Not selected | Alternate AI concept graphic | Excluded as duplicate. |
| `img/ai-energy-auditor-concept-assets/ai-energy-auditor-concept-compact.svg` | SVG | 900x1200 | 5.0 KB | Not selected | Mobile AI concept candidate | Excluded to keep the final asset set small. |
| `img/ai-energy-auditor-concept-assets/ai-energy-auditor-concept-compact.png` | PNG | 900x1200 | 122.6 KB | Not selected | Raster preview | Excluded because SVG is preferred. |
| `img/ai-energy-auditor-concept-assets/README.txt` | TXT | N/A | 0.7 KB | Reference only | Asset notes | Read; not copied. |
| `img/method-stack-assets.zip` | ZIP | N/A | 188.4 KB | Not selected | Source bundle | Excluded; ZIP archives are not website assets. |
| `img/ai-energy-auditor-concept-assets.zip` | ZIP | N/A | 418.7 KB | Not selected | Source bundle | Excluded; ZIP archives are not website assets. |

## Selected final assets

| Final asset | Source | Format | Dimensions | Size | Website use |
| --- | --- | --- | ---: | ---: | --- |
| `site/assets/neutral-shift-lab-bg.jpg` | `ChatGPT Image 2 июл. 2026 г., 22_40_40.png` | JPEG | 1536x1024 | 91.0 KB | Shared hero / profile background layer. |
| `site/assets/qr-card-bg.jpg` | `ChatGPT Image 2 июл. 2026 г., 22_40_40.png` | JPEG | 900x900 | 40.2 KB | QR card background layer. |
| `site/assets/og-image.png` | `ChatGPT Image 2 июл. 2026 г., 22_40_40.png` | PNG | 1200x630 | 676.2 KB | Local Open Graph preview image. |
| `site/assets/ik-logo.svg` | Hand-authored from reviewed IK mark direction | SVG | 96x96 viewBox | 0.8 KB | Navigation logo / mark. |
| `site/assets/favicon.svg` | Hand-authored from reviewed IK mark direction | SVG | 64x64 viewBox | 0.6 KB | Browser favicon. |
| `site/assets/method-stack.svg` | `img/method-stack-assets/method-stack.svg` | SVG | 1200x360 | 7.4 KB | Homepage and EN/RU method stack illustration. |
| `site/assets/ai-energy-auditor.svg` | `img/ai-energy-auditor-concept-assets/ai-energy-auditor-concept.svg` | SVG | 1600x900 | 10.0 KB | EN/RU AI Engineering Lab concept illustration. |

## Optimization notes

- `magick` and `cwebp` were not available in the local environment, so WebP
  conversion was not performed.
- The selected raster background source was resized / recompressed with local
  .NET / GDI+ tools into smaller JPEG derivatives.
- Final generated raster assets were written from fresh bitmap canvases, avoiding
  source PNG metadata propagation.
- SVG assets were preferred for diagrams and logos because they are small,
  local, dependency-free, and avoid raster metadata.
- SVG font stacks were adjusted to system fonts only.

## Website integration

- `site/index.html` now uses the local favicon, OG image, IK logo mark, and
  method-stack illustration.
- `site/qr/index.html` now uses the local favicon / OG metadata and the QR card
  receives a local branded background through CSS.
- `site/en/index.html` and `site/ru/index.html` now include method-stack and AI
  Energy Auditor concept illustrations in existing sections.
- `site/kk/index.html` receives only light visual consistency via favicon,
  metadata, and logo mark; no complex untranslated diagrams were added.
- `site/assets/styles.css` handles local background images, responsive asset
  figures, logo placement, and print-safe fallbacks.

## Privacy review

No selected final asset visibly contains:

- private phone numbers;
- private email addresses;
- WhatsApp / Telegram handles;
- private addresses;
- IIN or civil identifiers;
- date of birth;
- document, certificate, diploma, attestation, or membership numbers;
- document scans;
- signatures, seals, QR / EDS blocks;
- client names;
- contracts;
- private facility details;
- citation metrics or h-index values.

Excluded large PNGs contained broad marketing copy or stronger positioning than
the current evidence-backed site should publish. They remain source candidates
only and were not copied into `site/assets/`.

## Remaining TODOs

- Visual QA on Cloudflare preview is still required.
- Domain activation / DNS verification remains pending.
- Public contact route remains pending approval.
- Patent registry verification remains pending.
- Kazakh language review remains pending.
- SEO / metadata can be finalized in a later PR after visual assets are accepted.

## Visual QA notes for PR #24

Local headless Chrome screenshots were checked at 390px, 430px, 768px, 1024px,
and 1440px widths for `/`, `/qr`, `/en`, `/ru`, and `/kk`.

Findings and corrections:

- Header: the IK mark plus `IKurabayev.kz / Neutral Shift Lab` could become
  crowded on tablet widths, so the decorative suffix is hidden at 1020px and
  below.
- Hero background: the Neutral Shift Lab raster background was readable but
  visually active, so the dark overlay was strengthened.
- QR page: the QR card was close to the mobile viewport edge and risked
  horizontal overflow; the QR shell and card width rules were tightened, long
  text wrapping was hardened, and the `Home` mini-link is hidden under 500px.
- Method stack illustration: the previous mobile rule forced a 48rem image with
  translation, which risked awkward cropping; the mobile rule now uses normal
  responsive width with no transform.
- Section illustrations: selected SVG illustrations are capped with
  `max-height` and `object-fit: contain` so they support the text rather than
  dominate it.

Premium polish follow-up:

- The visual hierarchy was refined again on the same PR branch after reviewing
  local screenshots at 390px, 430px, 768px, 1024px, and 1440px.
- QR was tightened into a more badge-like composition: primary actions moved
  closer to the top, portrait and phase panel are treated as one compact visual
  unit, and status/profile links are visually quieter.
- EN/RU profile sections now use stronger hierarchy: major panels for primary
  explanation sections, quieter supporting cards, record-style publication rows,
  and compact recognition records.
- Method stack duplication was reduced by keeping the SVG as the main visual
  and making the explanatory method cards more compact.
- Visible ASCII arrows were replaced with `→`; Russian headings received light
  typography polish without changing technical meaning.
