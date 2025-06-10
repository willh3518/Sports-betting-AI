import requests
import time
import random

# File containing proxies (one per line)
PROXY_FILE = "working_proxies.txt"

# Test target
TEST_URL = "https://www.statmuse.com"

# Read proxies from file
def load_proxies(file_path):
    with open(file_path, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

# Test a single proxy
def test_proxy(proxy, timeout=10):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ Working Proxy: {proxy}")
            return True
        else:
            print(f"❌ Failed (Status Code {response.status_code}): {proxy}")
            return False
    except Exception as e:
        print(f"❌ Failed: {proxy} | Error: {e}")
        return False

# Main function to run the checks
def main():
    proxy_list = load_proxies(PROXY_FILE)
    print(f"🔹 Loaded {len(proxy_list)} proxies to test...")

    working_proxies = []

    for idx, proxy in enumerate(proxy_list, 1):
        print(f"🔎 Testing proxy {idx}/{len(proxy_list)}: {proxy}")
        if test_proxy(proxy):
            working_proxies.append(proxy)

        # Random delay to avoid hammering
        time.sleep(random.uniform(0.5, 1.5))

    # Save working proxies to a new file
    if working_proxies:
        with open("working_proxies_new.txt", "w") as f:
            for proxy in working_proxies:
                f.write(f"{proxy}\n")
        print(f"\n✅ {len(working_proxies)} working proxies saved to 'working_proxies.txt'")
    else:
        print("\n⚠️ No working proxies found.")

if __name__ == "__main__":
    main()
