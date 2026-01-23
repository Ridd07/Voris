from engine.features import findContact

query = "make a phone call with riya"
print(f"Testing query: '{query}'")

contact_no, name = findContact(query)
print(f"Contact found: {contact_no}, Name: {name}")

flag = ""
if "send message" in query or "send a message" in query:
    flag = 'message'
elif "phone call" in query or "call" in query:
    flag = 'call'
elif "video call" in query:
    flag = 'video'

print(f"Flag decided: '{flag}'")

if contact_no != 0 and flag != "":
    print("Ready to call whatsApp function")
else:
    print("Would NOT call whatsApp function")
