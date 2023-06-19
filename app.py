import os,datetime,time,json,ssl,threading,signal
from dotenv import load_dotenv
from api import BotAPI
import numpy as np
from nostr.relay_manager import RelayManager
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.event import EncryptedDirectMessage
from nostr.key import PrivateKey,PublicKey

load_dotenv()
# port = os.getenv('FLASK_RUN_PORT')
test_npub = os.getenv('TEST_NPUB')
test_nsec = os.getenv('TEST_NSEC')
test_name = os.getenv('TEST_NAME')
api_key = os.getenv('API_KEY')
botid = os.getenv('BOT_ID')

class NostrBot:
    def __init__(self, relays: str,name: str, pub: str,sec: str) -> None:
        self.name=name
        self.relay_file=relays
        self.relay_manager=RelayManager()
        self.npub= pub
        self.private_key=PrivateKey.from_nsec(sec)

    def connect_relays(self,stop_event,round_sec=10):
        relays = np.loadtxt(self.relay_file, delimiter=';',dtype='str')
        print(f"start connecting to {len(relays)} relays at{datetime.datetime.now()}")
        for r in relays:
            print(f"add relay:{r}")
            self.relay_manager.add_relay(r)
        # filter
        pubkey = PublicKey.from_npub(self.npub)
        dm_filter = Filter(
            pubkey_refs=[pubkey.hex()]
            )
        filters = Filters([dm_filter])
        subscription_id = self.npub
        request = [ClientMessageType.REQUEST,subscription_id]
        request.extend(filters.to_json_array())
        self.relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        # setup bot
        bot = BotAPI(chatbot_name=test_name, chatbot_id=botid,api_key=api_key)
        while not stop_event.is_set():
            while(self.relay_manager.message_pool.has_notices()):
                notice_msg = self.relay_manager.message_pool.get_notice()
                print(f"=================notices{datetime.datetime.now()}=====================")
                print(notice_msg.content)
            while(self.relay_manager.message_pool.has_events()):
                event_msg = self.relay_manager.message_pool.get_event()
                if event_msg.event.kind == EventKind.TEXT_NOTE or event_msg.event.kind == EventKind.ENCRYPTED_DIRECT_MESSAGE:
                    print(f"=================events{datetime.datetime.now()}=====================")
                    print(f"note id:{event_msg.event.note_id}")
                    print(f"note kind:{event_msg.event.kind}")
                    print(f"tags:{event_msg.event.tags}")
                    print(f"content:{event_msg.event.content}")
                    if event_msg.event.kind == EventKind.ENCRYPTED_DIRECT_MESSAGE:
                        msg = self.private_key.decrypt_message(event_msg.event.content,event_msg.event.public_key)
                        print(f"decrypt content:{msg}")
                        # test call botapi
                        print(f"message to {bot.chatbot_name}")
                        resp = bot.message_chatbot(msg)
                        print(f"response content:{resp}")
            time.sleep(round_sec)

        print("close all connnections")
        self.relay_manager.close_all_relay_connections()
        
    def push_note(self,message):
        event = Event(message)
        self.private_key.sign_event(event)
        self.relay_manager.publish_event(event)
        print("================publish notes!==================")
        print(message)
        time.sleep(5) # allow the messages to send

    def reply_note(self,original_note_author_pubkey,original_note_id,message):
        reply = Event(
        content=message,
        )

        # create 'e' tag reference to the note you're replying to
        reply.add_event_ref(original_note_id)

        # create 'p' tag reference to the pubkey you're replying to
        reply.add_pubkey_ref(original_note_author_pubkey)

        self.private_key.sign_event(reply)
        self.relay_manager.publish_event(reply)

    def dm(self,recipient_pubkey,message):
        dm = EncryptedDirectMessage(
        recipient_pubkey=recipient_pubkey,
        cleartext_content=message
        )
        self.private_key.sign_event(dm)
        self.relay_manager.publish_event(dm)

    def close_connections(self):
        self.relay_manager.close_all_relay_connections()

def signal_handler(signum,event):
    print("Received signal:", signum)
    time.sleep(2)
    exit(0)

if __name__ == '__main__':
    NewBot = NostrBot("relays.default",test_name,test_npub,test_nsec)
    print("read npub:", NewBot.npub)
    print(f"Hello, I am bot named {NewBot.name},launch time is {datetime.datetime.now()}")
    stop_event = threading.Event()
    t = threading.Thread(target=NewBot.connect_relays,args=(stop_event,))
    t.start()
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
    stop_event.set()
    t.join()
    print(f"Bye Karma!")