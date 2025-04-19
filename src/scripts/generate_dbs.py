import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from create_test_dbs import create_test_databases

async def main():
    await create_test_databases()

if __name__ == "__main__":
    asyncio.run(main())