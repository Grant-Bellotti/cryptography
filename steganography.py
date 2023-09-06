# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from os import path
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    def toBinary(self, data):
        """Convert `data` to binary format as string"""
        if type(data) == str:
            return ''.join([ format(ord(i), "08b") for i in data ])
        elif type(data) == bytes:
            return ''.join([ format(i, "08b") for i in data ])
        elif type(data) == np.ndarray:
            return [ format(i, "08b") for i in data ]
        elif type(data) == int or type(data) == np.uint8:
            return format(data, "08b")
        else:
            raise TypeError("Type not supported.")
    
    def encode(self, filein, fileout, message, codec):
        #image = cv2.imread(filein)
        image = cv2.imread(path.dirname(__file__) + "\\" + str(filein))
        #print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(message+self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary
            index = 0
            dataLength = len(binary)
            for row in image:
                for pixel in row:
                    # convert pixels into binary
                    r, g, b = self.toBinary(pixel)
                    if index < dataLength:
                        # red
                        pixel[0] = int(r[:-1] + binary[index], 2)
                        index += 1
                    if index < dataLength:
                        # green
                        pixel[1] = int(g[:-1] + binary[index], 2)
                        index += 1
                    if index < dataLength:
                        # blue
                        pixel[2] = int(b[:-1] + binary[index], 2)
                        index += 1
                    if index >= dataLength:
                        break

            #cv2.imwrite(fileout, image)
            cv2.imwrite(path.dirname(__file__) + "\\" + str(fileout), image)
                   
    def decode(self, filein, codec):
        #print(image) # for debugging    
        #image = cv2.imread(filein)  
        image = cv2.imread(path.dirname(__file__) + "\\" + str(filein))
        flag = True
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            binaryData = ""
            for row in image:
                for pixel in row:
                    r, g, b = self.toBinary(pixel)
                    binaryData += r[-1]
                    binaryData += g[-1]
                    binaryData += b[-1]
            self.text = self.codec.decode(binaryData)
            self.binary = self.codec.encode(self.text+self.codec.delimiter)    
        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        #plt.imshow(mpimg.imread(filename))
        plt.imshow(mpimg.imread(path.dirname(__file__) + "\\" + str(filename)))
        plt.show()

if __name__ == '__main__':
    
    s = Steganography()

    s.encode('fractal.jpg', 'fractal.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'

    s.decode('fractal.png', 'binary')
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')
