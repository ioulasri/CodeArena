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

You can return the answer in any order.""",
        difficulty="EASY",
        category="Arrays",
        tags=["array", "hash-table"],
        constraints="""- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.""",
        examples=[
            {
                "input": "2 7 11 15\n9",
                "output": "0 1",
                "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
                "input": "3 2 4\n6",
                "output": "1 2",
                "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
            },
            {
                "input": "3 3\n6",
                "output": "0 1",
                "explanation": "Because nums[0] + nums[1] == 6, we return [0, 1]."
            }
        ],
        time_limit_ms=2000,
        memory_limit_mb=128,
        acceptance_rate=49.5,
        is_premium=False
    )
    
    # Problem 2: Reverse String
    reverse_string = Problem(
        title="Reverse String",
        slug="reverse-string",
        description="""Write a function that reverses a string. The input string is given as an array of characters.

You must do this by modifying the input array in-place with O(1) extra memory.""",
        difficulty="EASY",
        category="Strings",
        tags=["string", "two-pointers"],
        constraints="""- 1 <= s.length <= 10^5
- s[i] is a printable ascii character.""",
        examples=[
            {
                "input": "hello",
                "output": "olleh",
                "explanation": "Reverse the string 'hello' to 'olleh'"
            },
            {
                "input": "world",
                "output": "dlrow",
                "explanation": "Reverse the string 'world' to 'dlrow'"
            }
        ],
        time_limit_ms=1000,
        memory_limit_mb=64,
        acceptance_rate=72.8,
        is_premium=False
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

Return the list for all numbers from 1 to n.""",
        difficulty="EASY",
        category="Math",
        tags=["math", "string"],
        constraints="1 <= n <= 10^4",
        examples=[
            {
                "input": "5",
                "output": "1\n2\nFizz\n4\nBuzz",
                "explanation": "Output for n=5"
            },
            {
                "input": "15",
                "output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
                "explanation": "Output for n=15"
            }
        ],
        time_limit_ms=1000,
        memory_limit_mb=64,
        acceptance_rate=65.2,
        is_premium=False
    )
    
    # Problem 4: Palindrome Number
    palindrome = Problem(
        title="Palindrome Number",
        slug="palindrome-number",
        description="""Given an integer x, return true if x is a palindrome, and false otherwise.

An integer is a palindrome when it reads the same forward and backward.
For example, 121 is a palindrome while 123 is not.""",
        difficulty="EASY",
        category="Math",
        tags=["math"],
        constraints="-2^31 <= x <= 2^31 - 1",
        examples=[
            {
                "input": "121",
                "output": "true",
                "explanation": "121 reads as 121 from left to right and from right to left."
            },
            {
                "input": "-121",
                "output": "false",
                "explanation": "From left to right, it reads -121. From right to left, it becomes 121-."
            },
            {
                "input": "10",
                "output": "false",
                "explanation": "Reads 01 from right to left."
            }
        ],
        time_limit_ms=1000,
        memory_limit_mb=64,
        acceptance_rate=54.3,
        is_premium=False
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
