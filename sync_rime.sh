#!/bin/bash
# filepath: sync_rime.sh

SRC=~/Library/Rime/
DEST=.

rsync -av \
--exclude 'build/' \
"$SRC" "$DEST"
