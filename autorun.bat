@echo off
pip install -r requirements.txt --upgrade
python scripts\youtube_m3ugrabber.py 2> last_run_error.log
git add youtube.m3u
git commit -m "links are updated" || exit 0
git push
