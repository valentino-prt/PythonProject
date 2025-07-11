async def main():
    object_ids = range(1000)  # ou 20000 dans ton cas
    semaphore = asyncio.Semaphore(100)  # limite de connexions
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = [
            MyObjectClient(obj_id, session, semaphore).run()
            for obj_id in object_ids
        ]

        # Utilise gather par batch pour éviter de charger 20000 tasks d'un coup
        BATCH_SIZE = 500
        for i in range(0, len(tasks), BATCH_SIZE):
            batch = tasks[i:i+BATCH_SIZE]
            batch_results = await asyncio.gather(*batch)
            results.extend(batch_results)

    print("All tasks done.")

asyncio.run(main())

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
        
        
import asyncio
import aiohttp
import random

class MyObjectClient:
    def __init__(self, obj_id: int, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
        self.obj_id = obj_id
        self.session = session
        self.semaphore = semaphore

    async def fetch_with_retry(self, url: str, retries: int = 3):
        for attempt in range(1, retries + 1):
            try:
                async with self.semaphore:
                    async with self.session.get(url, timeout=10) as response:
                        response.raise_for_status()
                        return await response.text()
            except Exception as e:
                if attempt == retries:
                    print(f"[{self.obj_id}] Failed to fetch {url}: {e}")
                    return None
                await asyncio.sleep(random.uniform(0.5, 1.5))  # backoff

    async def run(self):
        base_url = "https://api.example.com/object"
        endpoints = [
            f"{base_url}/{self.obj_id}/details",
            f"{base_url}/{self.obj_id}/status",
            f"{base_url}/{self.obj_id}/history",
            f"{base_url}/{self.obj_id}/metrics"
        ]

        results = await asyncio.gather(*(self.fetch_with_retry(url) for url in endpoints))
        return {
            "object_id": self.obj_id,
            "details": results[0],
            "status": results[1],
            "history": results[2],
            "metrics": results[3],
        }
