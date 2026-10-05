# EgoLAP project website

Static project website for **EgoLAP: Learning from Egocentric Human Data through Language-Action Reasoning**. Content and author order come from the current `-ICLR-2027-Ego-LAP/arxiv.tex` release and shared paper sections. Design follows the centered research-page layout, orange accent, wave header, and section navigation of https://lap-vla.github.io/. HTML, CSS, and JavaScript are implemented independently.

## Preview

Run `python -m http.server 8765` from this folder and visit http://localhost:8765/.

The included paper PDF was built from the existing public-release source. No acceptance claim, arXiv identifier, or public code/checkpoint URL has been invented.

## Videos

The supplied Slack message lists seven MP4 files. Slack's connector can read the message but returns `file_not_found` for all seven download requests. No substitute videos are used. The empty gallery stays hidden until real clips are available.

Download the attachments into a folder outside this checkout, then run:

```sh
python scripts/prepare_videos.py /path/to/slack-downloads
```

This samples frames across each video, detects black borders, conservatively combines content bounds, crops the actual encoded video, outputs browser-compatible H.264 with fast-start metadata, and creates posters plus `assets/videos/manifest.json`. Originals are retained. Provide `--titles captions.json` to label clips whose task is not identifiable from their filename. Inspect the processed clips before publication.

## GitHub organization and Pages

Suggested organization: `ego-lap`. It was not found by GitHub's API when checked during setup; the signup page must confirm availability.

Create the free organization at https://github.com/organizations/plan, then run from this folder:

```sh
gh repo create ego-lap/ego-lap.github.io --public --source=. --remote=origin --push
gh api --method POST repos/ego-lap/ego-lap.github.io/pages -f build_type=workflow
```

The included GitHub Actions workflow publishes the site at https://ego-lap.github.io/. Organization creation requires GitHub's interactive signup; the available GitHub tools do not expose that operation. No organization or remote repository has been created yet.

## Validation

Browser checks at desktop and mobile sizes verify image loading, horizontal overflow, and JavaScript errors. The citation button supports copying with a readable fallback. Tables scroll on narrow screens; navigation and controls support keyboard focus and reduced motion. Deployment contains only the public site and its assets, excluding processing scripts and documentation.
