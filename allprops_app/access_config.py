import os
import random
import string

ACCESS_CODE_FILE = os.path.join(os.path.dirname(__file__), 'access_code.txt')

def generate_random_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_access_code():
    if os.path.exists(ACCESS_CODE_FILE):
        with open(ACCESS_CODE_FILE, 'r') as f:
            return f.read().strip()
    else:
        new_code = generate_random_code()
        with open(ACCESS_CODE_FILE, 'w') as f:
            f.write(new_code)
        return new_code

DAILY_ACCESS_CODE = get_access_code()
