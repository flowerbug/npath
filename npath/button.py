from math import sqrt

import pyglet
from pyglet.window import mouse
from pyglet.image import SolidColorImagePattern, ImageData


def delta_color(color, border_color, delta):

   new_color = []
   for x in range( len(color)-1):
       y = color[x] - border_color[x] + delta
       new_color.append(y)

   # alpha channel is different
   if (color[3] == border_color[3]):
       new_color.append(color[3])
   else:
       y = color[3] - border_color[3]
       new_color.append(y)
   return (new_color)


def step_color(color_delta, border_size):

   step_color_l = []
   for x in color_delta:
       y = x / border_size
       step_color_l.append(y)
   return (step_color_l)


def adj_value(value, amount):

   value += amount
   if (value < 0):
       return (0)
   if (value > 255):
       return (255)
   return (value)


class SolidColorButtonImagePatternV00(SolidColorImagePattern):
    """Creates a beveled button image filled with a solid color."""


    def __init__(self, color=(0, 0, 0, 0), border_color=(0,0,0,255)):
        """Create a beveled image pattern with color and blend the 
                border towards border_color.

        :Parameters:
            `color` : (int, int, int, int)
                4-tuple of ints in range [0,255] giving RGBA components of
                color to fill with.
            `border_color` : (int, int, int, int)
                4-tuple of ints in range [0,255] giving RGBA components of
                the border color to blend towards.

        """
        if len(color) != 4:
            raise TypeError("color is expected to have 4 components")
        self.color = list(color)
        self.border_color = list(border_color)


    def create_image(self, width, height):

        data = self.color * width * height

        if (width < 3) or (height < 3):
            print ("width or height < 3 : ", width, height, "  No Border Applied to image.")
            img_data = ImageData(width, height, 'RGBA', bytes(data))
            return img_data

        x_border = int(width / sqrt(width))
        y_border = int(height / sqrt(height))
        if (x_border == 0):
            x_border = 1
        if (y_border == 0):
            y_border = 1

        # so the borders are uniform make sure they are the same size
        # even if the width and height of the tiles are different
        if (x_border != y_border):
            y_border = (x_border + x_border) // 2
            x_border = y_border

        # how many gradient steps to use for each part of the color and alpha
        step_x_red = (self.border_color[0] - self.color[0]) / x_border
        step_y_red = (self.border_color[0] - self.color[0]) / y_border
        step_x_green = (self.border_color[1] - self.color[1]) / x_border
        step_y_green = (self.border_color[1] - self.color[1]) / y_border
        step_x_blue = (self.border_color[2] - self.color[2]) / x_border
        step_y_blue = (self.border_color[2] - self.color[2]) / y_border
        step_x_alpha = (self.border_color[3] - self.color[3]) / x_border
        step_y_alpha = (self.border_color[3] - self.color[3]) / y_border

        # bottom and top row(s)
        red_x = self.border_color[0]
        green_x = self.border_color[1]
        blue_x = self.border_color[2]
        alpha_x = self.border_color[3]
        for x in range(x_border):
            for y in range(width-(x*2)):
                indx_lower = (x*width*4)+((y+x)*4)
                indx_upper = ((height-(x+1))*width*4)+((y+x)*4)
                data[indx_lower] = int(red_x)
                data[indx_upper] = int(red_x)
                data[indx_lower+1] = int(green_x)
                data[indx_upper+1] = int(green_x)
                data[indx_lower+2] = int(blue_x)
                data[indx_upper+2] = int(blue_x)
                data[indx_lower+3] = int(alpha_x)
                data[indx_upper+3] = int(alpha_x)

            red_x -= step_x_red
            green_x -= step_x_green
            blue_x -= step_x_blue
            alpha_x -= step_x_alpha

        # left and right col(s)
        red_y = self.border_color[0]
        green_y = self.border_color[1]
        blue_y = self.border_color[2]
        alpha_y = self.border_color[3]
        for x in range(y_border):
            for y in range(height-(x*2)):
                indx_left = (((y+x)*height)+(x))*4
                indx_right = (((y+x)*height)+(width-x-1))*4
                data[indx_left] = int(red_y)
                data[indx_right] = int(red_y)
                data[indx_left+1] = int(green_y)
                data[indx_right+1] = int(green_y)
                data[indx_left+2] = int(blue_y)
                data[indx_right+2] = int(blue_y)
                data[indx_left+3] = int(alpha_y)
                data[indx_right+3] = int(alpha_y)

            red_y -= step_y_red
            green_y -= step_y_green
            blue_y -= step_y_blue
            alpha_y -= step_y_alpha

        img_data = ImageData(width, height, 'RGBA', bytes(data))
        return img_data


