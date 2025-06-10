import requests
import random
import string
import os

# Generate and save new code
def generate_new_code(length=6):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    code_path = os.path.join(os.path.dirname(__file__), 'allprops_app', 'access_code.txt')
    with open(code_path, 'w') as f:
        f.write(code)
    return code

def send_notification():
    # Generate and store new code
    code = generate_new_code()

    webhook_url = "https://discord.com/api/webhooks/1354278970119426149/JmJu7JqDW2JBgwNKW3cb18eo4dN8dNNq2Iwvdz8jdw3CJ0J85KvYOP13qoPHHlHm-voU"

    message = {
        "content": f"📊 **Props of the Day are Ready!**\n🔗 Access: http://127.0.0.1:5000\n🧩 Code: `{code}`"
    }

    response = requests.post(webhook_url, json=message)
    if response.status_code == 204:
        print(f"✅ Notification sent with code: {code}")
    else:
        print(f"❌ Failed to send: {response.status_code}")

if __name__ == "__main__":
    send_notification()
