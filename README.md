# EgoLAP project website

Static project website for **EgoLAP: Learning from Egocentric Human Data through Language-Action Reasoning**. Content and author order come from the current `-ICLR-2027-Ego-LAP/arxiv.tex` release and shared paper sections. The design uses a warm neutral background, forest-green accents, spacious typography, a prominent interactive video showcase, and a sticky navigation bar. HTML, CSS, and JavaScript are implemented independently. Research content is retained from the paper; the new layout prioritizes its demonstrations.

## Preview

Run `python -m http.server 8765` from this folder and visit http://localhost:8765/.

Paper links point to https://arxiv.org/abs/2610.08726, and the citation uses its arXiv BibTeX. The local paper PDF remains archived; code and checkpoints are marked coming soon.

## Visual assets

Charts and supporting visuals use ingredients from the user-supplied `egolap_figures.key`. `assets/images/keynote/sources.json` records original archive members and pixel dimensions. Overview and method integrate the figures’ source photographs and trajectory frames with browser-rendered explanations and model components.

- Original simulation and real-world chart PNGs are copied byte-for-byte at 3793×1313 and 3793×1319. The reasoning chart is copied at 2237×1574. Original legends and uncertainty bars remain intact.
- Original robot photographs and dataset images retain their native pixel dimensions; photographic WebP files use quality 95 without downsampling.
- One integrated diagram shows a vector ring chart of the four training-data groups with representative camera views and dataset weights, explains the motivation for motion-level reasoning, and connects a clearly labeled cloth-folding example to the model architecture. The Keynote-inspired architecture uses native text, token streams, a separate action expert and a shared observation prefix; the diagram scrolls on narrow screens. All eight original frames appear beside concise reasoning and action excerpts. A separate inference path emphasizes action-expert rollout with no generated text. Native HTML annotations stay sharp; frames retain their original 224×224 (human) and 168×168 (robot) dimensions. Original figures remain archived in `assets/images/original/` without being embedded.
- Two compact summary charts are rebuilt as SVG from verified results: human-data transfer (7.2% and 16.4% success) and GRPO relative improvements (19.4%, 12.7%, and 14.2%). No uncertainty estimates are invented.
- Wide result charts scroll within their containers on phones and include links to the full-resolution originals.

Re-extract source assets with `python scripts/extract_keynote_assets.py /path/to/egolap_figures.key`. Regenerate vector summaries with `python scripts/render_summary_charts.py` (requires Pillow for extraction and matplotlib for chart rendering).

## Videos

All seven user-provided clips are included. Each original 672×224 three-camera video had 50-pixel black borders above and below the content; the encoded output is cropped to 672×124. Original attachments remain untouched. H.264 output uses fast-start metadata and includes posters.

The showcase includes task selection, all-camera and individual-camera views, playback speed, seeking, pause, and fullscreen. Mobile starts with the base camera to keep the action readable. Autoplay is disabled for reduced-motion preferences; videos pause when outside the viewport or when the page is hidden.

To process new clips, download them into a folder outside this checkout and run:

```sh
python scripts/prepare_videos.py /path/to/videos
```

Use `--titles captions.json` to label new clips. Captions for the supplied clips describe their visible manipulation; the two cloth clips use neutral labels because the source filenames do not provide task instructions. The video manifest controls showcase order and labels.

## GitHub Pages

Organization: https://github.com/ego-lap

Website repository: https://github.com/ego-lap/ego-lap.github.io

Public website: https://ego-lap.github.io/

GitHub Pages is configured to deploy through `.github/workflows/pages.yml`. Pushing to `main` publishes the latest website automatically. The workflow stages only the website files and assets; scripts and documentation remain in the repository.

To update the live website, edit and verify locally, then commit and push to `main`. Deployment status is visible in the repository's Actions tab.

## Validation

Browser checks at 1440, 1024, 768, and 390 pixels verify image loading, horizontal overflow, and JavaScript errors. All seven cropped clips play in the browser. Task switching, playback speed, camera views, citation copying, and reduced-motion behavior are checked. The citation button supports copying with a readable fallback. Tables scroll on narrow screens; navigation and controls support keyboard focus and reduced motion. Deployment contains only the public site and its assets, excluding processing scripts and documentation.

The mixture camera assets and dataset-weight definitions were retrieved from Codex thread `01a0c08e-97a1-7932-9648-28c008f2f21f` (“Plot dataset mixture and cameras”). `assets/images/mixture/sources.json` records their origin. Batch weights are 25% EgoVerse, 30% ABC, 25% other bimanual, and 20% OXE; rounded displayed dataset weights sum to their group totals.
