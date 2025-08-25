#!/usr/bin/env python3
"""
Quick admin setup - creates admin user and tests access
"""

from app import create_app
from app.models import User
from app.extensions import db

def setup_admin():
    app = create_app()
    
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print(f"✅ Admin user exists: {admin.email}")
        else:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@skill2wealth.com'
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created!")
            print("Email: admin@skill2wealth.com")
            print("Password: admin123")
        
        print("\n🚀 Next steps:")
        print("1. Run: python run.py")
        print("2. Go to: http://localhost:5000/auth/login")
        print("3. Login with admin credentials")
        print("4. Access admin panel: http://localhost:5000/admin")

if __name__ == '__main__':
    setup_admin()
