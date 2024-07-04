# Sending commands to CRYSTALFONTZ XES635BK-TML-KU
# by Luis La Rotta
# Based on the great C# code made by  Robert M. Meffe in February 2009

import serial
from datetime import datetime

#For CRC Calculation when sending text to the screen
crc_table = [ 0x00000, 0x01189, 0x02312, 0x0329B, 0x04624, 0x057AD, 0x06536, 0x074BF, 0x08C48, 0x09DC1, 0x0AF5A, 0x0BED3, 0x0CA6C, 0x0DBE5, 0x0E97E, 0x0F8F7, 0x01081, 0x00108, 0x03393, 0x0221A, 0x056A5, 0x0472C, 0x075B7, 0x0643E, 0x09CC9, 0x08D40, 0x0BFDB, 0x0AE52, 0x0DAED, 0x0CB64, 0x0F9FF, 0x0E876, 0x02102, 0x0308B, 0x00210, 0x01399, 0x06726, 0x076AF, 0x04434, 0x055BD, 0x0AD4A, 0x0BCC3, 0x08E58, 0x09FD1, 0x0EB6E, 0x0FAE7, 0x0C87C, 0x0D9F5, 0x03183, 0x0200A, 0x01291, 0x00318, 0x077A7, 0x0662E, 0x054B5, 0x0453C, 0x0BDCB, 0x0AC42, 0x09ED9, 0x08F50, 0x0FBEF, 0x0EA66, 0x0D8FD, 0x0C974, 0x04204, 0x0538D, 0x06116, 0x0709F, 0x00420, 0x015A9, 0x02732, 0x036BB, 0x0CE4C, 0x0DFC5, 0x0ED5E, 0x0FCD7, 0x08868, 0x099E1, 0x0AB7A, 0x0BAF3, 0x05285, 0x0430C, 0x07197, 0x0601E, 0x014A1, 0x00528, 0x037B3, 0x0263A, 0x0DECD, 0x0CF44, 0x0FDDF, 0x0EC56, 0x098E9, 0x08960, 0x0BBFB, 0x0AA72, 0x06306, 0x0728F, 0x04014, 0x0519D, 0x02522, 0x034AB, 0x00630, 0x017B9, 0x0EF4E, 0x0FEC7, 0x0CC5C, 0x0DDD5, 0x0A96A, 0x0B8E3, 0x08A78, 0x09BF1, 0x07387, 0x0620E, 0x05095, 0x0411C, 0x035A3, 0x0242A, 0x016B1, 0x00738, 0x0FFCF, 0x0EE46, 0x0DCDD, 0x0CD54, 0x0B9EB, 0x0A862, 0x09AF9, 0x08B70, 0x08408, 0x09581, 0x0A71A, 0x0B693, 0x0C22C, 0x0D3A5, 0x0E13E, 0x0F0B7, 0x00840, 0x019C9, 0x02B52, 0x03ADB, 0x04E64, 0x05FED, 0x06D76, 0x07CFF, 0x09489, 0x08500, 0x0B79B, 0x0A612, 0x0D2AD, 0x0C324, 0x0F1BF, 0x0E036, 0x018C1, 0x00948, 0x03BD3, 0x02A5A, 0x05EE5, 0x04F6C, 0x07DF7, 0x06C7E, 0x0A50A, 0x0B483, 0x08618, 0x09791, 0x0E32E, 0x0F2A7, 0x0C03C, 0x0D1B5, 0x02942, 0x038CB, 0x00A50, 0x01BD9, 0x06F66, 0x07EEF, 0x04C74, 0x05DFD, 0x0B58B, 0x0A402, 0x09699, 0x08710, 0x0F3AF, 0x0E226, 0x0D0BD, 0x0C134, 0x039C3, 0x0284A, 0x01AD1, 0x00B58, 0x07FE7, 0x06E6E, 0x05CF5, 0x04D7C, 0x0C60C, 0x0D785, 0x0E51E, 0x0F497, 0x08028, 0x091A1, 0x0A33A, 0x0B2B3, 0x04A44, 0x05BCD, 0x06956, 0x078DF, 0x00C60, 0x01DE9, 0x02F72, 0x03EFB, 0x0D68D, 0x0C704, 0x0F59F, 0x0E416, 0x090A9, 0x08120, 0x0B3BB, 0x0A232, 0x05AC5, 0x04B4C, 0x079D7, 0x0685E, 0x01CE1, 0x00D68, 0x03FF3, 0x02E7A, 0x0E70E, 0x0F687, 0x0C41C, 0x0D595, 0x0A12A, 0x0B0A3, 0x08238, 0x093B1, 0x06B46, 0x07ACF, 0x04854, 0x059DD, 0x02D62, 0x03CEB, 0x00E70, 0x01FF9, 0x0F78F, 0x0E606, 0x0D49D, 0x0C514, 0x0B1AB, 0x0A022, 0x092B9, 0x08330, 0x07BC7, 0x06A4E, 0x058D5, 0x0495C, 0x03DE3, 0x02C6A, 0x01EF1, 0x00F78 ]

#Serial port configuration
port='COM9'
baud_rate=115200
max_characters=20

_sp = serial.Serial(port, baud_rate)

