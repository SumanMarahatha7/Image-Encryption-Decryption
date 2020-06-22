import os
import math
import string
import random

from PIL import Image
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def get_key(key):
    main_key = SHA256.new(key.encode('utf-8')).digest()
    key1 = key[:math.floor(len(key) / 2)]
    key2 = key[math.floor(len(key) / 2):]
    key1 = SHA256.new(key1.encode('utf-8')).digest()
    key2 = SHA256.new(key2.encode('utf-8')).digest()
    return main_key, key1, key2


def encrypt(key, filename):
    with open(filename, 'rb') as file:
        infile = file.read()
        main_key, key1, key2 = get_key(key)

        iv = os.urandom(16)
        encryptor = AES.new(main_key, AES.MODE_CFB, iv)
        outfile = key1 + encryptor.encrypt(infile)

        encryptor_new = AES.new(key2, AES.MODE_CFB, iv)
        final = iv + encryptor_new.encrypt(outfile)

        with open(filename, 'wb') as encrypted:
            encrypted.write(final)


def decrypt(key, filename):
    with open(filename, 'rb') as file:
        final = file.read()
        main_key, key1, key2 = get_key(key)

        iv = final[:16]
        decryptor_new = AES.new(key2, AES.MODE_CFB, iv)
        outfile = decryptor_new.decrypt(final[16:])

        if outfile[:32] == key1:
            decryptor = AES.new(main_key, AES.MODE_CFB, iv)
            infile = decryptor.decrypt(outfile[32:])
            r_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(5))
            with open(f"media/DecryptedImage/processing-{r_str}.jpg", 'wb') as writing:
                writing.write(infile)
            image = Image.open(f"media/DecryptedImage/processing-{r_str}.jpg")
            return {"image": image.filename}
        else:
            return {'error': 'Key doest matches'}
