import websocket
import sys
from basic_api import open_websocket_connection, queue_prompt, get_history, upload_image, prompt_to_image

# Global variable to control the running state
running = True

def main(positive_prompt, negative_prompt, image_path):
    global running
    ws = None  # Initialize ws to None
    try:
        print("Welcome to the image generation program!")
        
        # Establish WebSocket connection
        ws = open_websocket_connection()
        print("WebSocket connection established.")

        # If an image path is provided, upload the image
        if image_path:
            upload_image(image_path, "input_image", "127.0.0.1:8188")

        # Prepare the prompt as a structured dictionary with class types
        prompt_data = {
            'nodes': {
                'class_type': 'NodeGroup',  # Class type for the group
                'id': 'main_group',          # Example ID for the group
                '#positive_prompt': {
                    'class_type': 'PromptNode',  # Class type for positive prompt
                    'value': positive_prompt
                },
                '#negative_prompt': {
                    'class_type': 'PromptNode',  # Class type for negative prompt
                    'value': negative_prompt
                },
                'image_path': {
                    'class_type': 'ImageNode',  # Class type for image path
                    'value': image_path or "default_image_path"  # Ensure there's a valid path
                }
            }
        }

        # Sending the prompt as a structured dictionary
        print(f"Sending prompt: {prompt_data}")
        prompt_id = queue_prompt(prompt_data, "client_id_placeholder", "127.0.0.1:8188")['prompt_id']

        # Logic to receive images
        while running:
            response = ws.recv()  # Receive the response from the server
            print(f"Received response: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if ws:
            ws.close()  # Close the WebSocket connection properly


def generate_image_by_prompt(positive_prompt, negative_prompt, image_path, output_path, save_previews=False):
    """
    Generates an image based on a given text prompt and saves it to a specified path, optionally saving preview images.
    """
    # Logic to establish WebSocket connection and send the prompt
    try:
        ws = open_websocket_connection()
        # Prepare the prompt data
        prompt_data = {
            'nodes': {
                'class_type': 'NodeGroup',
                'id': 'main_group',  # Ensure a valid ID is provided
                '#positive_prompt': {
                    'class_type': 'PromptNode',
                    'value': positive_prompt
                },
                '#negative_prompt': {
                    'class_type': 'PromptNode',
                    'value': negative_prompt
                }
            }
        }
        # Include image path only if it is provided
        if image_path:
            prompt_data['nodes']['image_path'] = {
                'class_type': 'ImageNode',
                'value': image_path
            }
        else:
            print("No image path provided; skipping image path in prompt.")

        # Send the prompt to the server
        print(f"Sending prompt: {prompt_data}")
        prompt_id = queue_prompt(prompt_data, "client_id_placeholder", "127.0.0.1:8188")['prompt_id']
        # Logic to track progress and save the image
        # ... (additional logic for tracking and saving)
    except Exception as e:
        print(f"An error occurred during image generation: {e}")
    finally:
        if ws:
            ws.close()  # Ensure WebSocket connection is closed properly


def exit_program():
    print("Exiting the program...")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python gen.py <positive_prompt> <negative_prompt> <image_path>")
        exit_program()
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    # Example prompts for testing
    positive_prompt = "potato"  # Replace with actual input if needed
    negative_prompt = "mars"     # Replace with actual input if needed
    image_path = ""              # Optional image path
    
    main(positive_prompt, negative_prompt, image_path)
