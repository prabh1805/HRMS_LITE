"""
Test PostgreSQL connection and create a test table.
"""
import asyncio
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

# Connection string from .env.example
DATABASE_URL = "postgresql+asyncpg://hrms_lite_av75_user:M40OIm3kCwQcEkEm6yaPy0ttKXDeo8eP@dpg-d6cnplfgi27c7384so3g-a.oregon-postgres.render.com/hrms_lite_av75"


async def test_connection():
    """Test database connection and create a test table."""
    print("🔌 Testing PostgreSQL connection...")
    print(f"📍 Host: dpg-d6cnplfgi27c7384so3g-a.oregon-postgres.render.com")
    print(f"🗄️  Database: hrms_lite_av75\n")
    
    try:
        # Create engine
        engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
        )
        
        # Create session factory
        async_session = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        async with async_session() as session:
            # Test 1: Basic connection
            print("✅ Step 1: Testing basic connection...")
            result = await session.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"   PostgreSQL version: {version[:50]}...\n")
            
            # Test 2: Check current database
            print("✅ Step 2: Checking current database...")
            result = await session.execute(text("SELECT current_database()"))
            db_name = result.scalar()
            print(f"   Connected to database: {db_name}\n")
            
            # Test 3: Create a test table
            print("✅ Step 3: Creating test table 'connection_test'...")
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS connection_test (
                    id SERIAL PRIMARY KEY,
                    test_message VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            await session.commit()
            print("   Table created successfully!\n")
            
            # Test 4: Insert test data
            print("✅ Step 4: Inserting test data...")
            await session.execute(text("""
                INSERT INTO connection_test (test_message)
                VALUES ('Connection test successful! 🎉')
            """))
            await session.commit()
            print("   Data inserted successfully!\n")
            
            # Test 5: Query the data
            print("✅ Step 5: Querying test data...")
            result = await session.execute(text("""
                SELECT id, test_message, created_at 
                FROM connection_test 
                ORDER BY id DESC 
                LIMIT 5
            """))
            rows = result.fetchall()
            print(f"   Found {len(rows)} row(s):")
            for row in rows:
                print(f"   - ID: {row[0]}, Message: {row[1]}, Created: {row[2]}")
            print()
            
            # Test 6: List all tables
            print("✅ Step 6: Listing all tables in database...")
            result = await session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
            if tables:
                print(f"   Found {len(tables)} table(s):")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("   No tables found (database is empty)")
            print()
            
            print("🎉 All tests passed! Your PostgreSQL connection is working perfectly!")
            
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"\n❌ Connection test failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
