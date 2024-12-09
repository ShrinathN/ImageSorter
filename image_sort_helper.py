#!/bin/python3

from kcpp import KoboldCppTextGen

#repeat counter, basically the number of times we want the repeat the session
REPEAT = 5

def simple_prompt_with_image(image_path, second_prompt, base_prompt="What is this image of? Any text in the image?"):
    #setting the server
    #this assumes the server is being hosted on localhost with 8080 as the port and API enabled
    #set change the server if required
    kcpp_server = KoboldCppTextGen()
    #converting image to 512x512 JPEG and putting it into the image field of the request
    kcpp_server.attach_image_simple(image_path)

    #we need to prompt the image multiple times because LLMs like to hallucinate
    output_buffer = []
    i = 0
    while(i < REPEAT):
        #base prompt
        prompt_text = f"\n(Attached Image)\n\n### Instruction:\n{base_prompt}\n### Response:\n"
        kcpp_server.set_max_length(300)
        response_1 = kcpp_server.generate_text(prompt_text)

        #asking if its a meme image
        prompt_text += response_1 + f"\n### Instruction:\n{second_prompt}. Answer with a simple yes or no and nothing else.\n### Response:\n"
        kcpp_server.set_max_length(1)
        response_2 = kcpp_server.generate_text(prompt_text)

        #only if it contains a "Yes" or "No", will we proceed
        if(response_2.replace("\n","").replace(".","") == "No" or response_2.replace("\n","").replace(".","") == "Yes"):
            output_buffer.append(response_2)
            i += 1

    #finally counting the number of "Yes" and returning
    #if >50% of responses are positive, we consider it a yes
    if(output_buffer.count("Yes") > (REPEAT / 2)):
        return True
    else:
        return False

def simple_get_response(image_path, second_prompt, base_prompt="What is this image of? Any text in the image?"):
    #setting the server
    #this assumes the server is being hosted on localhost with 8080 as the port and API enabled
    #set change the server if required
    kcpp_server = KoboldCppTextGen()
    #converting image to 512x512 JPEG and putting it into the image field of the request
    kcpp_server.attach_image_simple(image_path)
    
    #base prompt
    prompt_text = f"\n(Attached Image)\n\n### Instruction:\n{base_prompt}\n### Response:\n"
    kcpp_server.set_max_length(300)
    response_1 = kcpp_server.generate_text(prompt_text)

    #asking if its a meme image
    prompt_text += response_1 + f"\n### Instruction:\n{second_prompt}\n### Response:\n"
    kcpp_server.set_max_length(300)
    response_2 = kcpp_server.generate_text(prompt_text)
    return response_2