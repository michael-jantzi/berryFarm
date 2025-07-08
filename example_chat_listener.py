import minescript

def on_chat(event):
    # event["message"] contains the chat message
    minescript.echo(f"Chat: {event['message']}")

def main():
    # Register the chat event handler
    minescript.event.on_chat_message(on_chat)
    # Keep the script running
    while True:
        minescript.sleep(1)

if __name__ == "__main__":
    main()
