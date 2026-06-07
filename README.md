# MusicBee Compilation Tagger

A desktop GUI tool for fixing compilation and split EP album tags in MusicBee. Fixes the issue where MusicBee splits a single album across multiple artist entries due to inconsistent Album Artist or Album tags.

## The Problem

MusicBee groups albums by Album Artist and Album name. Compilation albums and split EPs often have inconsistent tags across tracks causing them to appear as separate albums per artist. This tool sets a unified Album Artist and Album name across all tracks in a folder.

## Tech Stack

- Python 3.x
- tkinter (built-in)
- mutagen

## How It Works

1. Select the album folder using the folder picker
2. Confirm or edit the album name (auto-filled from folder name)
3. Click Run Tagger
4. Album Artist is set to `Compilation: <folder name>` on every track
5. Album name is set uniformly across all tracks
6. Rescan your MusicBee library to apply

Supports MP3 and FLAC.

## Setup

**Prerequisites**

- Python 3.x
- mutagen

**Install dependencies**

```
pip install -r requirements.txt
```

**Run**

```
python tagger.py
```

## Screenshots

*(add screenshot here after first run)*

## Notes

Album Artist is intentionally set to `Compilation: <folder name>` instead of `Various Artists` to keep each compilation isolated in MusicBee without mixing with other compilations.
