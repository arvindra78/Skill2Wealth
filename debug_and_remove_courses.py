#!/usr/bin/env python3
"""
Script to debug and properly remove courses from the Skill2Wealth database
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import Product, Order, db

def debug_and_remove_courses():
    """Debug and remove all courses from the database"""
    app = create_app()
    
    with app.app_context():
        try:
            # First, let's see all products in the database
            all_products = Product.query.all()
            print(f"Total products in database: {len(all_products)}")
            
            courses = []
            for product in all_products:
                print(f"- {product.name} | Category: {product.category} | Price: ₹{product.price} | ID: {product.id}")
                if product.category == 'course' or 'course' in product.name.lower() or 'trading' in product.name.lower():
                    courses.append(product)
            
            print(f"\nFound {len(courses)} course-related products to remove:")
            for course in courses:
                print(f"  - {course.name} (ID: {course.id})")
            
            if not courses:
                print("No courses found to remove.")
                return True
            
            # Remove related orders first
            course_ids = [course.id for course in courses]
            orders_to_remove = Order.query.filter(Order.product_id.in_(course_ids)).all()
            
            if orders_to_remove:
                print(f"\nRemoving {len(orders_to_remove)} related orders...")
                for order in orders_to_remove:
                    print(f"  - Order ID: {order.id}")
                    db.session.delete(order)
            
            # Remove courses
            print(f"\nRemoving {len(courses)} courses...")
            for course in courses:
                print(f"  - Removing: {course.name}")
                db.session.delete(course)
            
            # Commit changes
            db.session.commit()
            print("\n✓ Successfully removed all courses!")
            
            # Verify removal
            remaining_products = Product.query.all()
            print(f"\nRemaining products after removal: {len(remaining_products)}")
            for product in remaining_products:
                print(f"  - {product.name} | Category: {product.category}")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    print("Debugging and removing courses from Skill2Wealth database...")
    print("=" * 60)
    
    success = debug_and_remove_courses()
    
    if success:
        print("\n" + "=" * 60)
        print("Course removal completed successfully!")
    else:
        print("\n" + "=" * 60)
        print("Course removal failed.")
