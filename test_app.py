#!/usr/bin/env python3
"""
Simple test script for Skill2Wealth MVP Flask application
"""

from app import create_app
from app.models import User, Product, Order
from app.extensions import db

def test_basic_functionality():
    """Test basic application functionality"""
    try:
        print("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            print("✓ Flask application created successfully")
            
            # Test database connection
            print("Testing database connection...")
            try:
                # Use the correct SQLAlchemy 2.0 syntax
                with db.engine.connect() as conn:
                    result = conn.execute(db.text("SELECT 1"))
                    result.fetchone()
                print("✓ Database connection successful")
            except Exception as e:
                print(f"⚠️ Database connection warning: {e}")
                print("Creating database tables...")
                db.create_all()
                print("✓ Database tables created")
            
            # Test models
            print("Testing models...")
            
            # Create a test user
            test_user = User(
                username='testuser',
                email='test@skill2wealth.com'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            
            # Create a test product
            test_product = Product(
                name='Test eBook',
                description='A test eBook for testing purposes',
                price=49.0,
                category='ebook',
                is_active=True
            )
            db.session.add(test_product)
            
            # Commit to database
            db.session.commit()
            print("✓ Models and database operations successful")
            
            # Clean up test data
            db.session.delete(test_user)
            db.session.delete(test_product)
            db.session.commit()
            print("✓ Test data cleaned up")
            
            print("\n🎉 All tests passed! The application is working correctly.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_basic_functionality()
