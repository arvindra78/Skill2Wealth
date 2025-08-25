import os
from flask import send_from_directory, abort, current_app
from flask_login import login_required, current_user
from . import main_bp
from ..models import Order

@main_bp.route('/content/ebooks/<filename>')
@login_required
def serve_ebook(filename):
    """Serve ebook files to authenticated users who have purchased them"""
    # Check if user is admin - no payment required
    from ..admin.routes import is_admin
    if is_admin(current_user):
        content_dir = os.path.join(current_app.root_path, '..', 'content', 'ebooks')
        return send_from_directory(content_dir, filename)
    
    # Check if user has purchased this ebook
    ebook_path = f"/content/ebooks/{filename}"
    
    # Find order with this file
    order = Order.query.join(Order.product).filter(
        Order.user_id == current_user.id,
        Order.payment_status == 'completed',
        Order.product.has(file_url=ebook_path)
    ).first()
    
    if not order:
        abort(403)  # Forbidden - user hasn't purchased this content
    
    # Serve the file
    content_dir = os.path.join(current_app.root_path, '..', 'content', 'ebooks')
    return send_from_directory(content_dir, filename)

@main_bp.route('/content/videos/<filename>')
@login_required
def serve_video(filename):
    """Serve video files to authenticated users who have purchased them"""
    # Check if user is admin - no payment required
    from ..admin.routes import is_admin
    if is_admin(current_user):
        content_dir = os.path.join(current_app.root_path, '..', 'content', 'videos')
        return send_from_directory(content_dir, filename)
    
    # Check if user has purchased this course
    video_path = f"/content/videos/{filename}"
    
    # Find order with this file
    order = Order.query.join(Order.product).filter(
        Order.user_id == current_user.id,
        Order.payment_status == 'completed',
        Order.product.has(file_url=video_path)
    ).first()
    
    if not order:
        abort(403)  # Forbidden - user hasn't purchased this content
    
    # Serve the file
    content_dir = os.path.join(current_app.root_path, '..', 'content', 'videos')
    return send_from_directory(content_dir, filename)

# Admin content serving (no purchase check)
@main_bp.route('/admin/content/ebooks/<filename>')
@login_required
def admin_serve_ebook(filename):
    """Serve ebook files for admin preview"""
    from ..admin.routes import is_admin
    if not is_admin(current_user):
        abort(403)
    
    content_dir = os.path.join(current_app.root_path, '..', 'content', 'ebooks')
    return send_from_directory(content_dir, filename)

@main_bp.route('/admin/content/videos/<filename>')
@login_required
def admin_serve_video(filename):
    """Serve video files for admin preview"""
    from ..admin.routes import is_admin
    if not is_admin(current_user):
        abort(403)
    
    content_dir = os.path.join(current_app.root_path, '..', 'content', 'videos')
    return send_from_directory(content_dir, filename)