class SolidColorButtonImagePattern(SolidColorImagePattern):
    """Creates a beveled button image filled with a solid color."""


    def __init__(self, color=(0, 0, 0, 0), border_color=(0,0,0,255)):
        """Create a beveled image pattern with color and blend the 
                border towards border_color.  Make the upper and left
                borders lighter and the right and bottom borders darker.

        :Parameters:
            `color` : (int, int, int, int)
                4-tuple of ints in range [0,255] giving RGBA components of
                color to fill with.
            `border_color` : (int, int, int, int)
                4-tuple of ints in range [0,255] giving RGBA components of
                the border color to blend towards.

        """
        if len(color) != 4:
            raise TypeError("color is expected to have 4 components")
        self.color = list(color)
        self.border_color = list(border_color)


    def create_image(self, width, height):

        data = self.color * width * height

        if (width < 3) or (height < 3):
            print ("width or height < 3 : ", width, height, "  No Border Applied to image.")
            img_data = ImageData(width, height, 'RGBA', bytes(data))
            return img_data

        x_border = int(width / (sqrt(width)*2))
        y_border = int(height / (sqrt(height)*2))
        if (x_border == 0):
            x_border = 1
        if (y_border == 0):
            y_border = 1

        # so the borders are uniform make sure they are the same size
        # even if the width and height of the tiles are different
        if (x_border != y_border):
            border_size = (x_border + x_border) // 2
        else:
            border_size = x_border

        print("Border Size : ", border_size)

        # the gradient steps to use for each part of the color and alpha
        # for the four sides
        delta_top_color = step_color(delta_color(self.color, self.border_color, 96), border_size)
        print("Delta Top Color : ", delta_top_color)
        delta_bottom_color = step_color(delta_color(self.color, self.border_color, -64), border_size)
        print("Delta Bottom Color : ", delta_bottom_color)
        delta_left_color = step_color(delta_color(self.color, self.border_color, 64), border_size)
        print("Delta Left Color : ", delta_left_color)
        delta_right_color = step_color(delta_color(self.color, self.border_color, -64), border_size)
        print("Delta Right Color : ", delta_right_color)

        # top row(s)
        red_x = self.border_color[0]
        green_x = self.border_color[1]
        blue_x = self.border_color[2]
        alpha_x = self.border_color[3]
        for x in range(border_size):
            for y in range(width-(x*2)):
                indx_upper = ((height-(x+1))*width*4)+((y+x)*4)
                data[indx_upper] = int(red_x)
                data[indx_upper+1] = int(green_x)
                data[indx_upper+2] = int(blue_x)
                data[indx_upper+3] = int(alpha_x)
            red_x = adj_value(red_x, delta_top_color[0])
            green_x = adj_value(green_x, delta_top_color[1])
            blue_x = adj_value(blue_x, delta_top_color[2])
            alpha_x = adj_value(alpha_x, delta_top_color[3])

        # bottom row(s)
        red_x = self.border_color[0]
        green_x = self.border_color[1]
        blue_x = self.border_color[2]
        alpha_x = self.border_color[3]
        for x in range(border_size):
            for y in range(width-(x*2)):
                indx_lower = (x*width*4)+((y+x)*4)
                data[indx_lower] = int(red_x)
                data[indx_lower+1] = int(green_x)
                data[indx_lower+2] = int(blue_x)
                data[indx_lower+3] = int(alpha_x)
            red_x = adj_value(red_x, delta_bottom_color[0])
            green_x = adj_value(green_x, delta_bottom_color[1])
            blue_x = adj_value(blue_x, delta_bottom_color[2])
            alpha_x = adj_value(alpha_x, delta_bottom_color[3])

        # left col(s)
        red_y = self.border_color[0]
        green_y = self.border_color[1]
        blue_y = self.border_color[2]
        alpha_y = self.border_color[3]
        for x in range(border_size):
            for y in range(height-(x*2)):
                indx_left = (((y+x)*height)+(x))*4
                data[indx_left] = int(red_y)
                data[indx_left+1] = int(green_y)
                data[indx_left+2] = int(blue_y)
                data[indx_left+3] = int(alpha_y)
            red_y = adj_value(red_y, delta_left_color[0])
            green_y = adj_value(green_y, delta_left_color[1])
            blue_y = adj_value(blue_y, delta_left_color[2])
            alpha_y = adj_value(alpha_y, delta_left_color[3])

        # right col(s)
        red_y = self.border_color[0]
        green_y = self.border_color[1]
        blue_y = self.border_color[2]
        alpha_y = self.border_color[3]
        for x in range(border_size):
            for y in range(height-(x*2)):
                indx_right = (((y+x)*height)+(width-x-1))*4
                data[indx_right] = int(red_y)
                data[indx_right+1] = int(green_y)
                data[indx_right+2] = int(blue_y)
                data[indx_right+3] = int(alpha_y)
            red_y = adj_value(red_y, delta_right_color[0])
            green_y = adj_value(green_y, delta_right_color[1])
            blue_y = adj_value(blue_y, delta_right_color[2])
            alpha_y = adj_value(alpha_y, delta_right_color[3])

        img_data = ImageData(width, height, 'RGBA', bytes(data))
        return img_data


