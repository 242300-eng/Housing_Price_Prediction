from dotenv import load_dotenv
import os

load_dotenv()
print(f"CLERK_PUBLISHABLE_KEY: {os.getenv('CLERK_PUBLISHABLE_KEY')}")
print(f"CLERK_SECRET_KEY: {os.getenv('CLERK_SECRET_KEY')}")
