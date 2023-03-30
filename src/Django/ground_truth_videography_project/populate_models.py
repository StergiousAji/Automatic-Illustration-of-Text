import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ground_truth_videography_project.settings')

import django
django.setup()

from ground_truth.models import Audio, Chunk
import json
import numpy as np

Audio.objects.all().delete()
Chunk.objects.all().delete()


with open(r"audios.json", "r", encoding='utf-16') as file:
    audios = json.load(file)

with open(r"chunks.json", "r", encoding='utf-16') as file:
    chunks = json.load(file)

for audio in audios:
    print(audio['pk'], audio['fields']['slug'])

audio_pks = list(set([audio['pk'] for audio in audios]).difference([3, 77, 254, 259]))
print(audio_pks)

audios = [audio for audio in audios if audio['pk'] in audio_pks]
for audio in audios:
    print(audio['pk'], audio['fields']['slug'])

order = np.argsort([11, 0, 10, 1, 3, 4, 9, 7, 5, 8, 6, 2])
print(order)
audios = np.array(audios)[order][:10]
for audio in audios:
    print(audio['pk'], audio['fields']['slug'])


def populate_audio(audios):
    for audio_info in audios:
        a = audio_info['fields']
        audio = Audio(music=a['music'], artist=a['artist'], title=a['title'], filename=a['filename'], transcript=a['transcript'], coverart_colour=a['coverart_colour'], _ground_truth="null")
        # audio._ground_truth = a['_ground_truth']
        audio.save(True)

def populate_chunks(chunks):
    audio_objs = list(Audio.objects.all())
    for i, audio in enumerate(audios):
        for chunk_info in chunks:
            c = chunk_info['fields']
            if c['audio'] != audio['pk']:
                  continue
              
            chunk = Chunk(index=c['index'], text=c['text'], audio_id=audio_objs[i].id, start_time=c['start_time'], end_time=c['end_time'], _image_ids=c['_image_ids'], _selected_ids="[]")
            if audio['fields']['slug'] in ['nena-99-luftballons', 'coldplay-viva-la-vida']:
                chunk._selected_ids = c['_selected_ids']
            chunk.save()

if (__name__=='__main__'):
    print('Populating database...')
    populate_audio(audios)
    populate_chunks(chunks)