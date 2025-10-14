from slowapi import Limiter
from slowapi.util import get_remote_address

# A criação do limiter agora vive aqui, num local central e independente.
limiter = Limiter(key_func=get_remote_address)
