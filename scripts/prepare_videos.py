#!/usr/bin/env python3
"""Remove persistent black borders and create web-ready H.264 videos and posters.

Usage: python scripts/prepare_videos.py /path/to/downloaded/slack/videos
Original inputs remain untouched. Requires ffmpeg and ffprobe.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
NAMES = {'video_2026_10_03_18_49_46': 'Fold pants', '05_red-bottle-in-bowl__video_egolap_pick_red_bottle_success_2026_08_12_18_43_00': 'Place the red bottle', '03_wipe-blue-bowl__video_ego_lap_reasoning_wipe_the_blue_bowl_success_2026_09_08_16_54_32': 'Wipe the blue bowl', 'y__2026_09_11_16_46_12': 'Place the bottle into the blue bowl', 'lap_reason__2026_09_09_22_20_30': 'Handover and put the object in the bowl', 'video_2026_10_03_18_26_33': 'Put the banana on the plate', 'lap_reason__2026_09_16_16_51_17': 'Manipulate the corn'}

def run(command):
    return subprocess.run(command, check=True, capture_output=True, text=True)

def prepare(source, output, title):
    info = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration', '-of', 'json', str(source)]).stdout)
    stream = info['streams'][0]
    width, height = stream['width'], stream['height']
    duration = float(info['format']['duration'])
    # Sample throughout the clip rather than infer borders from one dark frame.
    crops = []
    for fraction in [0.1, 0.3, 0.5, 0.7, 0.9]:
        result = run(['ffmpeg', '-hide_banner', '-ss', str(duration*fraction), '-i', str(source), '-t', str(min(2, duration*(1-fraction))), '-vf', 'cropdetect=limit=24:round=2:reset=0', '-an', '-f', 'null', '-'])
        detections = re.findall(r'crop=(\d+):(\d+):(\d+):(\d+)', result.stderr)
        if detections:
            crop = tuple(map(int, Counter(detections).most_common(1)[0][0]))
            # Avoid destructive crops when the frame is mostly black.
            if crop[0]*crop[1] >= width*height*0.45:
                crops.append(crop)
    # Union of detected content bounds preserves objects visible in any sample.
    if crops:
        left = min(c[2] for c in crops)//2*2
        top = min(c[3] for c in crops)//2*2
        right = min(width, max(c[2]+c[0] for c in crops))//2*2
        bottom = min(height, max(c[3]+c[1] for c in crops))//2*2
        crop = (right-left, bottom-top, left, top)
    else:
        crop = (width//2*2, height//2*2, 0, 0)
    target = output/(source.stem+'.mp4')
    if source.resolve() == target.resolve():
        raise ValueError('Use an input folder outside assets/videos to preserve originals.')
    filters = 'crop={}:{}:{}:{},scale=w=min(1280\\,iw):h=-2'.format(*crop)
    run(['ffmpeg','-y','-hide_banner','-i',str(source),'-map','0:v:0','-vf',filters,'-c:v','libx264','-preset','medium','-crf','23','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(target)])
    poster = target.with_suffix('.jpg')
    run(['ffmpeg','-y','-hide_banner','-ss',str(min(1,duration/2)),'-i',str(target),'-frames:v','1','-q:v','2',str(poster)])
    return {'file': target.name, 'poster': poster.name, 'title': title, 'source': source.name, 'original_size': [width,height], 'crop': list(crop)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/videos')
    parser.add_argument('--titles',type=Path,help='Optional JSON mapping from original filename to caption')
    args = parser.parse_args()
    sources = sorted(p for p in args.input.iterdir() if p.suffix.lower() in {'.mp4','.mov','.m4v'})
    if not sources:
        parser.error('No videos found in the input folder.')
    args.output.mkdir(parents=True,exist_ok=True)
    titles = json.loads(args.titles.read_text()) if args.titles else {}
    manifest = []
    for index,source in enumerate(sources,1):
        if source.stem == 'lap_reason__2026_09_16_16_51_17':
            continue
        title = titles.get(source.name,NAMES.get(source.stem,f'EgoLAP rollout {index}'))
        item = prepare(source,args.output,title)
        manifest.append(item)
        print(f'{source.name}: {item["original_size"]} → crop {item["crop"]}')
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Prepared {len(manifest)} videos; gallery is enabled automatically.')

if __name__ == '__main__':
    main()