#For pressed button decoding
last_serial_received_values = []    

#Required by the CRYSTALFONTZ XES635BK-TML-KU screen
class Commands:
    SEND_DATA_TO_LCD = 0x1F 

#Makes the python console look better
def print_with_timestamp(text):
     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
     print(f"{current_time}: {text}")

#Checks text length and pads it before sending to screen
def send_text_to_screen(line_number, text, xpos, padded):
        text_to_array = list(text)

        to_write = []

        count = 0
        while count < len(text_to_array):
            char = text_to_array[count]
            if char != '\\':
                to_write.append(ord(char))
            else:
                str_dec_value = ''.join(text_to_array[count + 1:count + 4])
                try:
                    int_dec_value = int(str_dec_value)
                    to_write.append(int_dec_value)
                    count += 3
                except ValueError:
                    to_write.append(ord(char))
            count += 1

        if len(to_write) > max_characters:
            raise IndexError("Too many characters passed in.")

        if line_number > 3 or line_number < 0:
            raise IndexError("Line Number out of range. Valid 0 - 3")

        if not _sp.is_open:
            raise ValueError("Serial Port is not open")

        if padded:
            pad_amount = max_characters - len(to_write)
            to_write.extend([32] * pad_amount)

        send_list = [xpos, line_number] + to_write

        send_command(Commands.SEND_DATA_TO_LCD, send_list)

#Sends the text to the screen
def send_command(command, data):
        send_list = [command, len(data)] + data

        calculate_crc(send_list)

        #To see the actual HEX values:
        #send_list_to_hex = "Sending HEX: " + ' '.join(format(x, '02X') for x in send_list)
        #print_with_timestamp(send_list_to_hex)  
        
        _sp.write(bytearray(send_list))

#For CRC Calculation when sending text to the screen
def calculate_crc(byte_list):
        work = 0xFFFF
        for byte in byte_list:
            work = (work >> 8) ^ crc_table[(work ^ byte) & 0xFF]
        work = ~work  # Invert bits
        byte_list.append(work & 0xFF)
        byte_list.append((work >> 8) & 0xFF)


def up_button_was_pressed():
    print_with_timestamp("Up button pressed")

def down_button_was_pressed():
    print_with_timestamp("Down button pressed")

def left_button_was_pressed():
    print_with_timestamp("Left button pressed")

def right_button_was_pressed():
    print_with_timestamp("Right button pressed")

def accept_button_was_pressed():
    print_with_timestamp("Accept button pressed")

def reject_button_was_pressed():
    print_with_timestamp("Reject button pressed")


# Check the conditions for button press based on the last two messages
def button_interpretation(hex_data):  
 
    #The two last values are stored for debouncing purposes

    if(last_serial_received_values.count) == 2:
         last_serial_received_values.clear

    last_serial_received_values.append(hex_data)

    last_message_index = len(last_serial_received_values) - 1

    if(last_message_index) < 2:
        return          
    
    #Screen button mapping
   
    if last_serial_received_values[last_message_index] == '80 01 07 47 A7' and \
        last_serial_received_values[last_message_index-1] == '80 01 01 71 C2':
            up_button_was_pressed()

    if last_serial_received_values[last_message_index] == '80 01 08 B0 5F' and \
        last_serial_received_values[last_message_index-1] == '80 01 02 EA F0':
            down_button_was_pressed()

    if last_serial_received_values[last_message_index] == '80 01 09 39 4E' and \
        last_serial_received_values[last_message_index-1] == '80 01 03 63 E1':
            left_button_was_pressed()

    if last_serial_received_values[last_message_index] == '80 01 0A A2 7C' and \
            last_serial_received_values[last_message_index-1] == '80 01 04 DC 95':
            right_button_was_pressed() 

    if last_serial_received_values[last_message_index] == '80 01 0B 2B 6D' and \
            last_serial_received_values[last_message_index-1] == '80 01 05 55 84':
             accept_button_was_pressed()             

    if last_serial_received_values[last_message_index] == '80 01 0C 94 19' and \
            last_serial_received_values[last_message_index-1] == '80 01 06 CE B6':
             reject_button_was_pressed()  

#Read incoming serial from screen, to decode which button is pressed
def read_incoming_serial():  

    while True:
        try:
            if _sp.in_waiting > 0:
                received_data = _sp.read(_sp.in_waiting)            
                hex_data = ' '.join(format(x, '02X') for x in received_data)    
                button_interpretation(hex_data)           

        except serial.SerialException as e:
            print_with_timestamp(f"Serial error occurred: {e}")
            break

        except KeyboardInterrupt:
            print_with_timestamp(f"Program interrupted. Exiting...")
            break  


# Main entry point

def main():
    try:

        print("Crystalfontz loaded OK")

        #send_text_to_screen(0, "Line 1", 0, True)
        #send_text_to_screen(1, "Line 2", 0, True)
        #send_text_to_screen(2, "Line 3", 0, True)
        #send_text_to_screen(3, "Line 4", 0, True)
    
        read_incoming_serial()

    except serial.SerialException as e:
        print_with_timestamp(f"Serial error occurred: {e}")

    finally:
        if _sp.is_open:
            _sp.close()

main()