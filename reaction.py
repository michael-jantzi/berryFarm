import minescript
import datetime
import os
import time

# Configure log file path
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"chat_log_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt")

def on_chat_message(event):
    """Handle chat message events and log them to a file"""
    # Get message content
    message = event["message"]
    
    # Format with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    # Write to log file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    # Optional: Echo to console that message was logged
    minescript.echo(f"Logged: {message}")

def main():
    # Register the chat message listener
    minescript.event.on_chat_message(on_chat_message)
    
    # Print startup message
    minescript.echo(f"Chat logger started. Logging to: {log_file}")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        minescript.echo("Chat logger stopped.")
    except Exception as e:
        minescript.echo(f"Error in chat logger: {e}")

if __name__ == "__main__":
    main()
