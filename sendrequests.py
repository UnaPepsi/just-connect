import requests
from requests.exceptions import ReadTimeout, ConnectionError, ConnectTimeout
from typing import Optional

BASE = 'https://fun.guimx.me/jaja'

class BaseException(Exception):
    ...
class BadCredentials(BaseException):
    ...
class Timeout(BaseException):
    ...
class RateLimited(BaseException):
    ...
class UsernameInUse(BaseException):
    ...

def login(username: str, password: str):
    """
    Manda un POST request login

    Parameters
    ----------
    username : `str`
        El nombre de usuario
    password : `str`
        La contraseña
    """
    try:
        resp = requests.post(f'{BASE}/login', json={'name': username, 'passwd': password})
    except (ReadTimeout, ConnectionError, ConnectTimeout):
        raise Timeout('El servidor no responde')
    if resp.status_code == 200:
        return resp.json()
    if resp.status_code == 429:
        raise RateLimited('Estás enviando muchas peticiones, intenta más tarde')
    raise BadCredentials('Credenciales incorrectas')

def register(username: str, password: str, pfp: Optional[bytes] = None):
    """
    Manda un POST request register

    Parameters
    ----------
    username : `str`
        El nombre de usuario
    password : `str`
        La contraseña
    pfp : `Optional[bytes]`
        La foto de perfil
    """
    body = {'name': username, 'passwd': password, 'pfp': pfp}
    if pfp is None: body.pop('pfp')
    try:
        resp = requests.post(f'{BASE}/register', json=body)
    except (ReadTimeout, ConnectionError, ConnectTimeout):
        raise Timeout('El servidor no responde')
    if resp.status_code == 200:
        return resp.json()
    if resp.status_code == 429:
        raise RateLimited('Estás enviando muchas peticiones, intenta más tarde')
    raise UsernameInUse('Ese nombre de usuario ya está en uso. Prueba con otro')