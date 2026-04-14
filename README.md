MAXEL-OS AI Control Center

MAXEL-OS is a professional desktop interface for local Large Language Models (LLMs). It provides a high-performance, modern UI specifically designed to handle bilingual interactions (English/Arabic) with full RTL support.
Core Features

    Modern GUI: Built with CustomTkinter for a sleek, dark-themed experience.

    Smart Conversation History: Automatically saves, renames, and manages your chat sessions.

    Advanced Controls: Pin important chats and delete old ones with a single click.

    Universal RTL Support: Native support for Arabic text shaping and Right-to-Left alignment.

    Local & Private: Powered by Ollama, ensuring your data never leaves your machine.

Prerequisites

Before running the application, ensure you have the following installed:

1.    Ollama: Download from ollama.com

2.    Qwen 2.5 Model: Run the command:
    Bash
    ollama run qwen2.5
    
Setup & Installation

1. Clone the Repository
git clone https://github.com/MAXEL-OS/MAXEL-OS.git
cd MAXEL-OS

2. Install Dependencies
pip install -r requirements.txt

3. Configure the Model
Create the custom model using the provided Modelfile:
ollama create maxel-ai -f Modelfile

4. Run the Application
sh run.sh


