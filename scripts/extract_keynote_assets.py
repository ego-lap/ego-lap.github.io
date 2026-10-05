#!/usr/bin/env python3
"""Extract selected original assets from the supplied Keynote archive.

Usage: python scripts/extract_keynote_assets.py /path/to/egolap_figures.key
Photographs are encoded as high-quality WebP without resizing; chart PNGs and
trajectory frames are copied byte-for-byte. No slide previews are used.
"""
import argparse
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {'human-mecka.webp': 'Data/mecka-10127.png', 'human-aria.webp': 'Data/aria-10131.png', 'robot-agibot.webp': 'Data/agibot-9908.png', 'robot-yam.webp': 'Data/IMG_0363-12872.jpg', 'simulation-tasks.webp': 'Data/perturbation_03_seed_20260513-11838.png', 'results-simulation.png': 'Data/pasted-movie-13000.png', 'results-real-world.png': 'Data/pasted-movie-13021.png', 'reasoning-comparison.png': 'Data/pasted-movie-12750.png', 'human-fold-1.png': 'Data/human_01_anchor_02-10921.png', 'human-fold-2.png': 'Data/human_02_anchor_04-10924.png', 'human-fold-3.png': 'Data/human_03_anchor_08-10926.png', 'human-fold-4.png': 'Data/human_04_anchor_21-10928.png', 'robot-fold-1.png': 'Data/robot_01_anchor_36-10963.png', 'robot-fold-2.png': 'Data/robot_02_anchor_50-10964.png', 'robot-fold-3.png': 'Data/robot_03_anchor_70-10965.png', 'robot-fold-4.png': 'Data/robot_04_anchor_84-10966.png'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    args = parser.parse_args()
    output = ROOT/'assets/images/keynote'
    output.mkdir(parents=True,exist_ok=True)
    records = []
    with ZipFile(args.archive) as archive:
        for name,source in ASSETS.items():
            content = archive.read(source)
            image = Image.open(BytesIO(content))
            if name.endswith('.webp'):
                image.save(output/name,quality=95,method=6)
            else:
                (output/name).write_bytes(content)
            records.append({'file':name,'source':source,'dimensions':list(image.size),'resized':False})
    (output/'sources.json').write_text(json.dumps({'archive':args.archive.name,'assets':records},indent=2)+'\n')
    print(f'Extracted {len(records)} assets at their native dimensions.')

if __name__ == '__main__':
    main()
