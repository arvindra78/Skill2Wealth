from flask import render_template, send_file, abort, redirect
from flask_login import login_required, current_user
from . import dashboard_bp
from ..models import Order, Product
import os

@dashboard_bp.route('/')
@login_required
def dashboard_home():
    # Get user's completed orders
    completed_orders = Order.query.filter_by(
        user_id=current_user.id, 
        payment_status='completed'
    ).all()
    
    return render_template('dashboard.html', orders=completed_orders)

@dashboard_bp.route('/download/<int:order_id>')
@login_required
def download_content(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order
    if order.user_id != current_user.id:
        abort(403)
    
    # Check if payment is completed
    if order.payment_status != 'completed':
        abort(400)
    
    # Check if product has a file
    if not order.product.file_url:
        abort(404)
    
    # For now, we'll just redirect to the file URL
    # In production, you might want to serve files securely
    return redirect(order.product.file_url)

@dashboard_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@dashboard_bp.route('/orders')
@login_required
def orders():
    # Get all user's orders
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)
