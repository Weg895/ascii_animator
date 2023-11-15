import os, time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def setUp(filenames) :
    frames = []
    for name in filenames:
        with open(name, 'r', encoding="utf8") as f:
            frames.append(f.readlines())
    return frames
            
def animate(frames, clsActive, delay = 1 ) :
    while True :
        for frame in frames : 
            print(''.join(frame), end='', flush=True)
            time.sleep(delay)
            print('\r' + ' ' * len(frame[0]) + '\r', end='', flush=True)
            
            if clsActive : 
                 clear_screen()
                 
            if len(frames) == 1 :
                return
        
def getFrame(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        file_list = os.listdir(folder_path)
        return [folder_path + "/" + s for s in sorted(file_list, key=lambda x: int(x))]
    else:
        print("The folder path is not valid.")
        return []
      
def loop(frames, delay):
    direction = 1
    index = 0
    while True:
        print(''.join(frames[index]))
        time.sleep(delay)
        os.system('cls')

        if (index == 0 and direction == -1) or (index == len(frames) - 1 and direction == 1):
            direction = -direction 

        index += direction
      
def animator(foldername, delay, clsActive = False):
    print("Starting soon ...")
    frames = setUp(getFrame(foldername))
    animate(frames, clsActive, delay )
    
    
