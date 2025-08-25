from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from . import store_bp
from ..models import Product, Order
from ..extensions import db
from ..utils import create_razorpay_order, verify_razorpay_signature, get_razorpay_payment_details
import razorpay
import hmac
import hashlib
from datetime import datetime

# Static product data for MVP
STATIC_PRODUCTS = {
    201: {
        'id': 201,
        'name': 'Trading Starter Course',
        'title': 'Trading Starter Course',
        'description': 'Complete beginner course with video lessons and PDF materials in Hindi + Hinglish. Perfect for students starting their trading journey.',
        'price': 199.0,
        'category': 'course',
        'detailed_description': 'Comprehensive video course designed specifically for Indian students who want to start their trading journey. This course covers everything from the basics to advanced concepts, with practical examples from Indian markets, all explained in Hindi + Hinglish.',
        'features': [
            '10+ hours of HD video content',
            'Step-by-step trading tutorials',
            'Live market examples and case studies',
            'Downloadable PDF resources',
            'Indian market focus (NSE/BSE)',
            'Mobile trading app tutorials'
        ],
        'language': 'Hindi + Hinglish',
        'duration': '10+ hours',
        'format': 'HD Video + PDF',
        'image_url': '/static/images/products/trading-starter-course.jpg',
        'file_url': '/content/videos/trading-starter-course/',
        'additional_files': [
            '/content/ebooks/trading-starter-course-materials.pdf',
            '/content/videos/trading-starter-course/lesson-01-intro.mp4',
            '/content/videos/trading-starter-course/lesson-02-basics.mp4',
            '/content/videos/trading-starter-course/lesson-03-analysis.mp4'
        ]
    },
    202: {
        'id': 202,
        'name': 'Advanced Trading Course',
        'title': 'Advanced Trading Course',
        'description': 'Advanced strategies and techniques with real market examples. Hindi + Hinglish content for serious traders.',
        'price': 299.0,
        'category': 'course',
        'detailed_description': 'Take your trading to the next level with advanced strategies, risk management techniques, and professional trading methods. This course is designed for traders who have completed the basics and want to develop professional-level skills.',
        'features': [
            '15+ hours of advanced video content',
            'Professional trading strategies',
            'Advanced technical analysis',
            'Risk management mastery',
            'Portfolio management techniques',
            'Real-time market analysis sessions'
        ],
        'language': 'Hindi + Hinglish',
        'duration': '15+ hours',
        'format': 'HD Video + PDF',
        'image_url': '/static/images/products/advanced-trading-course.jpg',
        'file_url': '/content/videos/advanced-trading-course/',
        'additional_files': [
            '/content/ebooks/advanced-trading-course-materials.pdf',
            '/content/videos/advanced-trading-course/module-01-strategies.mp4',
            '/content/videos/advanced-trading-course/module-02-risk-management.mp4',
            '/content/videos/advanced-trading-course/module-03-portfolio.mp4'
        ]
    }
}

def get_product_by_id(product_id):
    """Get product from database or static products"""
    # First try to get from database
    db_product = Product.query.filter_by(id=product_id).first()
    if db_product:
        return db_product
    
    # If not in database, check static products
    if product_id in STATIC_PRODUCTS:
        # Create a product-like object from static data
        static_data = STATIC_PRODUCTS[product_id]
        
        class StaticProduct:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)
        
        return StaticProduct(static_data)
    
    return None

@store_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('main.store'))
    return render_template('product_detail.html', product=product)

