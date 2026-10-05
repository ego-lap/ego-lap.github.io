# EgoLAP project website

Static project website for **EgoLAP: Learning from Egocentric Human Data through Language-Action Reasoning**. Content and author order come from the current `-ICLR-2027-Ego-LAP/arxiv.tex` release and shared paper sections. The design uses a warm neutral background, forest-green accents, spacious typography, a prominent interactive video showcase, and a sticky navigation bar. HTML, CSS, and JavaScript are implemented independently. Research content is retained from the paper; the new layout prioritizes its demonstrations.

## Preview

Run `python -m http.server 8765` from this folder and visit http://localhost:8765/.

The included paper PDF was built from the existing public-release source. No acceptance claim, arXiv identifier, or public code/checkpoint URL has been invented.

## Videos

All seven user-provided clips are included. Each original 672×224 three-camera video had 50-pixel black borders above and below the content; the encoded output is cropped to 672×124. Original attachments remain untouched. H.264 output uses fast-start metadata and includes posters.

The showcase includes task selection, all-camera and individual-camera views, playback speed, seeking, pause, and fullscreen. Mobile starts with the base camera to keep the action readable. Autoplay is disabled for reduced-motion preferences; videos pause when outside the viewport or when the page is hidden.

To process new clips, download them into a folder outside this checkout and run:

```sh
python scripts/prepare_videos.py /path/to/videos
```

Use `--titles captions.json` to label new clips. Captions for the supplied clips describe their visible manipulation; the two cloth clips use neutral labels because the source filenames do not provide task instructions. The video manifest controls showcase order and labels.

## GitHub organization and Pages

Suggested organization: `ego-lap`. It was not found by GitHub's API when checked during setup; the signup page must confirm availability.

Create the free organization at https://github.com/organizations/plan, then run from this folder:

```sh
gh repo create ego-lap/ego-lap.github.io --public --source=. --remote=origin --push
gh api --method POST repos/ego-lap/ego-lap.github.io/pages -f build_type=workflow
```

The included GitHub Actions workflow publishes the site at https://ego-lap.github.io/. Organization creation requires GitHub's interactive signup; the available GitHub tools do not expose that operation. No organization or remote repository has been created yet.

## Validation

Browser checks at 1440, 1024, 768, and 390 pixels verify image loading, horizontal overflow, and JavaScript errors. All seven cropped clips play in the browser. Task switching, playback speed, camera views, citation copying, and reduced-motion behavior are checked. The citation button supports copying with a readable fallback. Tables scroll on narrow screens; navigation and controls support keyboard focus and reduced motion. Deployment contains only the public site and its assets, excluding processing scripts and documentation.
