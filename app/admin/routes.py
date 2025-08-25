import os
import uuid
from flask import render_template, request, redirect, url_for, flash, current_app, jsonify, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import admin_bp
from ..models import Product, User
from ..extensions import db
from datetime import datetime

# File upload configuration
ALLOWED_EXTENSIONS = {
    'pdf': ['pdf'],
    'video': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'],
    'image': ['jpg', 'jpeg', 'png', 'gif', 'webp']
}

def allowed_file(filename, file_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(file_type, [])

def is_admin(user):
    """Check if user is admin - for now, check if username is 'admin'"""
    return user.is_authenticated and user.username == 'admin'

@admin_bp.before_request
def require_admin():
    """Require admin access for all admin routes"""
    if not current_user.is_authenticated:
        flash('Please login to access admin panel', 'error')
        return redirect(url_for('auth.login'))
    
    if not is_admin(current_user):
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))

@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    total_products = Product.query.count()
    total_ebooks = Product.query.filter_by(category='ebook').count()
    total_courses = Product.query.filter_by(category='course').count()
    total_users = User.query.count()
    
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_ebooks=total_ebooks,
                         total_courses=total_courses,
                         total_users=total_users,
                         recent_products=recent_products)

@admin_bp.route('/products')
def products():
    """List all products"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('admin/products.html', products=products, category=category)

@admin_bp.route('/upload')
def upload_form():
    """Show upload form"""
    return render_template('admin/upload.html')

@admin_bp.route('/upload', methods=['POST'])
def upload_content():
    """Handle content upload"""
    try:
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        category = request.form.get('category')
        
        if not all([name, description, category]):
            flash('All fields are required', 'error')
            return redirect(url_for('admin.upload_form'))
        
        # Handle file uploads
        content_file = request.files.get('content_file')
        image_file = request.files.get('image_file')
        
        file_url = None
        image_url = None
        
        # Upload content file
        if content_file and content_file.filename:
            if category == 'ebook' and allowed_file(content_file.filename, 'pdf'):
                filename = secure_filename(content_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(current_app.root_path, '..', 'content', 'ebooks', unique_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                content_file.save(file_path)
                file_url = f"/content/ebooks/{unique_filename}"
                
            elif category == 'course' and allowed_file(content_file.filename, 'video'):
                filename = secure_filename(content_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(current_app.root_path, '..', 'content', 'videos', unique_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                content_file.save(file_path)
                file_url = f"/content/videos/{unique_filename}"
            else:
                flash(f'Invalid file type for {category}', 'error')
                return redirect(url_for('admin.upload_form'))
        
        # Upload image file
        if image_file and image_file.filename and allowed_file(image_file.filename, 'image'):
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Create static/images/products directory if it doesn't exist
            images_dir = os.path.join(current_app.root_path, 'static', 'images', 'products')
            os.makedirs(images_dir, exist_ok=True)
            
            file_path = os.path.join(images_dir, unique_filename)
            image_file.save(file_path)
            image_url = f"/static/images/products/{unique_filename}"
        
        # Create product in database
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            file_url=file_url,
            image_url=image_url,
            is_active=True
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'{category.title()} uploaded successfully!', 'success')
        return redirect(url_for('admin.products'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('admin.upload_form'))

@admin_bp.route('/product/<int:product_id>/edit')
def edit_product(product_id):
    """Edit product form"""
    product = Product.query.get_or_404(product_id)
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/product/<int:product_id>/edit', methods=['POST'])
def update_product(product_id):
    """Update product"""
    product = Product.query.get_or_404(product_id)
    
    try:
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price', 0))
        product.is_active = 'is_active' in request.form
        
        # Handle new file uploads
        content_file = request.files.get('content_file')
        image_file = request.files.get('image_file')
        
        # Update content file if provided
        if content_file and content_file.filename:
            if product.category == 'ebook' and allowed_file(content_file.filename, 'pdf'):
                filename = secure_filename(content_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(current_app.root_path, '..', 'content', 'ebooks', unique_filename)
                
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                content_file.save(file_path)
                product.file_url = f"/content/ebooks/{unique_filename}"
                
            elif product.category == 'course' and allowed_file(content_file.filename, 'video'):
                filename = secure_filename(content_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(current_app.root_path, '..', 'content', 'videos', unique_filename)
                
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                content_file.save(file_path)
                product.file_url = f"/content/videos/{unique_filename}"
        
        # Update image if provided
        if image_file and image_file.filename and allowed_file(image_file.filename, 'image'):
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            images_dir = os.path.join(current_app.root_path, 'static', 'images', 'products')
            os.makedirs(images_dir, exist_ok=True)
            
            file_path = os.path.join(images_dir, unique_filename)
            image_file.save(file_path)
            product.image_url = f"/static/images/products/{unique_filename}"
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Update failed: {str(e)}', 'error')
        return redirect(url_for('admin.edit_product', product_id=product_id))

@admin_bp.route('/product/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    
    try:
        # Delete associated files
        if product.file_url:
            file_path = os.path.join(current_app.root_path, '..', product.file_url.lstrip('/'))
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if product.image_url and product.image_url.startswith('/static/'):
            image_path = os.path.join(current_app.root_path, product.image_url.lstrip('/'))
            if os.path.exists(image_path):
                os.remove(image_path)
        
        db.session.delete(product)
        db.session.commit()
        
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Delete failed: {str(e)}', 'error')
    
    return redirect(url_for('admin.products'))

@admin_bp.route('/bulk-upload')
def bulk_upload_form():
    """Bulk upload form"""
    return render_template('admin/bulk_upload.html')

@admin_bp.route('/bulk-upload', methods=['POST'])
def bulk_upload():
    """Handle bulk upload of multiple files"""
    try:
        files = request.files.getlist('files')
        category = request.form.get('category')
        
        if not files or not category:
            flash('Please select files and category', 'error')
            return redirect(url_for('admin.bulk_upload_form'))
        
        uploaded_count = 0
        
        for file in files:
            if file and file.filename:
                # Generate product name from filename
                name = os.path.splitext(file.filename)[0].replace('_', ' ').replace('-', ' ').title()
                
                # Save file
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                
                if category == 'ebook' and allowed_file(file.filename, 'pdf'):
                    file_path = os.path.join(current_app.root_path, '..', 'content', 'ebooks', unique_filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    file_url = f"/content/ebooks/{unique_filename}"
                    
                elif category == 'course' and allowed_file(file.filename, 'video'):
                    file_path = os.path.join(current_app.root_path, '..', 'content', 'videos', unique_filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    file_url = f"/content/videos/{unique_filename}"
                else:
                    continue  # Skip invalid files
                
                # Create product
                product = Product(
                    name=name,
                    description=f"Auto-uploaded {category}",
                    price=49.0,  # Default price
                    category=category,
                    file_url=file_url,
                    is_active=False  # Require manual activation
                )
                
                db.session.add(product)
                uploaded_count += 1
        
        db.session.commit()
        flash(f'Successfully uploaded {uploaded_count} files!', 'success')
        return redirect(url_for('admin.products'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Bulk upload failed: {str(e)}', 'error')
        return redirect(url_for('admin.bulk_upload_form'))
