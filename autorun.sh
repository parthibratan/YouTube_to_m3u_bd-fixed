#!/bin/bash
pip3 install -r requirements.txt --upgrade
python3 scripts/youtube_m3ugrabber.py 2> last_run_error.log
git add youtube.m3u
git commit -m "links are updated" || true
git push
