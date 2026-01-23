"""
Seed database with sample problems and test cases
Run: python -m scripts.seed_data
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.problem import Problem
from app.models.user import User
from app.core.security import hash_password


def create_sample_problems(db: Session):
    """Create sample programming problems"""
    
    # Problem 1: Two Sum
    two_sum = Problem(
        title="Two Sum",
        slug="two-sum",
        description="""Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: 2 7 11 15
       9
Output: 0 1

Example 2:
Input: 3 2 4
       6
Output: 1 2""",
        difficulty="EASY",
        category="Arrays",
        tags=["array", "hash-table"],
        time_limit_ms=2000,
        memory_limit_mb=128
    )
    
    # Problem 2: Reverse String
    reverse_string = Problem(
        title="Reverse String",
        slug="reverse-string",
        description="""Write a function that reverses a string. The input string is given as an array of characters.

You must do this by modifying the input array in-place with O(1) extra memory.

Example 1:
Input: hello
Output: olleh

Example 2:
Input: world
Output: dlrow""",
        difficulty="EASY",
        category="Strings",
        tags=["string", "two-pointers"],
        time_limit_ms=1000,
        memory_limit_mb=64
    )
    
    # Problem 3: Fizz Buzz
    fizz_buzz = Problem(
        title="Fizz Buzz",
        slug="fizz-buzz",
        description="""Given an integer n, return a list of strings where:
- For multiples of 3, print "Fizz"
- For multiples of 5, print "Buzz"  
- For multiples of both 3 and 5, print "FizzBuzz"
- Otherwise, print the number

Return the list for all numbers from 1 to n.

Example:
Input: 15
Output: 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz""",
        difficulty="EASY",
        category="Math",
        tags=["math", "string"],
        time_limit_ms=1000,
        memory_limit_mb=64
    )
    
    # Problem 4: Palindrome Number
    palindrome = Problem(
        title="Palindrome Number",
        slug="palindrome-number",
        description="""Given an integer x, return true if x is a palindrome, and false otherwise.

An integer is a palindrome when it reads the same forward and backward.

Example 1:
Input: 121
Output: true

Example 2:
Input: -121
Output: false

Example 3:
Input: 10
Output: false""",
        difficulty="EASY",
        category="Math",
        tags=["math"],
        time_limit_ms=1000,
        memory_limit_mb=64
    )
    
    # Add problems to database
    db.add(two_sum)
    db.add(reverse_string)
    db.add(fizz_buzz)
    db.add(palindrome)
    db.commit()
    
    print("✅ Created 4 sample problems")


def create_admin_user(db: Session):
    """Create an admin user for testing"""
    existing_admin = db.query(User).filter(User.username == "admin").first()
    
    if not existing_admin:
        admin = User(
            username="admin",
            email="admin@codearena.com",
            password_hash=hash_password("admin123"),
            bio="Platform Administrator"
        )
        db.add(admin)
        db.commit()
        print("✅ Created admin user (username: admin, password: admin123)")
    else:
        print("ℹ️  Admin user already exists")


def main():
    """Main seeding function"""
    print("🌱 Seeding database...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if problems already exist
        existing_problems = db.query(Problem).count()
        
        if existing_problems > 0:
            print(f"ℹ️  Database already has {existing_problems} problems")
            response = input("Do you want to add more sample problems? (y/n): ")
            if response.lower() != 'y':
                print("Skipping problem creation")
                return
        
        create_admin_user(db)
        create_sample_problems(db)
        
        print("\n✅ Database seeded successfully!")
        print("\nSample Problems:")
        print("1. Two Sum (EASY) - Arrays")
        print("2. Reverse String (EASY) - Strings")
        print("3. Fizz Buzz (EASY) - Math")
        print("4. Palindrome Number (EASY) - Math")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
