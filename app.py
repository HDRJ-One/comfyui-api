from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from database import init_db
import logging
import subprocess
import os
import signal
import uuid
from basic_api import queue_prompt, get_history, get_images

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Graceful shutdown handler
def signal_handler(sig, frame):
    logging.info('Received shutdown signal. Exiting...')
    exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Create the Flask app and set the static folder
app = Flask(__name__, static_folder='output')

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

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        client_id = str(uuid.uuid4())  # Generate a unique client ID
        server_address = '127.0.0.1:8188'
        response = queue_prompt(prompt, client_id, server_address)
        # Fetch the history of the prompt
        prompt_id = response.get('id')  # Assuming the response contains an ID
        history = get_history(prompt_id, server_address)
        images = get_images(prompt_id, server_address, allow_preview=True)
        return render_template('index.html', history=history, images=images)
    return render_template('index.html')

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        prompt = request.form['prompt']
        # Call the function from main.py to generate image
        status = run_image_generation(prompt)
        return redirect(url_for('index2'))
    return render_template('index.html')

@app.route('/index3', methods=['GET', 'POST'])
def index3():
    if request.method == 'POST':
        prompt = request.form['prompt']
        # Call the function from main.py to generate image
        status = run_image_generation(prompt)
        return redirect(url_for('index3'))
    return render_template('index.html')

def run_image_generation(prompt):
    # Call main.py and capture output
    process = subprocess.Popen(['python', 'c:/photogen/comfyui-api/main.py', prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return {'output': stdout.decode('utf-8'), 'error': None}  # Return the output and no error
    else:
        logging.error(f'Error in image generation: {stderr.decode("utf-8")}')
        return {'output': None, 'error': stderr.decode('utf-8')}  # Return no output and the error message

@app.route('/generate', methods=['POST'])
def generate_image_with_prompts():
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

@app.route('/generate_image', methods=['POST'])
def generate_image():
    global running_process
    # Start the main.py process and redirect stdout and stderr to the console
    running_process = subprocess.Popen(
        ['python', 'c:/photogen/comfyui-api/main.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Capture output as text
    )
    
    # Log the output and errors
    for line in iter(running_process.stdout.readline, ''):
        logging.info(line.strip())
    for line in iter(running_process.stderr.readline, ''):
        logging.error(line.strip())
    
    running_process.stdout.close()
    running_process.stderr.close()
    return jsonify({'status': 'Image generation started'})

@app.route('/generate_image_with_empty_prompt', methods=['POST'])
def generate_image_with_empty_prompt():
    # Call the run_image_generation function without a prompt
    result = run_image_generation('')  # Pass empty string or predefined prompt
    if result and result['output']:
        image_data = result['output']  # Assuming output contains base64 image data
        return jsonify({'image': image_data})
    return jsonify({'image': None}), 500

@app.route('/generate_image_button', methods=['POST'])
def generate_image_button():
    # This function is no longer needed if the above is sufficient
    pass  # Or implement any other logic if needed

@app.route('/get_images', methods=['GET'])
def get_images():
    output_dir = 'output'
    images = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return jsonify({'images': [{'name': image} for image in images]})  # Ensure it returns a list of objects with 'name' keys

@app.route('/retrieve_images', methods=['GET'])
def retrieve_images():
    output_dir = 'output'
    images = []
    for filename in os.listdir(output_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Add other image types if needed
            images.append({'name': filename})
    return jsonify({'images': images})

@app.route('/get_last_generated_image', methods=['GET'])
def get_last_generated_image():
    output_dir = 'output'
    images = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        last_image = sorted(images)[-1]  # Get the last image based on alphabetical order
        return jsonify({'image_name': last_image})
    return jsonify({'image_name': None}), 404

@app.route('/serve_last_generated_image', methods=['GET'])
def serve_last_generated_image():
    output_dir = 'output'
    images = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        last_image = sorted(images)[-1]  # Get the last image based on alphabetical order
        return send_file(os.path.join(output_dir, last_image), mimetype='image/jpeg')
    return jsonify({'error': 'No images found'}), 404

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=8100)
    except Exception as e:
        logging.error(f'Error running the application: {e}')
