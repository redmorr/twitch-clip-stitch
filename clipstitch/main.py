import detectoverlap

clips = detectoverlap.display_all_clips_overlapping_clip_by_frames('../input/single-stream-all-clips')
clip_chains = detectoverlap.find_seamless_clip_chains(clips)
