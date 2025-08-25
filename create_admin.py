#!/usr/bin/env python3
"""
Script to create an admin user for the Skill2Wealth platform
Run this script to create your first admin user who can access the admin panel
"""

from app import create_app
from app.models import User
from app.extensions import db

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print("✅ Admin user already exists!")
            print(f"Username: {admin_user.username}")
            print(f"Email: {admin_user.email}")
            return
        
        # Create admin user
        print("Creating admin user...")
        
        # Get admin details
        email = input("Enter admin email: ").strip()
        password = input("Enter admin password: ").strip()
        
        if not email or not password:
            print("❌ Email and password are required!")
            return
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print("❌ A user with this email already exists!")
            return
        
        # Create the admin user
        admin_user = User(
            username='admin',
            email=email
        )
        admin_user.set_password(password)
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created successfully!")
            print(f"Username: admin")
            print(f"Email: {email}")
            print("\nYou can now login and access the admin panel at: /admin")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {e}")

if __name__ == '__main__':
    create_admin_user()
