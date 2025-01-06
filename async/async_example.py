import asyncio
import aiohttp

async def fetch_data(session, url):
    print("Start fetching data...")
    async with session.get(url) as response:
        data = await response.json()  # Parse the JSON response
        print("Finished fetching data.")
        return data

async def perform_computation():
    for i in range(5):
        print(f"Performing computation {i + 1}")
        await asyncio.sleep(0.1)  # Simulating a non-blocking delay to yield control to the event loop

async def perform_another_computation():
    for i in range(5):
        print(f"Performing another computation {i + 1}")
        await asyncio.sleep(0.1)  # Simulating a non-blocking delay to yield control to the event loop

async def main():
    url = 'https://jsonplaceholder.typicode.com/posts/1'

    async with aiohttp.ClientSession() as session:
        # Schedule fetch_data() to run concurrently with other tasks
        fetch_task = asyncio.create_task(fetch_data(session, url))
        #another_computation = asyncio.create_task(perform_another_computation())

        # Perform other tasks while fetch_data() is running
        await perform_computation()
        await perform_another_computation()

        # Await the result of fetch_data()
        result = await fetch_task
        print(f"Fetched result: {result}")

# Run the main coroutine
asyncio.run(main())

