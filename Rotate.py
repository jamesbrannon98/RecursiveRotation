import sys
import math
import cv2 as cv
import numpy as np

class Rotate(object):

    def __init__(self, fileName, output):
        self.fileName = fileName
        self.image = cv.imread(fileName)
        self.output = output

    def check_size(self):
        if self.image.shape[0] != 0:
            if self.image.shape[0] == self.image.shape[1]:
                if (self.image.shape[0] & (self.image.shape[0] - 1) == 0):
                    return True
        return False

    def resize_image(self):
        newDimension = 2**round(math.log(min(self.image.shape[0], self.image.shape[1]), 2))
        self.image = cv.resize(self.image, (newDimension, newDimension))

    def rotate(self):
        if not(self.check_size()):
            print("Image provided is not N x N, where N is a power of 2.")
            print("Resizing image.")
            self.resize_image()
        dimensions = self.image.shape[0]
        out = cv.VideoWriter(self.output, cv.VideoWriter_fourcc('m','p','4','v'), 30, (dimensions, dimensions))
        for i in range(4):
            width = dimensions // 2
            frames = 2 * int(math.log2(dimensions))
            while width > 1:
                frames -= 2
                frames = max(1, frames)
                for i in range(0, frames):
                    output_canvas = np.copy(self.image)
                    shift = (width * (i + 1)) // frames
                    for x in range(0, dimensions, 2 * width):
                        for y in range(0, dimensions, 2 * width):
                            self.rotateWithSteps(output_canvas, x, y, width, shift)
                    cv.imshow('output', output_canvas)
                    cv.waitKey(1)
                    out.write(output_canvas)
                self.image = np.copy(output_canvas)
                width = width // 2
        out.release()
        print("Done!")

    def rotateWithSteps(self, output, x, y, width, shift):
        temp = np.copy(self.image[y:y + width, x:x + width])
        output[y + width - shift:y + 2 * width - shift, x:x + width] = self.image[y + width:y + 2 * width, x:x + width]
        output[y + width:y + 2 * width, x + width - shift:x + 2 * width - shift] = self.image[y + width:y + 2 * width, x + width:x + 2 * width]
        output[y + shift:y + width + shift, x + width:x + 2 * width] = self.image[y:y + width, x + width:x + 2 * width]
        output[y:y + width, x + shift:x + width + shift] = temp

if len(sys.argv) != 3:
    print("Correct Format: Rotate.py <input> <output>")
    sys.exit()

input_image = sys.argv[1]
output_video = sys.argv[2]
rotate = Rotate(input_image, output_video)
rotate.rotate()
