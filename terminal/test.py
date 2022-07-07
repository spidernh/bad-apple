import keyboard
import os

# for i in range(120, 122):
#     for i in range(29):
#         for k in range(119):
#             if k != 118:
#                 print('a', end='')
#             else:
#                 print('a', end='\n')
string = ''
for y in range(63):
    for x in range(235):
        string += 'a'
    string += '\n'
print(string)
# os.system('')
# print('\033[31mbanana\033[m\033[1Dapple')

while not keyboard.is_pressed('q'):
    pass