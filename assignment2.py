"""Based on slowaes pure Python implementation (not recommended for real usage!)
"""

import itertools
import struct

from aes import AES



def group_by(iterable, n):
    args = [iter(iterable)] * n
    return itertools.izip_longest(*args)

def strxor(a, b):
    """xor two ascii strings"""
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def aes_cbc_decrypt(key, ciphertext):
    aes = AES()

    def cbc_heart(key, iv, block):
        #print "block: %r, key: %r, iv: %r" % (block, key, iv)
        output = aes.decrypt(
            struct.unpack('>' + 'B'*16, block),
            struct.unpack('>' + 'B'*16, key),
            16)
        return strxor(iv, struct.pack('>' + 'B'*16, *output))

    iv = None
    plaintext = ''
    for block in group_by(ciphertext, 16):
        block = "".join(block)
        if not iv:
            iv = block
            continue

        plaintext += cbc_heart(key, iv, block)
        iv = block

    padding = struct.unpack('>B', plaintext[-1:])[0]
    print "padding: ", padding

    return plaintext[-1 * padding:].encode('hex')


def aes_ctr_decrypt(key, chipertext):
    return plaintext


if __name__ == '__main__':
    cbc_key = "140b41b22a29beb4061bda66b6747e14"
    cbc_data = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee\
2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
    cbc_2_key = "140b41b22a29beb4061bda66b6747e14"
    cbc_2_data = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48\
e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
    print aes_cbc_decrypt(cbc_key.decode('hex'), cbc_data.decode('hex'))
    print aes_cbc_decrypt(cbc_2_key.decode('hex'), cbc_2_data.decode('hex'))

    ctr_key = "36f18357be4dbd77f050515c73fcf9f2"
    ctr_data = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc3\
88d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
    ctr_2_key = "36f18357be4dbd77f050515c73fcf9f2"
    ctr_2_data = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa\
0e311bde9d4e01726d3184c34451"
    print aes_ctr_decrypt(ctr_key.decode('hex'), ctr_data.decode('hex'))
    print aes_ctr_decrypt(ctr_2_key.decode('hex'), ctr_2_data.decode('hex'))
