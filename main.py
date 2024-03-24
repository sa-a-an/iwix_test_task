import asyncio
import time

def main():
    start_time = time.time()

    time_diff = time.time() - start_time
    print(f"Time diff: {time_diff}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())