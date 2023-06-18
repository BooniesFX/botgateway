## Usage
**Generate a key**
```python
from nostr.key import PrivateKey

private_key = PrivateKey()
public_key = private_key.public_key
print(f"Private key: {private_key.bech32()}")
print(f"Public key: {public_key.bech32()}")
```

**Connect to relays**
```python
import json
import ssl
import time
from nostr.relay_manager import RelayManager

relay_manager = RelayManager()
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://offchain.pub")
relay_manager.add_relay("wss://nos.lol")
relay_manager.add_relay("wss://relay.snort.social")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(1.25) # allow the connections to open

while relay_manager.message_pool.has_notices():
  notice_msg = relay_manager.message_pool.get_notice()
  print(notice_msg.content)
  
relay_manager.close_connections()
```

**Publish to relays**
```python
import json 
import ssl
import time
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey

relay_manager = RelayManager()
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://offchain.pub")
relay_manager.add_relay("wss://nos.lol")
relay_manager.add_relay("wss://relay.snort.social")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(1.25) # allow the connections to open

private_key = PrivateKey()

event = Event("Hello Nostr")
private_key.sign_event(event)

relay_manager.publish_event(event)
time.sleep(1) # allow the messages to send

relay_manager.close_connections()
```

**Reply to a note**
```python
from nostr.event import Event

reply = Event(
  content="Hey, that's a great point!",
)

# create 'e' tag reference to the note you're replying to
reply.add_event_ref(original_note_id)

# create 'p' tag reference to the pubkey you're replying to
reply.add_pubkey_ref(original_note_author_pubkey)

private_key.sign_event(reply)
relay_manager.publish_event(reply)
```

**Send a DM**
```python
from nostr.event import EncryptedDirectMessage

dm = EncryptedDirectMessage(
  recipient_pubkey=recipient_pubkey,
  cleartext_content="Secret message!"
)
private_key.sign_event(dm)
relay_manager.publish_event(dm)
```


**Receive events from relays**
```python
import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType

filters = Filters([Filter(authors=[<a nostr pubkey in hex>], kinds=[EventKind.TEXT_NOTE])])
subscription_id = <a string to identify a subscription>
request = [ClientMessageType.REQUEST, subscription_id]
request.extend(filters.to_json_array())

relay_manager = RelayManager()
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://offchain.pub")
relay_manager.add_relay("wss://nos.lol")
relay_manager.add_relay("wss://relay.snort.social")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_subscription(subscription_id, filters)
relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(1.25) # allow the connections to open

message = json.dumps(request)
relay_manager.publish_message(message)
time.sleep(1) # allow the messages to send

while relay_manager.message_pool.has_events():
  event_msg = relay_manager.message_pool.get_event()
  print(event_msg.event.content)
  
relay_manager.close_connections()
```