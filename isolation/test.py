import asyncio
import aiohttp
import time

async def do_health_check(address):
    async with aiohttp.ClientSession() as session:
        try:
            start = time.time()
            async with session.get(address) as resp:
                print(resp.status)  # prints HTTP status as integer
                end = time.time()
                duration = end - start
                print(duration)
                return address, True if resp.status == 200 and duration < 0.5 else False
        except Exception as e:
            print(str(e))
            return address, False

async def health_check(services_addresses):
    tasks = [do_health_check(a) for a in services_addresses]
    t1 = await asyncio.gather(*tasks)
    
    res = {res[0]: res[1] for res in t1}
    print(res)
    return res


if __name__ == "__main__":
    addresses = ["http://httpbin.org/get", "http://google.de", "127.0.0.1:30003", "http://www.amazon.de"]
    asyncio.run(health_check(addresses))


