import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    # Use absolute path for database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "instance", "skill2wealth.sqlite")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_R9O0qNXALduHdh')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'Cxi948W6ufBwUyUgicg3mCuV')
    # Directory to store eBooks (for MVP eBook store)
    EBOOKS_DIR = os.getenv('EBOOKS_DIR', os.path.join(BASE_DIR, "ebooks"))
