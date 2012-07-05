import hashlib

prev_h = ''
blocks = []
data = 'foo'

with open('assignment3.mp4', 'rb') as f:
    while data != '':
        data = f.read(1024)
        if data != '':
            blocks.insert(0, data)

for data in blocks:
        prev_h = hashlib.sha256(data + prev_h).digest()
        hex_h = hashlib.sha256(data + prev_h).hexdigest()

print hex_h
