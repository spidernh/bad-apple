from PIL import Image
import numpy as np

# frame = 1
# print(f'render-frames\\{frame:04}.png')
# 
# img = Image.open('frame-sequence/0310.png')
# print(type(img))
# # img.show()
# print(img.format)
# frame = np.asarray(img)
# print(type(frame))
# print(str(frame))

def change_color(color):
    print(f'Changing color to {"white" if color else "black"}')
    

color_is_black = True
new_color = 255
if (new_color < 128) != color_is_black:
    change_color(color_is_black)
    color_is_black = not color_is_black

# if new_color >= 128:
#         if color_is_black:
#             change_color(True)
#         color_is_black = False
# elif new_color < 128:
#     if not color_is_black:
#         change_color(False)
#     color_is_black = True

print(f'color: {"black" if color_is_black else "white"}')