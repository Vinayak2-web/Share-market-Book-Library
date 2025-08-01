import random
from django.utils.encoding import force_bytes,force_str # type: ignore
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode # type: ignore

def get_otp():
    return random.randint(1000,9999)

def enc_uname(uname):
    return urlsafe_base64_encode(force_bytes(uname))

def dec_uname(encoded_uname):
    return force_str(urlsafe_base64_decode(encoded_uname))