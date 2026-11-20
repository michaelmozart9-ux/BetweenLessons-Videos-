"""Mux frames + audio into the final MP4.  python encode.py <videoDir> [out.mp4]"""
import os, subprocess, sys
d = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(d, os.path.basename(os.path.normpath(d)) + ".mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", os.path.join(d, "frames", "%04d.jpg"), "-i", os.path.join(d, "audio.wav"),
                "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
print(f"wrote {out} ({dur}s)")
