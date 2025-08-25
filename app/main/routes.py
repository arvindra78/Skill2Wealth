from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from . import main_bp
from ..models import Product
from ..extensions import db

# Static product data for MVP
STATIC_PRODUCTS = {
    # Courses removed - add new ones here when needed
}

def get_static_products(category=None):
    """Get static products, optionally filtered by category"""
    static_products = []
    for product_data in STATIC_PRODUCTS.values():
        if category is None or product_data['category'] == category:
            class StaticProduct:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)
            static_products.append(StaticProduct(product_data))
    return static_products

@main_bp.route('/')
def index():
    try:
        # Get featured products for homepage
        featured_products = Product.query.filter_by(is_active=True).limit(4).all()
    except Exception as e:
        print(f"Database error in index route: {e}")
        try:
            db.create_all()
            featured_products = Product.query.filter_by(is_active=True).limit(4).all()
        except Exception as e2:
            print(f"Failed to initialize database: {e2}")
            featured_products = []
            flash('Database connection issue. Please contact support.', 'error')
    
    return render_template('index.html', products=featured_products)


@main_bp.route('/ebooks')
def ebooks():
    """Dedicated eBooks page"""
    try:
        db_ebooks = Product.query.filter_by(category='ebook', is_active=True).all()
    except Exception as e:
        print(f"Database error in ebooks route: {e}")
        try:
            db.create_all()
            db_ebooks = Product.query.filter_by(category='ebook', is_active=True).all()
        except Exception:
            db_ebooks = []
            flash('Unable to load eBooks. Please try again later.', 'error')
    
    # Add static ebooks
    static_ebooks = get_static_products('ebook')
    all_ebooks = list(db_ebooks) + static_ebooks
    
    return render_template('ebooks.html', ebooks=all_ebooks)

@main_bp.route('/courses')
def courses():
    """Dedicated courses page"""
    try:
        db_courses = Product.query.filter_by(category='course', is_active=True).all()
    except Exception as e:
        print(f"Database error in courses route: {e}")
        try:
            db.create_all()
            db_courses = Product.query.filter_by(category='course', is_active=True).all()
        except Exception:
            db_courses = []
            flash('Unable to load courses. Please try again later.', 'error')
    
    # Add static courses
    static_courses = get_static_products('course')
    all_courses = list(db_courses) + static_courses
    
    return render_template('courses.html', courses=all_courses)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')
