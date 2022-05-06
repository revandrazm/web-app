import bcrypt

def hash_password(password: str) -> bytes:
	"Hash a given password"
	
	return bcrypt.hashpw(password, bcrypt.gensalt())