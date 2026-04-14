from ui import MaxelUI
import brain
import json
import os
import time

class MaxelController:
    def __init__(self):
        self.db_file = "chats.json"
        self.chats = self.load_data()
        self.current_chat_id = None
        
        callbacks = {
            'send': self.on_send,
            'new_chat': self.on_new,
            'load': self.load_chat,
            'pin': self.toggle_pin,
            'delete': self.delete_chat
        }
        
        self.ui = MaxelUI(callbacks)
        self.ui.render_history(self.chats)
        self.on_new()

    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_data(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.chats, f, ensure_ascii=False, indent=4)
        self.ui.render_history(self.chats)

    def get_current_chat(self):
        for c in self.chats:
            if c['id'] == self.current_chat_id:
                return c
        return None

    def on_send(self):
        msg = self.ui.user_input.get()
        if not msg.strip(): 
            return

        chat = self.get_current_chat()
        
        # Auto-name the chat if it is the first message
        if not chat['messages'] and chat['title'] == "New Chat":
            words = msg.split()
            chat['title'] = " ".join(words[:4])

        self.ui.user_input.delete(0, "end")
        self.ui.display_msg("user", msg)

        # Get response using context
        response = brain.call_ollama(msg, chat['messages'])
        self.ui.display_msg("assistant", response)

        # Save to history
        chat['messages'].append({"role": "user", "content": msg})
        chat['messages'].append({"role": "assistant", "content": response})
        self.save_data()

    def on_new(self):
        new_id = str(int(time.time()))
        new_chat = {
            "id": new_id,
            "title": "New Chat",
            "pinned": False,
            "messages": []
        }
        self.chats.append(new_chat)
        self.current_chat_id = new_id
        self.save_data()
        
        self.ui.chat_display.configure(state="normal")
        self.ui.chat_display.delete("1.0", "end")
        self.ui.chat_display.configure(state="disabled")

    def load_chat(self, chat_id):
        self.current_chat_id = chat_id
        chat = self.get_current_chat()
        
        self.ui.chat_display.configure(state="normal")
        self.ui.chat_display.delete("1.0", "end")
        self.ui.chat_display.configure(state="disabled")
        
        for msg in chat['messages']:
            self.ui.display_msg(msg['role'], msg['content'])

    def toggle_pin(self, chat_id):
        for c in self.chats:
            if c['id'] == chat_id:
                c['pinned'] = not c.get('pinned', False)
                break
        self.save_data()

    def delete_chat(self, chat_id):
        self.chats = [c for c in self.chats if c['id'] != chat_id]
        if self.current_chat_id == chat_id:
            self.on_new()
        else:
            self.save_data()

    def run(self):
        self.ui.mainloop()

if __name__ == "__main__":
    app = MaxelController()
    app.run()
