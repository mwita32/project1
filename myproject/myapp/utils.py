from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

def generate_token(user):
    return default_token_generator.make_token(user)

def encode_uid(pk):
    return urlsafe_base64_encode(force_bytes(pk))

def decode_uid(encoded_pk):
    return force_str(urlsafe_base64_decode(encoded_pk))
