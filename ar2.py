from pyfirmata import Arduino, SERVO, util
from time import sleep

port = 'COM9'
pin = 3
pin1 = 4
pin2 = 5
board = Arduino(port)
if board:
    print("Successfully connected to Arduino")

# Set the mode of the pin to SERVO
board.digital[pin].mode = SERVO
board.digital[pin1].mode = SERVO
board.digital[pin].write(90)
board.digital[pin1].write(90)
board.digital[pin2].write(90)

board.digital[pin].write(180)  # Rotate at full speed (change value based on your servo)
sleep(2.2)
board.digital[pin].write(90)   # Stop the servo
sleep(1)

board.digital[pin1].write(180)  # Rotate at full speed (change value based on your servo)
sleep(2.2)
board.digital[pin1].write(90)   # Stop the servo
sleep(1)

board.digital[pin2].write(180)  # Rotate at full speed (change value based on your servo)
sleep(2.2)
board.digital[pin2].write(90)   # Stop the servo
sleep(2)

board.exit()  # Close the connection when done
