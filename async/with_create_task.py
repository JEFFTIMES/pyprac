import asyncio
import time

async def part1(n: int) -> int:
    print("Starting part1...")
    await asyncio.sleep(2)  # Simulating a non-blocking I/O operation
    print("Finished part1.")
    return n + 1

async def part2(n: int) -> int:
    print("Starting part2...")
    await asyncio.sleep(1)  # Simulating a non-blocking I/O operation
    print("Finished part2.")
    return n * 2

async def chain(n: int) -> None:
    start = time.perf_counter()
    
    # Start part1 as a task
    part1_task = asyncio.create_task(part1(n))
    
    # Start part2 independently of part1
    part2_task = asyncio.create_task(part2(n))

    # Await both tasks
    p1_result = await part1_task
    p2_result = await part2_task

    end = time.perf_counter() - start
    
    print(f"Results: part1={p1_result}, part2={p2_result}, Time elapsed: {end:.2f} seconds")

# Run the main coroutine
asyncio.run(chain(5))
