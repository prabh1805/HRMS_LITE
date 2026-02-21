"""Seed script to populate database with 100 employees and attendance records."""

import asyncio
from datetime import date, timedelta
import random
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.employee import Employee
from app.models.attendance import Attendance, AttendanceStatus


# Sample data for generating realistic employees
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna",
    "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Frank", "Rachel", "Alexander", "Catherine", "Patrick", "Carolyn", "Jack", "Janet",
    "Dennis", "Ruth", "Jerry", "Maria", "Tyler", "Heather", "Aaron", "Diane"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins"
]

DEPARTMENTS = [
    "Engineering", "Marketing", "Sales", "Human Resources", "Finance",
    "Operations", "Customer Support", "Product Management", "Design", "Legal"
]


async def generate_employee_id(session: AsyncSession, index: int) -> str:
    """Generate employee ID in format EMP-0001, EMP-0002, etc."""
    return f"EMP-{index:04d}"


async def seed_employees(session: AsyncSession, count: int = 100):
    """Create employees with realistic data."""
    from sqlalchemy import select, func
    
    # Check existing employee count to start from next ID
    result = await session.execute(select(func.max(Employee.employee_id)))
    max_id = result.scalar()
    
    start_index = 1
    if max_id:
        # Extract number from EMP-XXXX format
        try:
            start_index = int(max_id.split('-')[1]) + 1
        except:
            start_index = 1
    
    print(f"Creating {count} employees starting from EMP-{start_index:04d}...")
    
    employees = []
    for i in range(count):
        emp_num = start_index + i
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{emp_num}@company.com"
        department = random.choice(DEPARTMENTS)
        employee_id = f"EMP-{emp_num:04d}"
        
        employee = Employee(
            employee_id=employee_id,
            full_name=full_name,
            email=email,
            department=department
        )
        employees.append(employee)
        
        if (i + 1) % 10 == 0:
            print(f"  Generated {i + 1}/{count} employees...")
    
    session.add_all(employees)
    await session.flush()
    print(f"✓ Created {count} employees")
    return employees


async def seed_attendance(session: AsyncSession, employees: list[Employee], days: int = 30):
    """Create attendance records for the past N days."""
    print(f"\nCreating attendance records for past {days} days...")
    
    today = date.today()
    attendance_records = []
    
    for day_offset in range(days):
        attendance_date = today - timedelta(days=day_offset)
        
        # Skip weekends (optional - remove if you want weekend attendance)
        if attendance_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
            continue
        
        for employee in employees:
            # 85% chance of being present (realistic attendance rate)
            status = AttendanceStatus.PRESENT if random.random() < 0.85 else AttendanceStatus.ABSENT
            
            attendance = Attendance(
                employee_id=employee.id,
                date=attendance_date,
                status=status
            )
            attendance_records.append(attendance)
        
        if (day_offset + 1) % 5 == 0:
            print(f"  Generated attendance for {day_offset + 1}/{days} days...")
    
    session.add_all(attendance_records)
    await session.flush()
    print(f"✓ Created {len(attendance_records)} attendance records")


async def main():
    """Main seeding function."""
    print("=" * 60)
    print("DATABASE SEEDING SCRIPT")
    print("=" * 60)
    print("\nThis will add 100 employees and their attendance records.")
    print("Press Ctrl+C to cancel...\n")
    
    await asyncio.sleep(2)  # Give user time to cancel
    
    async with AsyncSessionLocal() as session:
        try:
            # Create employees
            employees = await seed_employees(session, count=100)
            
            # Create attendance records for past 30 days
            await seed_attendance(session, employees, days=30)
            
            # Commit all changes
            await session.commit()
            
            print("\n" + "=" * 60)
            print("✓ SEEDING COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"\nSummary:")
            print(f"  • 100 employees created")
            print(f"  • Attendance marked for past 30 days (weekdays only)")
            print(f"  • Average attendance rate: ~85%")
            print(f"\nYou can now view the data in your application!")
            
        except Exception as e:
            await session.rollback()
            print(f"\n✗ ERROR: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
