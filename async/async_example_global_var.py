import asyncio

state = None

async def fetch_data():
    global state
    print(f"Start fetching data... | {state} ")
    state = 'fetch-started'
    await asyncio.sleep(2)  # Simulating a non-blocking I/O operation
    print(f"Finished fetching data. | {state} ")
    state = 'fetch-completed'
    return "data"

async def perform_computation():
    global state
    for i in range(5):
        print(f"Performing computation {i + 1} | {state}")
        state = f'perform - {i+1}'
        await asyncio.sleep(1)  # Simulating a non-blocking delay to yield control to the event loop

async def main():
    # Schedule fetch_data() to run concurrently with other tasks
    fetch_task = asyncio.create_task(fetch_data())

    # Perform other tasks while fetch_data() is running
    await perform_computation()

    # Await the result of fetch_data()
    result = await fetch_task
    print(f"Fetched result: {result}")

# Run the main coroutine
asyncio.run(main())

