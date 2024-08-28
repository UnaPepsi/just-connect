import requests
from requests.exceptions import ReadTimeout, ConnectionError, ConnectTimeout
from typing import Optional
from base64 import b64decode, b64encode

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
class UserNotFound(BaseException):
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

def send_message(token: str, recipient: str, message: str, file: Optional[bytes] = None):
	"""
	Manda un POST request send

	Parameters
	----------
	token : `str`
		El token de autenticación
	recipient : `str`
		El destinatario
	message : `str`
		El mensaje
	file : `Optional[bytes]`
		Un objeto tipo bytes representando un archivo
	"""
	body = {'auth': token, 'recipient': recipient, 'message': message}
	if file is not None:
		body['file'] = b64encode(file).decode('utf-8')
	resp = requests.post(f'{BASE}/send', json=body)
	if resp.status_code == 200:
		return resp.json()
	if resp.status_code == 429:
		raise RateLimited('Estás enviando muchas peticiones, intenta más tarde')
	if resp.status_code in (401, 403):
		raise BadCredentials('Credenciales incorrectas. Este error no debería pasar...')
	else:
		raise BaseException('Error desconocido')

def edit_user(token: str,new_user: Optional[str], new_password: Optional[str] = None, pfp: Optional[bytes] = None):
	"""
	Manda un POST request edit

	Parameters
	----------
	token : `str`
		El token de autenticación
	new_password : `Optional[str]`
		La nueva contraseña
	pfp : `Optional[bytes]`
		La foto de perfil
	"""
	body = {'auth': token, 'new_name':new_user}
	if new_password:
		body['new_passwd'] = new_password	
	if pfp is not None:
		body['pfp'] = b64encode(pfp).decode('utf-8')
	resp = requests.post(f'{BASE}/edit', json=body)
	if resp.status_code == 200:
		return resp.json()
	if resp.status_code == 429:
		raise RateLimited('Estás enviando muchas peticiones, intenta más tarde')
	if resp.status_code in (401, 403, 400):
		raise BadCredentials('Credenciales incorrectas. Este error no debería pasar...')
	else:
		raise BaseException(f'Error desconocido: {resp.status_code}')
	
def load_other_pfp(user: str):
	"""
	Manda un GET request pfp

	Parameters
	----------
	user : `str`
		El nombre de usuario
	"""
	resp = requests.get(f'{BASE}/pfp?name={user}')
	if resp.status_code == 200:
		return b64decode(resp.json()['info']['pfp'])
	if resp.status_code == 429:
		raise RateLimited('Estás enviando muchas peticiones, intenta más tarde')
	if resp.status_code == 404:
		raise UserNotFound('Usuario no encontrado')
	else:
		raise BaseException(f'Error desconocido: {resp.status_code}')