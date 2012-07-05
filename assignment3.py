"""Homework #3 for Stanford crypto class
implementing block hashing of video files
for validating origin of streamed video.
"""
import hashlib


def get_h_from_file(filename):
    blocks = []
    prev_h = ''

    with open(filename, 'rb') as f:
        data = None
        while data != '':
            data = f.read(1024)
            if data != '':
                blocks.insert(0, data)

    for block in blocks:
        m = block + prev_h
        h = hashlib.sha256(m)
        prev_h = h.digest()
        hex_h = h.hexdigest()

    return hex_h

print('sample: ' + get_h_from_file('assignment3-sample.mp4'))
print('result: ' + get_h_from_file('assignment3-result.mp4'))