@store_bp.route('/buy/<int:product_id>', methods=['GET', 'POST'])
@login_required
def buy(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('main.store'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        
        # Create order
        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            amount=product.price,
            payment_method=payment_method
        )
        db.session.add(order)
        db.session.commit()
        
        # Only Razorpay is supported
        if payment_method == 'razorpay':
            # Create Razorpay order
            razorpay_order = create_razorpay_order(product.price)
            if razorpay_order:
                order.razorpay_order_id = razorpay_order['id']
                db.session.commit()
                return render_template('razorpay_payment.html', 
                                     order=order, 
                                     product=product,
                                     razorpay_order=razorpay_order,
                                     razorpay_key=current_app.config['RAZORPAY_KEY_ID'])
            else:
                flash('Payment initialization failed', 'error')
                return redirect(url_for('store.buy', product_id=product.id))
        else:
            # Invalid payment method
            flash('Invalid payment method. Only Razorpay is supported.', 'error')
            return redirect(url_for('store.buy', product_id=product.id))
    
    return render_template('buy.html', product=product)

@store_bp.route('/payment/razorpay/<int:order_id>')
@login_required
def razorpay_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
    
    # Temporarily redirect to success for testing
    flash('Razorpay integration coming soon!', 'info')
    return redirect(url_for('store.payment_success', order_id=order.id))

# Stripe payment route removed - only Razorpay is supported

@store_bp.route('/payment/success/<int:order_id>')
@login_required
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
    
    order.payment_status = 'completed'
    db.session.commit()
    
    flash('Payment successful! You can now download your content.', 'success')
    return render_template('purchase_success.html', order=order)

@store_bp.route('/payment/cancel/<int:order_id>')
@login_required
def payment_cancel(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
    
    flash('Payment was cancelled', 'info')
    return redirect(url_for('store.buy', product_id=order.product_id))

@store_bp.route('/payment/verify', methods=['POST'])
@login_required
def verify_payment():
    """Verify Razorpay payment signature"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')
        
        # Get the order
        order = Order.query.get_or_404(order_id)
        if order.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 403
        
        # Verify the payment signature
        if verify_razorpay_signature(razorpay_payment_id, razorpay_order_id, razorpay_signature):
            # Update order with payment details
            order.payment_status = 'completed'
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.transaction_id = razorpay_payment_id
            
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Payment verified successfully'})
        else:
            # Payment verification failed
            order.payment_status = 'failed'
            db.session.commit()
            
            return jsonify({'success': False, 'error': 'Payment verification failed'}), 400
            
    except Exception as e:
        current_app.logger.error(f"Payment verification error: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@store_bp.route('/payment/failed', methods=['POST'])
def payment_failed():
    """Handle failed payments"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        error_details = data.get('error', {})
        
        # Get the order
        order = Order.query.get_or_404(order_id)
        order.payment_status = 'failed'
        
        db.session.commit()
        
        current_app.logger.error(f"Payment failed for order {order_id}: {error_details}")
        
        return jsonify({'success': True, 'message': 'Payment status updated'})
        
    except Exception as e:
        current_app.logger.error(f"Error handling failed payment: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@store_bp.route('/webhook/razorpay', methods=['POST'])
def razorpay_webhook():
    """Handle Razorpay webhooks"""
    try:
        # Get webhook signature from headers
        webhook_signature = request.headers.get('X-Razorpay-Signature')
        webhook_secret = current_app.config.get('RAZORPAY_WEBHOOK_SECRET')
        
        if webhook_secret:
            # Verify webhook signature if secret is configured
            webhook_body = request.get_data()
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                webhook_body,
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_signature, webhook_signature):
                current_app.logger.warning("Razorpay webhook signature verification failed")
                return jsonify({'error': 'Invalid signature'}), 400
        
        # Process webhook data
        data = request.get_json()
        event = data.get('event')
        
        if event == 'payment.captured':
            payment_data = data.get('payload', {}).get('payment', {}).get('entity', {})
            razorpay_order_id = payment_data.get('order_id')
            razorpay_payment_id = payment_data.get('id')
            
            # Find order by razorpay_order_id
            order = Order.query.filter_by(razorpay_order_id=razorpay_order_id).first()
            if order:
                order.payment_status = 'completed'
                order.razorpay_payment_id = razorpay_payment_id
                order.transaction_id = razorpay_payment_id
                db.session.commit()
                
                current_app.logger.info(f"Payment captured for order {order.id}")
        
        elif event == 'payment.failed':
            payment_data = data.get('payload', {}).get('payment', {}).get('entity', {})
            razorpay_order_id = payment_data.get('order_id')
            
            # Find order by razorpay_order_id
            order = Order.query.filter_by(razorpay_order_id=razorpay_order_id).first()
            if order:
                order.payment_status = 'failed'
                db.session.commit()
                
                current_app.logger.info(f"Payment failed for order {order.id}")
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        current_app.logger.error(f"Razorpay webhook error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
