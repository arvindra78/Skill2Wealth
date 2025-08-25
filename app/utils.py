"""
Utility functions for payment processing and other helper functions
"""
import razorpay
import hmac
import hashlib
from flask import current_app

def create_razorpay_order(amount, currency='INR'):
    """Create a Razorpay order"""
    try:
        client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))
        order_data = {
            'amount': int(amount * 100),  # Amount in paise
            'currency': currency,
            'payment_capture': 1
        }
        order = client.order.create(data=order_data)
        return order
    except Exception as e:
        current_app.logger.error(f"Razorpay order creation failed: {str(e)}")
        return None

def verify_razorpay_signature(payment_id, order_id, signature):
    """Verify Razorpay payment signature"""
    try:
        key_secret = current_app.config['RAZORPAY_KEY_SECRET']
        body = order_id + "|" + payment_id
        generated_signature = hmac.new(
            key_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(generated_signature, signature)
    except Exception as e:
        current_app.logger.error(f"Razorpay signature verification failed: {str(e)}")
        return False

def get_razorpay_payment_details(payment_id):
    """Get payment details from Razorpay"""
    try:
        client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))
        payment = client.payment.fetch(payment_id)
        return payment
    except Exception as e:
        current_app.logger.error(f"Failed to fetch Razorpay payment details: {str(e)}")
        return None
