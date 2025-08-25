#!/usr/bin/env python3
"""
Admin Management Script for Skill2Wealth Platform
- Create new admin user
- Edit existing admin user
- Reset admin password
- List admin users
"""

from app import create_app
from app.models import User
from app.extensions import db

def create_admin():
    """Create a new admin user"""
    print("\n=== Create Admin User ===")
    
    # Check if admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    
    if admin_user:
        print("✅ Admin user already exists!")
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print("\nUse option 2 to edit the existing admin user.")
        return
    
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
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating admin user: {e}")

def edit_admin():
    """Edit existing admin user"""
    print("\n=== Edit Admin User ===")
    
    admin_user = User.query.filter_by(username='admin').first()
    
    if not admin_user:
        print("❌ No admin user found! Create one first.")
        return
    
    print(f"Current admin details:")
    print(f"Username: {admin_user.username}")
    print(f"Email: {admin_user.email}")
    print(f"Created: {admin_user.created_at}")
    
    print("\nWhat would you like to edit?")
    print("1. Change email")
    print("2. Change password")
    print("3. Change both email and password")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        new_email = input("Enter new email: ").strip()
        if new_email:
            # Check if email already exists
            existing = User.query.filter(User.email == new_email, User.id != admin_user.id).first()
            if existing:
                print("❌ This email is already used by another user!")
                return
            
            admin_user.email = new_email
            try:
                db.session.commit()
                print("✅ Email updated successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error updating email: {e}")
    
    elif choice == "2":
        new_password = input("Enter new password: ").strip()
        if new_password:
            admin_user.set_password(new_password)
            try:
                db.session.commit()
                print("✅ Password updated successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error updating password: {e}")
    
    elif choice == "3":
        new_email = input("Enter new email: ").strip()
        new_password = input("Enter new password: ").strip()
        
        if new_email and new_password:
            # Check if email already exists
            existing = User.query.filter(User.email == new_email, User.id != admin_user.id).first()
            if existing:
                print("❌ This email is already used by another user!")
                return
            
            admin_user.email = new_email
            admin_user.set_password(new_password)
            try:
                db.session.commit()
                print("✅ Email and password updated successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error updating admin user: {e}")
    else:
        print("❌ Invalid choice!")

def list_admins():
    """List all admin users"""
    print("\n=== Admin Users ===")
    
    admin_users = User.query.filter_by(username='admin').all()
    
    if not admin_users:
        print("❌ No admin users found!")
        return
    
    for i, admin in enumerate(admin_users, 1):
        print(f"{i}. Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Created: {admin.created_at}")
        print(f"   ID: {admin.id}")
        print()

def delete_admin():
    """Delete admin user (with confirmation)"""
    print("\n=== Delete Admin User ===")
    
    admin_user = User.query.filter_by(username='admin').first()
    
    if not admin_user:
        print("❌ No admin user found!")
        return
    
    print(f"⚠️  WARNING: You are about to delete the admin user:")
    print(f"Username: {admin_user.username}")
    print(f"Email: {admin_user.email}")
    
    confirm = input("\nType 'DELETE' to confirm: ").strip()
    
    if confirm == 'DELETE':
        try:
            db.session.delete(admin_user)
            db.session.commit()
            print("✅ Admin user deleted successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error deleting admin user: {e}")
    else:
        print("❌ Deletion cancelled.")

def main():
    """Main menu"""
    app = create_app()
    
    with app.app_context():
        while True:
            print("\n" + "="*50)
            print("🔧 SKILL2WEALTH ADMIN MANAGEMENT")
            print("="*50)
            print("1. Create admin user")
            print("2. Edit admin user")
            print("3. List admin users")
            print("4. Delete admin user")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                create_admin()
            elif choice == "2":
                edit_admin()
            elif choice == "3":
                list_admins()
            elif choice == "4":
                delete_admin()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter 1-5.")

if __name__ == '__main__':
    main()
