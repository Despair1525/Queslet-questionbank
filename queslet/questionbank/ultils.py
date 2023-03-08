
import time

def get_time():
    t = time.time()
    t_s = int(t)
    return str(t_s)

def isManger(User):
    if User.is_superuser:
        return True
    return User.groups.filter(name='manager').exists() 