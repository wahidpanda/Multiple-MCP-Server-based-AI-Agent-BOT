import asyncio 
from dotenv import load_dotenv
from mcp_use import  MCPAgent, MCPClient
from langchain_groq import ChatGroq
import os
load_dotenv()

async def run_memory_chat():
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    config_file = "browser_mcp.json"
    print("Initializatig Chat....")
    client= MCPClient.from_config_file(config_file)
    llm= ChatGroq(model="llama3-8b-8192")

    agent=MCPAgent(
        llm=llm,
        client=client,
        max_step=15,
        memory_enabled=True,

    )

    print("\n=== Interactive MCP Chat ====")
    print("Type 'exit' to end the conversation.")
    print("Type 'clear' to clear the memory.")
    print("===========================================================\n")

    try:
        while True:
            user_input= input("\nYou: ")
            if user_input.lower() == "exit":
                print("Exiting the chat...")
                break
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversastion History Cleared.")

            print("\nAssistant: ", end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"An error occurred: {e}")
    finally:
        if client and client.session:
            await client.close_all_session()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())

                

