#!/bin/python
'''
This is an example program which brute forces the LLaVA model to recognise meme images
'''

from image_sort_helper import simple_prompt_with_image


response = simple_prompt_with_image("example.jpg", "Does the image appear to be a meme image?", "You are an image inspecting service, study the image thoroughly and respond describing its contents.")
print("Meme found!" if(response) else "Not a meme")