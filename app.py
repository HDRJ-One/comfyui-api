from flask import Flask, render_template, request
from database import init_db
import logging
import subprocess
import os
from gen import main, exit_program
import signal

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Graceful shutdown handler
def signal_handler(sig, frame):
    logging.info('Received shutdown signal. Exiting...')
    exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

app = Flask(__name__)

# Initialize the database
init_db()

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f'An error occurred: {e}')
    return render_template('error.html', error=str(e)), 500

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f'Error rendering home page: {e}')
        return handle_exception(e)

@app.route('/generate', methods=['POST'])
def generate_image():
    logging.info(f"Received request with data: {request.form}")
    logging.info(f"Request data: positive_prompt={request.form.get('positive_prompt')}, negative_prompt={request.form.get('negative_prompt')}, image_path={request.form.get('image_path', '')}")
    positive_prompt = request.form.get('positive_prompt')
    negative_prompt = request.form.get('negative_prompt')
    image_path = request.form.get('image_path', '')
    
    # Validate inputs
    if not positive_prompt:
        return "Positive prompt is required!", 400
    if not negative_prompt:
        return "Negative prompt is required!", 400
    
    # Call the main function from gen.py with the provided prompts
    try:
        main(positive_prompt, negative_prompt, image_path)
        return "Image generation started!", 200
    except Exception as e:
        logging.error(f'Error generating image: {e}')
        return f"An error occurred: {str(e)}", 500

@app.route('/generate_photo', methods=['POST'])
def generate_photo():
    prompt = request.form['prompt']
    logging.debug(f'Received prompt: {prompt}')
    try:
        # Call the main function from main.py to generate images
        subprocess.run(['python', 'main.py'], check=True)
        return "Photo generation process started!"
    except Exception as e:
        logging.error(f'Error generating photo: {e}')
        return handle_exception(e)

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=8100)
    except Exception as e:
        logging.error(f'Error running the application: {e}')
