#!/usr/bin/env python3
"""python3 publish.py android <apk> <versionName> <versionCode> [--notes ".."] [--force] [--min N]"""
import argparse, json, os, shutil
p = argparse.ArgumentParser()
p.add_argument("platform", choices=["android"]); p.add_argument("apk"); p.add_argument("versionName"); p.add_argument("versionCode", type=int)
p.add_argument("--notes", default=""); p.add_argument("--force", action="store_true"); p.add_argument("--min", type=int, default=0)
a = p.parse_args()
os.makedirs("android", exist_ok=True)
name = f"SahraRemote-{a.versionName}.apk"
shutil.copy(a.apk, os.path.join("android", name))
feed = json.load(open("update.json")) if os.path.exists("update.json") else {}
if a.versionCode <= feed.get("android", {}).get("versionCode", 0): raise SystemExit("versionCode must go up")
feed["android"] = {"versionName": a.versionName, "versionCode": a.versionCode,
    "url": f"https://raw.githubusercontent.com/moraxdev/sahra-remote-releases/main/android/{name}",
    "notes": a.notes, "force": a.force, "minVersionCode": a.min}
json.dump(feed, open("update.json", "w"), indent=2)
