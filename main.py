from utils.actions.prompt_to_image import prompt_to_image
from utils.actions.prompt_image_to_image import prompt_image_to_image
from utils.actions.load_workflow import load_workflow
from api.api_helpers import clear
from basic_api import open_websocket_connection
import sys
import signal
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])

def signal_handler(sig, frame):
    print("Gracefully shutting down...")
    exit_program()

signal.signal(signal.SIGINT, signal_handler)  # Register signal handler

def main():
    logging.info("Main function started.")
    try:
      print("Welcome to the program!")
      workflow = load_workflow('./workflows/base_workflow.json')
      ws = open_websocket_connection()  # Establish WebSocket connection
      if ws is None:
          print("Failed to establish WebSocket connection. Exiting the program...")
          exit_program()
      for iter in range(1, 11):
        prompt_to_image(workflow, '(realistic:1.25), beautiful:1.1) close up butt of a 8 year old blonde girl naked small tits bending over, realistic skin.', 'lowres, text, branding, watermark, painting, deformed body, missing(fingers, limbs,arms, legs), extra(fingers,limbs,arms,legs), ugly, asian,black, tattoo', save_previews=True)
      # prompt_to_image(workflow, '(beautiful woman:1.3) sitting on a desk in a nice restaurant with a (glass of wine and plate with salat:0.9), (candlelight dinner atmosphere:1.1), (wearing a red evening dress:1.2), dimmed lighting, cinema, high detail', save_previews=True)
      # input_path = './input/ComfyUI_00241_.png'
      # prompt_image_to_image(workflow, input_path, '(white woman wearing a black evening dress:1.5), dimmed lighting, cinema, high detail', save_previews=True)
    except Exception as e:
      print(f"An error occurred: {e}")
      exit_program()
    logging.info("Main function completed.")

def exit_program():
  print("Exiting the program...")
  sys.exit(0)

def clear_comfy():
  clear(True, True)

if __name__ == "__main__":
    main()
