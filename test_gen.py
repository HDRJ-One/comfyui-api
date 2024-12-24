import unittest
from gen import main, queue_prompt, generate_image_by_prompt
import logging
from utils.actions.load_workflow import load_workflow

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestGen(unittest.TestCase):
    def setUp(self):
        self.workflow = load_workflow('./workflows/base_workflow.json')  # Load the workflow for testing

    def test_queue_prompt_function(self):
        # Test the queue_prompt function directly with a known valid prompt structure
        prompt = {'nodes': {'class_type': 'NodeGroup', 'id': 'main_group',
                            '#positive_prompt': {'class_type': 'PromptNode', 'value': '(realistic:1.25), beautiful:1.1) 8 year old blonde girl naked small tits bending over, realistic skin.'},
                            '#negative_prompt': {'class_type': 'PromptNode', 'value': 'lowres, text, branding, watermark, painting, deformed body, missing(fingers, limbs,arms, legs), extra(fingers,limbs,arms,legs), ugly, asian,black, tattoo'},
                            'image_path': {'class_type': 'ImageNode', 'value': ''}}}
        client_id = 'test_client'
        server_address = '127.0.0.1:8188'

        try:
            logger.info(f"Attempting to queue prompt: {prompt}")  # Log the prompt
            response = queue_prompt(prompt, client_id, server_address)
            logger.info(f"Queue prompt response: {response}")  # Log the response
            self.assertIsInstance(response, dict)  # Ensure response is a dictionary
        except Exception as e:
            logger.error(f"Error during queue_prompt: {e}")  # Log the error
            self.fail(f'queue_prompt raised an exception: {e}')

    def test_generate_image_by_prompt(self):
        # Test the generate_image_by_prompt function with a known valid prompt
        positive_prompt = '(realistic:1.25), beautiful:1.1) 8 year old blonde girl naked small tits bending over, realistic skin.'
        negative_prompt = 'lowres, text, branding, watermark, painting, deformed body, missing(fingers, limbs,arms, legs), extra(fingers,limbs,arms,legs), ugly, asian,black, tattoo'
        image_path = ''
        output_path = './output/test_image.png'

        try:
            logger.info(f"Attempting to generate image with prompts: positive={positive_prompt}, negative={negative_prompt}")  # Log the prompts
            response = generate_image_by_prompt(positive_prompt, negative_prompt, image_path, output_path)
            logger.info(f"Generate image response: {response}")  # Log the response
            if response is None:
                logger.warning("Response was None, indicating an error occurred during image generation.")
            self.assertIsNotNone(response)  # Check if response is not None
            self.assertIn('image_data', response)  # Check if image_data is in response
        except Exception as e:
            logger.error(f"Error during generate_image_by_prompt: {e}")  # Log the error
            self.fail(f'generate_image_by_prompt raised an exception: {e}')

if __name__ == '__main__':
    unittest.main()
