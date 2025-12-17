from models.User import User
from extensions import db
from passlib.hash import pbkdf2_sha256

# Check if an admin user exists in the database
async def admin_exists():
    admin_user = db.session.query(User).filter(User.username == 'Administrator').first()
    return True if admin_user else False

# Verifica las credenciales de login
async def verify_login(username, passwd):
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        is_verified = await verify_passwd(passwd, user.passwd)
        return True if is_verified else False
    
    return False

# Encripta la contraseña
async def encrypt_passwd(passwd):
    hash_passwd = pbkdf2_sha256.hash(passwd)
    return hash_passwd

# Verifica si la contraseña concuerda con la del hash
async def verify_passwd(passwd, hash):
    return pbkdf2_sha256.verify(passwd, hash)