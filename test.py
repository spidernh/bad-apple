import keyboard

# for i in range(120, 122):
for i in range(29):
    for k in range(119):
        if k != 118:
            print('a', end='')
        else:
            print('a', end='\n')

while not keyboard.is_pressed('q'):
    pass