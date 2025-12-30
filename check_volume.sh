#!/bin/bash
ffmpeg -i test_audio_output.wav -af volumedetect -f null /dev/null > volume_check.txt 2>&1
echo "Done"
