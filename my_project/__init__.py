import asyncio
import aiohttp

CONCURRENCY_LIMIT = 100  # Tune based on your system/network

# Simulate 4 async calls per object
async def process_object(obj_id, session, semaphore):
    async with semaphore:
        r1 = await session.get(f"https://example.com/api/1/{obj_id}")
    async with semaphore:
        r2 = await session.get(f"https://example.com/api/2/{obj_id}")
    async with semaphore:
        r3 = await session.get(f"https://example.com/api/3/{obj_id}")
    async with semaphore:
        r4 = await session.get(f"https://example.com/api/4/{obj_id}")

    return await r1.text(), await r2.text(), await r3.text(), await r4.text()

async def main():
    object_ids = list(range(20000))
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    async with aiohttp.ClientSession() as session:
        tasks = [
            process_object(obj_id, session, semaphore)
            for obj_id in object_ids
        ]

        results = await asyncio.gather(*tasks)

    print("All done.")

asyncio.run(main())


BATCH_SIZE = 500

async def run_batches():
    for i in range(0, len(object_ids), BATCH_SIZE):
        batch = tasks[i:i+BATCH_SIZE]
        await asyncio.gather(*batch)
