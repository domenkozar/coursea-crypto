"""Padding oracle attack on AES CBC chipertext at
http://crypto-class.appspot.com/po?er=<ciphertext>

PS: I know, probably my worst code ever out there.
"""

import requests


def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def has_correct_padding(ct):
    url = 'http://crypto-class.appspot.com/po?er=' + ct.encode('hex')
    print url

    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        raise Exception('you sent working ciphertext')
    elif r.status_code == 404:
        return True
    elif r.status_code == 403:
        return False
    else:
        raise Exception('Unexpected http code: %d' % r.status_code)


if __name__ == '__main__':
    ct = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61\
044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'.decode('hex')
    msg = ''

    ct_blocks = [ct[:16], ct[16:32], ct[32:48], ct[48:64]]

    for i in range(2, 3):
        first_block = ct_blocks[i]
        block_msg = []

        for block_part in reversed(range(16)):
            new_first_block = list(first_block)
            print "using block %d: " % i, new_first_block

            # calculate new padding
            padding_num = 16 - block_part
            padding = chr(padding_num)
            print "padding ", repr(padding)

            # apply padding
            for j in range(1, padding_num + 1):
                new_first_block[-j] = strxor(new_first_block[-j], padding)

            print "block with padding", new_first_block

            # apply known guesses
            for k, m in enumerate(reversed(block_msg)):
                k += 1
                prev_k = new_first_block[-k]
                new_first_block[-k] = strxor(new_first_block[-k], m)
                print "xoring %r with %r gets us %r" % (prev_k, m, new_first_block[-k])

            print "block with known guesses", new_first_block

            # xor the new guess
            for guess_num in [32] + range(97, 123) + range(2, 98) + range(98, 256):
                guess = chr(guess_num)
                print "guess %r" % (guess)
                new_first_block2 = list(new_first_block)
                new_first_block2[block_part] = strxor(new_first_block2[block_part], guess)
                print "first_block with guess", new_first_block2
                if has_correct_padding(''.join(ct_blocks[i-1:i] + new_first_block2 + [ct_blocks[i + 1]])):
                    block_msg.insert(0, guess)
                    print "msg ", block_msg
                    print
                    break
            else:
                raise Exception('nothing found in this block! msg: %r block_msg: %r' % (msg, block_msg))
        msg += ''.join(block_msg)

    print msg
