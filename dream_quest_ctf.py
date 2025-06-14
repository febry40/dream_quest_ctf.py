#!/usr/bin/env python3
import socket
import threading
import sys

class DreamQuestCTF:
    def __init__(self):
        self.flag = "TI404{fbrySl.latt∆mCH4.##blurr3d}"
        
    def send_message(self, client_socket, message):
        """Send message to client"""
        try:
            client_socket.send(message.encode('utf-8') + b'\r\n')
        except:
            return False
        return True
    
    def receive_input(self, client_socket):
        """Receive input from client"""
        try:
            data = client_socket.recv(1024).decode().strip().lower()
            return data
        except:
            return None
    
    def show_welcome(self, client_socket):
        """Display welcome screen"""
        welcome = """
===============================================
    WELCOME TO THE DREAM QUEST
===============================================

You find yourself standing at the edge of a mystical forest. 
Ancient runes glow softly on nearby trees, and you can hear 
whispers of forgotten knowledge carried by the wind.

A mysterious figure approaches you...

"Greetings, traveler! I am the Guardian of Digital Secrets. 
To obtain the flag you seek, you must prove your worth 
through wisdom and courage."

Choose your path:
A) Enter the Enchanted Forest
B) Seek the Oracle's Wisdom  
C) Challenge the Guardian directly
[a/b/c] > """
        return self.send_message(client_socket, welcome)
    
    def handle_forest_path(self, client_socket):
        """Handle forest path (dead end)"""
        message = """
You walk deeper into the forest. The trees whisper ancient codes...
But suddenly, you realize you're lost in an endless loop of trees.

💀 GAME OVER - Try again, brave soul! 💀

Connection will close in 3 seconds..."""
        self.send_message(client_socket, message)
        return False
    
    def handle_challenge_guardian(self, client_socket):
        """Handle direct challenge (returns to menu)"""
        message = """
The Guardian laughs heartily. "Brave, but foolish! 
One must earn wisdom before wielding power."

You are teleported back to the beginning...

Press Enter to continue..."""
        self.send_message(client_socket, message)
        self.receive_input(client_socket)  # Wait for Enter
        return True  # Return to main menu
    
    def handle_oracle_wisdom(self, client_socket):
        """Handle Oracle's wisdom path"""
        oracle_message = """

You approach the Oracle's chamber. She speaks in riddles:

"The flag you seek has these properties:
- It begins with the sacred prefix of your realm
- Contains the essence of your digital identity  
- Bears the symbol of change (triangle)
- Ends with the blur of confusion
- Numbers dance within: 404, 4, and thrice the first"

The Oracle presents you with three crystals:

A) Crystal of Truth - "TI404{fbrySl.latt∆mCH4.##blurr3d}"
B) Crystal of Deception - "FLAG{this_is_fake_flag_404}"  
C) Crystal of Illusion - "TI{wrong_format_here}"

Which crystal contains the true flag?
[a/b/c] > """
        
        while True:
            if not self.send_message(client_socket, oracle_message):
                return False
                
            choice = self.receive_input(client_socket)
            if choice is None:
                return False
                
            if choice == 'a':
                # Correct choice - show victory
                victory_message = f"""

=== CONGRATULATIONS! ===

The Crystal of Truth blazes with brilliant light!
You have proven yourself worthy, noble adventurer.

The Guardian nods approvingly: 
"Well done! You have shown wisdom in seeking knowledge 
before action, and discernment in recognizing truth 
from deception."

Your flag: {self.flag}

===============================================
    QUEST COMPLETED SUCCESSFULLY!
===============================================

Thank you for playing Dream Quest CTF!
"""
                self.send_message(client_socket, victory_message)
                return False  # End game
                
            elif choice in ['b', 'c']:
                # Wrong choice
                wrong_message = """
The crystal crumbles to dust. "Not all that glitters is gold..."
Try again, seeker of truth.

Press Enter to choose again..."""
                self.send_message(client_socket, wrong_message)
                self.receive_input(client_socket)  # Wait for Enter
                # Continue loop to show crystals again
                
            else:
                error_message = "Invalid choice. Please enter 'a', 'b', or 'c'."
                self.send_message(client_socket, error_message)
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        print(f"[+] Connection established with {address}")
        
        try:
            while True:
                # Show main menu
                if not self.show_welcome(client_socket):
                    break
                    
                # Get user choice
                choice = self.receive_input(client_socket)
                if choice is None:
                    break
                
                # Handle choices
                if choice == 'a':
                    # Forest path - game over
                    if not self.handle_forest_path(client_socket):
                        break
                        
                elif choice == 'b':
                    # Oracle path - main game
                    if not self.handle_oracle_wisdom(client_socket):
                        break
                        
                elif choice == 'c':
                    # Challenge guardian - return to menu
                    if not self.handle_challenge_guardian(client_socket):
                        break
                        
                else:
                    error_msg = "Invalid choice. Please enter 'a', 'b', or 'c'."
                    if not self.send_message(client_socket, error_msg):
                        break
                        
        except Exception as e:
            print(f"[-] Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"[-] Connection closed with {address}")

def start_server(host='localhost', port=12345):
    """Start the CTF server"""
    ctf_game = DreamQuestCTF()
    
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind and listen
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[*] Dream Quest CTF Server started on {host}:{port}")
        print(f"[*] Connect using: nc {host} {port}")
        print("[*] Press Ctrl+C to stop the server")
        
        while True:
            # Accept connections
            client_socket, address = server_socket.accept()
            
            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=ctf_game.handle_client,
                args=(client_socket, address)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n[*] Server shutting down...")
    except Exception as e:
        print(f"[-] Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 12345

    
    # Allow custom host/port via command line
    if len(sys.argv) >= 2:
        PORT = int(sys.argv[1])
    if len(sys.argv) >= 3:
        HOST = sys.argv[2]
    
    start_server(HOST, PORT)