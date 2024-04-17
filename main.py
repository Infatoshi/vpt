import minerl
import gym
import cv2
import json
import pygame
import numpy as np
# import torch
import pickle
import os

img_scaling = 0.25

samples = 1
output_video_path = os.getcwd()

for i in range(samples):
        # Initialize pygame
    pygame.init()

    frames = []

    # Constants
    OUTPUT_VIDEO_FILE = f"{output_video_path}/data/labeller-training/video/mc-{i}.mp4"
    # ACTION_LOG_FILE = f"/mnt/d/py/vpt/data/labeller-training/actions/mc-{i}.json"
    FPS = 30
    RESOLUTION = (640, 360)  # Resolution at which to capture and save the video
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption('Minecraft')
    SENS = 0.05

    # Set up the OpenCV video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO_FILE, fourcc, FPS, RESOLUTION)

    pygame.mouse.set_visible(False)
    pygame.mouse.set_pos(screen.get_width() // 2, screen.get_height() // 2)  # Center the mouse
    pygame.event.set_grab(True)

    prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()

    # Mapping from pygame key to action
    key_to_action_mapping = {
        pygame.K_w: {'forward': 1},
        pygame.K_s: {'back': 1},
        pygame.K_a: {'left': 1},
        pygame.K_d: {'right': 1},
        pygame.K_SPACE: {'jump': 1},
        pygame.K_1: {'hotbar.1': 1},
        pygame.K_2: {'hotbar.2': 1},
        pygame.K_3: {'hotbar.3': 1},
        pygame.K_4: {'hotbar.4': 1},
        pygame.K_5: {'hotbar.5': 1},
        pygame.K_6: {'hotbar.6': 1},
        pygame.K_7: {'hotbar.7': 1},
        pygame.K_8: {'hotbar.8': 1},
        pygame.K_9: {'hotbar.9': 1},
        pygame.K_LSHIFT: {'sprint': 1},
        pygame.K_LCTRL: {'sneak': 1},
        pygame.K_g: {'drop': 1},
        pygame.K_e: {'inventory': 1},
        pygame.K_f: {'swapHands': 1},
        pygame.K_t: {'pickItem': 1}
        }
        # ... movement keys, jump, crouch, sprint, hotbar, attack, use, inventory, drop, swaphands, pickitem
    # Mapping from mouse button to action
    mouse_to_action_mapping = {
        0: {'attack': 1},      # Left mouse button
        2: {'use': 1}    # Right mouse button
        # Add more if needed
    }
    
    action_log = []

    # Initialize the Minecraft environment
    env = gym.make('MineRLBasaltBuildVillageHouse-v0')


    env.seed(2143)
    obs = env.reset()
   
    done = False
    """
    # action_space = {"ESC": 0,
    #          "noop": [], 
    #          "attack": 0, 
    #          "back": 0, 
    #          "drop": 0, 
    #          "forward": 0, 
    #          "hotbar.1": 0, 
    #          "hotbar.2": 0, 
    #          "hotbar.3": 0, 
    #          "hotbar.4": 0, 
    #          "hotbar.5": 0, 
    #          "hotbar.6": 0, 
    #          "hotbar.7": 0, 
    #          "hotbar.8": 0, 
    #          "hotbar.9": 0, 
    #          "inventory": 0, 
    #          "jump": 0, 
    #          "left": 0, 
    #          "right": 0, 
    #          "pickItem": 0, 
    #          "sneak": 0, 
    #          "sprint": 0, 
    #          "swapHands": 0, 
    #          "use": 0,
    #          "camera": [0.0, 0.0]}
    """
    try:
        while not done:
            # Convert the observation to a format suitable for pygame display
            image = np.array(obs['pov'])
            # image = cvtColor(image, cv2)
            # Record the current frame
            
            # print(image.shape)
            # out_image = cv2.resize(image, (int(360 * img_scaling), int(640 * img_scaling)))
            out.write(image)
            # cv2.imshow('temp', image)
            image = np.flip(image, axis=1)
            image = np.rot90(image)
            # image = image * 0.1 # <- brightness
            image = pygame.surfarray.make_surface(image)
            screen.blit(image, (0, 0))
            pygame.display.update()
        
            # Get the current state of all keys
            keys = pygame.key.get_pressed()
        
            action = {'noop': []}
            for key, act in key_to_action_mapping.items():
                if keys[key]:
                    action.update(act)
            
            # Get mouse button states
            mouse_buttons = pygame.mouse.get_pressed()
            for idx, pressed in enumerate(mouse_buttons):
                if pressed:
                    action.update(mouse_to_action_mapping.get(idx, {}))
            
            # Get mouse movement
            mouse_x, mouse_y = pygame.mouse.get_pos()
            delta_x = mouse_x - prev_mouse_x
            delta_y = mouse_y - prev_mouse_y
        
            # Reset mouse to the center of the window
            pygame.mouse.set_pos(screen.get_width() // 2, screen.get_height() // 2)
            prev_mouse_x, prev_mouse_y = screen.get_width() // 2, screen.get_height() // 2
        
            # Now, use delta_x and delta_y for the camera movement
            action['camera'] = [delta_y * SENS, delta_x * SENS]
        
            # Add the in-game 'ESC' action to the beginning of the action
            action = {'ESC': 0, **action}
            action_log.append(action)
        
            # Apply the action in the environment
            obs, reward, done, _ = env.step(action)
        
            # Check if the 'q' key is pressed to terminate the loop
            if keys[pygame.K_q]:
                break
        
            # Handle pygame events to avoid the window becoming unresponsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
    except KeyboardInterrupt:
        pass
    finally:    
        # env.render()
        # Cleanup
        out.release()
        # cv2.destroyAllWindows()
        pygame.quit()
        
        # # Save the actions to a JSON file
        # with open(ACTION_LOG_FILE, 'w') as f:
        #     json.dump(action_log, f)

    cv2.namedWindow('Recorded Video', cv2.WINDOW_NORMAL)
    cap = cv2.VideoCapture(OUTPUT_VIDEO_FILE)

    if not cap.isOpened():
        print("Error: Could not open video file.")
    else:
        # Set the video capture to return grayscale frames
        # cap.set(cv2.CAP_PROP_CONVERT_RGB, False)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('Recorded Video', frame)
            
            # Adjust the delay for cv2.waitKey() if the playback speed is not correct
            if cv2.waitKey(int(1000/FPS)) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

