# main.py
from brain import think
from tools import AVAILABLE_TOOLS
import re

def main():
    print("--- JARVIS v1 ONLINE ---")
    print("Type 'exit' to go offline.")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == 'exit':
            break

        # 1. Let the brain think
        response = think(user_input)

        # 2. Check if the brain wants to use a tool
        # We use a more flexible regex to capture the tool and the arguments
        match = re.search(r"TOOL:\s*(\w+)\((.*)\)", response)

        if match:
            tool_name = match.group(1)
            arg_string = match.group(2)

            if tool_name in AVAILABLE_TOOLS:
                # DEBUG: This tells us exactly what Jarvis is thinking
                print(f"[*] Jarvis decided to use: {tool_name} with args: ({arg_string})")

                func = AVAILABLE_TOOLS[tool_name]

                try:
                    # Split arguments by comma and clean them up
                    # This handles "key, value" -> ["key", "value"]
                    if arg_string.strip():
                        args = [a.strip().strip('"').strip("'") for a in arg_string.split(',')]
                    else:
                        args = []

                    result = func(*args)
                    print(f"Jarvis: {result}")
                except Exception as e:
                    print(f"Jarvis: I encountered an error executing that tool: {e}")
            else:
                print(f"Jarvis: I see you want {tool_name}, but that tool isn't installed.")
        else:
            # Just a normal chat response
            print(f"Jarvis: {response}")

if __name__ == "__main__":
    main()