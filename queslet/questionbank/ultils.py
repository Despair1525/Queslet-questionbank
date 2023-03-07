def isManger(User):
    if User.is_superuser:
        return True
    return User.groups.filter(name='manager').exists() 