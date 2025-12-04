import os
import sys
import numpy as np
import soundfile as sf
import ffmpeg

video_file = sys.argv[1]
fps = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0

tmp = "temp_ltc.wav"
print("Extracting audio...")
ffmpeg.input(video_file).output(tmp, ac=1, ar=48000, acodec='pcm_s16le')\
    .overwrite_output().run(quiet=True)
audio, sr = sf.read(tmp)
os.remove(tmp)

frame_samples = int(sr / fps)
step = frame_samples // 2

def has_ltc(chunk):
    if len(chunk) < frame_samples//2: return False
    crossings = ((chunk[:-1] * chunk[1:]) < 0).sum()
    level = np.max(np.abs(chunk))
    return crossings > 85 and level > 0.05

ltc_blocks = []
current_start = None

print("Finding real LTC takes (discarding non-LTC parts)...")
for i in range(0, len(audio)-frame_samples, step):
    pos = i / sr
    chunk = audio[i:i+frame_samples]
    detected = has_ltc(chunk)

    if detected and current_start is None:
        current_start = pos
        print(f"LTC take STARTS at {pos:.2f}s")
    elif not detected and current_start is not None:
        end = pos
        if end - current_start > 2.0: 
            print(f"  → LTC take ENDS at {end:.2f}s (duration: {end-current_start:.2f}s)")
            ltc_blocks.append((current_start, end))
        else:
            print(f"  → Short LTC burst ignored (<2s)")
        current_start = None

if current_start is not None:
    end = len(audio)/sr
    if end - current_start > 2.0:
        print(f"  → LTC take ENDS at file end ({end:.2f}s)")
        ltc_blocks.append((current_start, end))

# Split — ONLY the real LTC takes
os.makedirs("splits", exist_ok=True)
base = os.path.splitext(os.path.basename(video_file))[0]

print(f"\nFound {len(ltc_blocks)} real LTC takes → exporting...")
for i, (start, end) in enumerate(ltc_blocks, 1):
    duration = end - start
    out = f"splits/{base}_LTC_take_{i:02d}_{int(start)}s.mp4"
    (
        ffmpeg
        .input(video_file, ss=start, t=duration)
        .output(out, c='copy')
        .overwrite_output()
        .run(quiet=True)
    )
    print(f"  Take {i}: {out}  ({duration:.2f}s)")

print(f"\nDone! Only real LTC takes saved — {len(ltc_blocks)} clean clips created.")
print("   Non-LTC parts (silence, noise, etc.) were discarded.")
