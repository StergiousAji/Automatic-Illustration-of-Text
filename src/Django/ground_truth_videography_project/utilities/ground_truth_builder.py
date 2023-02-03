import numpy as np
import json
import os

def build_ground_truth(audio, chunks, clip, folder):
    ground_truth = {
        'id': audio.filename,
        'artist': audio.artist,
        'title': audio.title,
    }

    chunks_info = []
    for c in chunks:
        selected_image_ids = np.array(c.image_ids)[c.selected_ids].tolist() if c.image_ids != [] and c.selected_ids != []  else []
        selected_image_paths = clip.image_paths[selected_image_ids].tolist()
        chunks_info.append({
            'index': c.index,
            'text': c.text,
            'start_time': c.start_time,
            'end_time': c.end_time,
            'selected_image_ids': selected_image_ids,
            'selected_image_paths': selected_image_paths,
        })
    
    ground_truth['chunks'] = chunks_info

    audio.ground_truth = ground_truth
    audio.save(False)

    with open(os.path.join(folder, "ground_truth", f"{audio.filename}.json"), "w", encoding='utf-8') as gt_json:
        json.dump(ground_truth, gt_json, indent=4, ensure_ascii=False)

def load_ground_truth(folder, filename):
    try:
        with open(os.path.join(folder, "ground_truth", f"{filename}.json"), 'r', encoding="utf-8") as gt_json:
            return json.load(gt_json)
    except Exception as ex:
        print(f"\u001b[31m{type(ex).__name__}: {ex.args}\u001b[0m")
        return None