import keyboard, time, random
import os, win32com.client, win32con, win32gui as w32gui, win32api as w32
import PIL.ImageGrab as GetImg

import ctypes as ct
import numpy as np

WIN_NAME = "Snes9X v1.43 for Windows"
KEYS = {"d": 0x44, "x": 0x58, "z": 0x5A, "enter": win32con.VK_RETURN}
KEYS_LIST = [KEYS["d"], KEYS["x"], KEYS["z"], KEYS["enter"]]
MAX_WEIGHT = 2
SLEEP_TIME = 0.02

# author: LW

class NeuralNetwork():
        def __init__(self, pixelData):
                self.firstLayer = []
                for x in range(0, len(pixelData)):
                        self.firstLayer.append(0)
                self.weights = []
                self.weightMatrix = np.array
                self.outputLayer = KEYS_LIST * 2 # for key press and release
                self.activation = np.array

        def setupRandomLayerFirst(self):
                # create layers (only 2 atm)
                for idx, out in enumerate(self.outputLayer):
                        self.weights.append([])
                        for pixel in self.firstLayer:
                                self.weights[idx].append(random.uniform(0, MAX_WEIGHT))
                self.weightMatrix = np.array(self.weights)
                
        def randomizeWeights(self):
                 # create layers (only 2 atm)
                for x in range(0, len(self.weights)):
                        for y in range(0, len(self.weights[x])):
                                self.weights[x][y] = random.uniform(0, MAX_WEIGHT)
                print("w0: ", self.weights[0][0])
                self.weightMatrix = np.array(self.weights)

        def transform(self, pixelData):
                for idx, pixel in enumerate(pixelData):
                        self.firstLayer[idx] = pixel[0] + pixel[1] + pixel[2] # grayscale?
                self.activation = self.weightMatrix.dot(np.array(self.firstLayer))

        def getActivatedNeurons(self):
                activated = []
                
                for idx, val in enumerate(self.activation):
                        if (val / len(self.firstLayer)) > 390.4: # bias test
                                activated.append(idx)
                                
                return activated
                

def getImageOfWindow(hwnd):
        rect = w32gui.GetWindowRect(hwnd)
        img = GetImg.grab((rect[0], rect[1], rect[2], rect[3]))
        return img

def getPixelsTotal(hwnd):
        return len(getImageOfWindow(hwnd).getdata())

def readScoreMemory(hwnd):
        return 0

def main():
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.appActivate(WIN_NAME)
        
        WIN_ID = w32gui.FindWindow(None, WIN_NAME)
        random.seed(None)

        network = NeuralNetwork(getImageOfWindow(WIN_ID).getdata())
        network.setupRandomLayerFirst()
        loop = 0

        print("Loop Started")
        while not keyboard.is_pressed('q'):
                loop += 1
                network.transform(getImageOfWindow(WIN_ID).getdata())
                print("Act Neu: ", len(network.getActivatedNeurons()))
                for val in network.getActivatedNeurons():
                        if (val > len(KEYS_LIST)):
                                w32.keybd_event(network.outputLayer[val], 0, 0, 0)
                        else:
                                w32.keybd_event(network.outputLayer[val], 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(SLEEP_TIME)

                if loop % 100 is 0:
                        network.randomizeWeights() # just testing stuff
        print("Loop Ended")
                        
        shell.appActivate("Python 3.6.4 Shell")

        # w32.PostMessage(WIN_ID, win32con.WM_KEYUP, KEYS["d"], 0)
        # w32.PostMessage(WIN_ID, win32con.WM_KEYDOWN, KEYS["d"], 0xF000)
main()
