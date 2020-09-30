if message["chat"]["type"]=="private":
    print("message['from']['id'] and message['chat']['id'] are equal")
else:
    print("message['from']['id'] and message['chat']['id'] are not equal")