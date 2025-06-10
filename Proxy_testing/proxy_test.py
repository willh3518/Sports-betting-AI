import aiohttp
import asyncio

# 📌 Timeout for Proxy Test (Seconds)
PROXY_TIMEOUT = 10
TEST_URL = "https://www.statmuse.com"  # Simple page to test connectivity

async def check_proxy(proxy_url):
    """
    Tests if a proxy is working by sending a request to a test URL.
    Returns True if working, False otherwise.
    """
    test_proxy = f"http://{proxy_url}"  # Ensure HTTP format
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(TEST_URL, proxy=test_proxy, timeout=PROXY_TIMEOUT) as resp:
                if resp.status == 200:
                    print(f"✅ Proxy Working: {proxy_url}")
                    return proxy_url  # Return the working proxy
    except:
        print(f"❌ Proxy Failed: {proxy_url}")
        return None  # Return None if proxy fails

async def test_proxies(proxy_list):
    """Tests all proxies concurrently and saves the working ones."""
    print("\n🔍 Testing Proxies...\n")

    tasks = [check_proxy(proxy) for proxy in proxy_list]
    working_proxies = await asyncio.gather(*tasks)

    # Remove None values (failed proxies)
    working_proxies = [proxy for proxy in working_proxies if proxy]

    # Save working proxies to a file
    if working_proxies:
        with open("working_proxies.txt", "w") as file:
            for proxy in working_proxies:
                file.write(proxy + "\n")
        print("\n✅ Working proxies saved to 'working_proxies.txt'!\n")
    else:
        print("\n🚨 No working proxies found.\n")

if __name__ == "__main__":
    # Load proxy list from the file
    with open("proxyscrape_premium_http_proxies.txt", "r") as file:
        proxies = [line.strip() for line in file.readlines()]
    asyncio.run(test_proxies(proxies))
