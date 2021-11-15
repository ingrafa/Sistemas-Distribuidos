import CosNaming, Client, Client__POA
import os
import sys
import threading
from omniORB import CORBA, PortableServer
from utils import connect_to_client


class ClientServer(Client__POA.ClientServer):
    chat_msg = {}

    def receive_msg(self, username, timestamp, msg, from_me):
        chat = ""
        if from_me != '':
            chat = "[{}] {}: {}".format(timestamp, from_me, msg)
        else:
            chat = "[{}] {}: {}".format(timestamp, username, msg)
        
        if username not in self.chat_msg:
            self.chat_msg[username] = []
        self.chat_msg[username].append(chat)


    def get_msg_count(self, username):
        if username in self.chat_msg:
            return len(self.chat_msg[username])
        else:
            return 0

    def show_chat(self, username):
        if username in self.chat_msg:
            for msg in self.chat_msg[username]:
                    print(msg)
        else:
            print("Nenhuma mensagem ainda :(")
            print("Converse com seu amigo!")
            