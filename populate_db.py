#!/usr/bin/env python3
"""
Database Population Script for Skill2Wealth MVP
This script creates sample products and users for testing the platform.
"""

from app import create_app
from app.models import User, Product, Order
from app.extensions import db
from werkzeug.security import generate_password_hash

def populate_database():
    """Populate the database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Order.query.delete()
        Product.query.delete()
        User.query.delete()
        
        # Create sample users
        print("Creating sample users...")
        admin_user = User(
            username='admin',
            email='admin@skill2wealth.com'
        )
        admin_user.set_password('admin123')
        
        test_user = User(
            username='testuser',
            email='test@skill2wealth.com'
        )
        test_user.set_password('test123')
        
        db.session.add(admin_user)
        db.session.add(test_user)
        
        # Create sample products
        print("Creating sample products...")
        
        # eBooks
        trading_ebook = Product(
            name='Trading Fundamentals for Beginners',
            description='A comprehensive guide to understanding the basics of trading, including market analysis, risk management, and trading psychology. Perfect for students aged 18-28 who want to start their trading journey.',
            price=49.0,
            category='ebook',
            image_url='',
            file_url='https://example.com/trading-fundamentals.pdf',
            is_active=True
        )
        
        psychology_ebook = Product(
            name='Trading Psychology & Mindset',
            description='Master the mental aspects of trading with this essential guide. Learn how to control emotions, build discipline, and develop the mindset of successful traders.',
            price=49.0,
            category='ebook',
            image_url='',
            file_url='https://example.com/trading-psychology.pdf',
            is_active=True
        )
        
        motivation_ebook = Product(
            name='Motivation & Success in Trading',
            description='Stay motivated and focused on your trading goals. This eBook provides practical strategies for maintaining momentum and achieving long-term success.',
            price=49.0,
            category='ebook',
            image_url='',
            file_url='https://example.com/motivation-success.pdf',
            is_active=True
        )
        
        # Trading Courses
        starter_course = Product(
            name='Trading Starter Course',
            description='Complete beginner-friendly course with video lessons, PDF materials, and practical examples. Learn trading from scratch with step-by-step guidance.',
            price=199.0,
            category='course',
            image_url='',
            file_url='https://example.com/trading-starter-course.zip',
            is_active=True
        )
        
        technical_course = Product(
            name='Technical Analysis Mastery',
            description='Advanced course covering chart patterns, indicators, and technical analysis strategies. Perfect for traders who want to take their skills to the next level.',
            price=299.0,
            category='course',
            image_url='',
            file_url='https://example.com/technical-analysis-course.zip',
            is_active=True
        )
        
        # Add products to session
        db.session.add(trading_ebook)
        db.session.add(psychology_ebook)
        db.session.add(motivation_ebook)
        db.session.add(starter_course)
        db.session.add(technical_course)
        
        # Create sample orders
        print("Creating sample orders...")
        
        # Sample order for test user
        sample_order = Order(
            user_id=2,  # test_user
            product_id=1,  # trading_ebook
            amount=49.0,
            payment_method='razorpay',
            payment_status='completed',
            transaction_id='TXN123456789'
        )
        
        db.session.add(sample_order)
        
        # Commit all changes
        print("Committing changes to database...")
        db.session.commit()
        
        print("Database populated successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Product.query.count()} products")
        print(f"Created {Order.query.count()} orders")
        
        # Print product details
        print("\nProducts created:")
        for product in Product.query.all():
            print(f"- {product.name} (₹{product.price}) - {product.category}")

if __name__ == '__main__':
    populate_database()
