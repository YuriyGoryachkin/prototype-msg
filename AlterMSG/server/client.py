from websocket import create_connection

url = "ws://127.0.0.1:8888/v1/search/"

message = {'search': 'mte@gmail.com'}

ws = create_connection(url, header=['token:d53e124e6b31e34d'])
# print("Sending some message...")
# msg = ''
# while msg != 'exit':
#     msg = input('Enter message to send: ')
#     ws.send(msg)
#     print("Sent")
#
#     print("Reсeiving...")
#     result = ws.recv()
#     print("Received '%s'" % result)
#
# ws.close()

print(message)
ws.send(message)
result = ws.recv()
print(result)
ws.close()