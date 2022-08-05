from dotenv import load_dotenv
import os

load_dotenv()

client = os.getenv("CLIENT_ID")
secret = os.getenv("CLIENT_SECRET")

def print_env():
    print(f'Client id: {client}')
    print(f'Secret id: {secret}')

if __name__ == "__main__":
    print_env()