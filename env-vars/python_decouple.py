from decouple import config

API_USERNAME = config('CLIENT_ID')
API_KEY = config('CLIENT_SECRET')

def print_env():
    print(f'Client id: {API_USERNAME}')
    print(f'Secret id: {API_KEY}')

if __name__ == "__main__":
    print_env()