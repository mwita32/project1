from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def generate_token(user):
    return default_token_generator.make_token(user)

def encode_uid(uid):
    return urlsafe_base64_encode(force_bytes(uid))

def decode_uid(uidb64):
    return force_str(urlsafe_base64_decode(uidb64))
