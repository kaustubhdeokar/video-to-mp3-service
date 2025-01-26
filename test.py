import asyncio

async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)  # Simulate an I/O-bound operation
    print("Data fetched")
    return {"data": "sample"}

async def another_task():
    print("Starting another task...")
    await asyncio.sleep(1)  # Simulate an I/O-bound operation
    print("Another task completed")

async def main():
    print("Start")
    # Schedule both tasks to run concurrently
    task1 = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(another_task())
    
    # Await both tasks to complete
    result = await task1
    await task2
    
    print("Result:", result)
    print("End")

# Run the main coroutine
asyncio.run(main())