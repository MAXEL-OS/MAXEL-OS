import customtkinter as ctk
import arabic_reshaper
from bidi.algorithm import get_display

class MaxelUI(ctk.CTk):
    def __init__(self, callbacks):
        super().__init__()

        # UI Scaling and Window Configuration
        ctk.set_widget_scaling(1.3) 
        self.title("MAXEL-OS - AI Control Center")
        self.geometry("1200x800")

        self.callbacks = callbacks
        self.font_chat = ("Arial", 20)
        self.font_ui = ("Arial", 14)

        # Layout Configuration
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Left Side) ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(2, weight=1)

        self.logo = ctk.CTkLabel(self.sidebar, text="MAXEL-OS", font=("Arial", 24, "bold"))
        self.logo.grid(row=0, column=0, pady=20, padx=20)

        self.btn_new = ctk.CTkButton(self.sidebar, text="+ New Chat", font=("Arial", 16, "bold"), 
                                     height=40, command=self.callbacks['new_chat'])
        self.btn_new.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

        # Chat History List
        self.history_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.history_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # --- Main Chat Area ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.chat_display = ctk.CTkTextbox(self.main_frame, font=self.font_chat, spacing3=12)
        self.chat_display.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        
        self.chat_display._textbox.tag_config("rtl", justify="right")
        self.chat_display._textbox.tag_config("ltr", justify="left")

        # --- Input Section ---
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = ctk.CTkEntry(self.input_frame, height=55, font=self.font_chat, 
                                       placeholder_text="Enter your command...")
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(0, 15))
        
        self.user_input.bind("<KeyRelease>", self.update_input_direction)
        self.user_input.bind("<Return>", lambda e: self.callbacks['send']())

        self.btn_send = ctk.CTkButton(self.input_frame, text="Execute", width=110, height=55, 
                                      font=("Arial", 18, "bold"), command=self.callbacks['send'])
        self.btn_send.grid(row=0, column=1)

    def update_input_direction(self, event):
        text = self.user_input.get()
        if any('\u0600' <= c <= '\u06FF' for c in text):
            self.user_input.configure(justify="right")
        else:
            self.user_input.configure(justify="left")

    def process_text(self, text):
        if any('\u0600' <= c <= '\u06FF' for c in text):
            lines = text.split('\n')
            reshaped_lines = [get_display(arabic_reshaper.reshape(line)) for line in lines]
            return '\n'.join(reshaped_lines)
        return text

    def display_msg(self, role, text):
        self.chat_display.configure(state="normal")
        is_ar = any('\u0600' <= c <= '\u06FF' for c in text)
        tag = "rtl" if is_ar else "ltr"
        
        if role == "user":
            display_content = self.process_text(text)
        else:
            header = "MAXEL: "
            body = self.process_text(text)
            display_content = f"{header}\n{body}" if is_ar else f"{header}{body}"

        self.chat_display.insert("end", f"{display_content}\n\n", tag)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def render_history(self, chats):
        # Clear current list
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        # Sort: Pinned first, then by normal order
        sorted_chats = sorted(chats, key=lambda x: x.get('pinned', False), reverse=True)

        for chat in sorted_chats:
            chat_id = chat['id']
            frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
            frame.pack(fill="x", pady=2)

            title = chat.get("title", "New Chat")
            title_disp = self.process_text(title[:15] + "..." if len(title) > 15 else title)
            pin_icon = "[P]" if chat.get('pinned') else "---"

            btn_load = ctk.CTkButton(frame, text=title_disp, font=self.font_ui, anchor="w", 
                                     fg_color="transparent", border_width=1,
                                     command=lambda cid=chat_id: self.callbacks['load'](cid))
            btn_load.pack(side="left", fill="x", expand=True, padx=(0, 5))

            btn_pin = ctk.CTkButton(frame, text=pin_icon, width=30, font=self.font_ui,
                                    command=lambda cid=chat_id: self.callbacks['pin'](cid))
            btn_pin.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(frame, text="X", width=30, font=self.font_ui, fg_color="#8B0000", hover_color="#FF0000",
                                    command=lambda cid=chat_id: self.callbacks['delete'](cid))
            btn_del.pack(side="left", padx=2)
