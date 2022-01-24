import detectoverlap
import stitcher

clips = detectoverlap.display_all_clips_overlapping_clip_by_frames('../input/single-stream-all-clips')
clip_chains = detectoverlap.find_clip_chains(clips)
optimal_clip_chains = detectoverlap.remove_redundant_clips(clip_chains)
stitcher.display_overlap_stats(optimal_clip_chains)
stitcher.create_concat_input_file(optimal_clip_chains)