import pyvisa
import statistics
import time

def reset5522a(fluke5522a):
    try:
        # Set a longer timeout (10 seconds) for Fluke 5522A
        fluke5522a.timeout = 10000
        # Reset the instrument
        fluke5522a.write('*RST')
        print('Fluke 5522A reset.')

    except Exception as e:
        print(f"Fluke 5522A Reset Error: {e}")

def setup5522a(fluke5522a):
    try:
        # Set resistance to 1 ohm and activate the output on Fluke 5522A
        # Enable 4-wire mode on Fluke 5522A
        fluke5522a.write("OUT 1Ohm")
        fluke5522a.write("ZCOMP WIRE4")
        
        print('Fluke 5522A setup.')

    except Exception as e:
        print(f"Fluke 5522A Setup Error: {e}")
        
def reset3458a(hp3458a):
    try:
        # Set Timeout - 10 seconds for HP 3458A
        hp3458a.timeout = 10000
        # Reset the instrument
        hp3458a.write('RESET')
        
        #hp3458a.write("DISP MSG,\"SquirrelsAreReal\"")
        #hp3458a.write("DISP ON")
        
        print('Keysight 3458A reset.')

    except Exception as e:
        print(f"Keysight 3458A Reset Error: {e}")
        
def setup3458a(hp3458a):
    try:
        # Set the HP 3458A for 4-wire resistance measurement with additional settings
        hp3458a.write("END ALWAYS")
        hp3458a.write("OHMF 10")  # Set range and 4-wire mode
        hp3458a.write("NRDGS 1,AUTO")
        hp3458a.write("NPLC 100")    # Set number of power line cycles
        hp3458a.write("OCOMP ON")    # Enable open circuit compensation
        hp3458a.write("TRIG AUTO")   # Set trigger to auto

        print('Keysight 3458A setup.')

    except Exception as e:
        print(f"Keysight 3458A Setup Error: {e}")

def send_command(inst, command):
    try:
        # Write the command to the instrument
        inst.write(command)
        # If the command is a query, read the response
        if '?' in command:
            response = inst.read()
            return response.strip()
        return None
    except pyvisa.errors.VisaIOError as e:
        print(f"VISA IO Error: {e}")
        return None
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

try:
    # Initialize the resource manager
    rm = pyvisa.ResourceManager()

    # Open the GPIB instrument at address 4 for Fluke 5522A
    fluke5522a = rm.open_resource('GPIB0::4::INSTR')
    # Open the GPIB instrument at address 22 for HP 3458A
    hp3458a = rm.open_resource("GPIB0::22::INSTR")

    # Perform reset and setup for Fluke 5522A and Keysight 3458A
    reset5522a(fluke5522a)
    reset3458a(hp3458a)  
    setup5522a(fluke5522a)
    setup3458a(hp3458a)
    
    # Prompt the user to hook up the wires for Fluke 5522A
    input('Please hook up the wires for Fluke 5522A and press Enter to continue...')
    
    # Perform the measurement 10 times and store results
    measurements = []
    
    #send_command(fluke5522a, 'OPER')
    fluke5522a.write("OPER")
    time.sleep(10)
    
    for i in range(10):
        hp3458a.write("TARM HOLD")
        hp3458a.write("TARM SGL")
        resistance = float(hp3458a.read())
        measurements.append(resistance)
        print(f'Meas {i+1}: Resistance from the Fluke 5522A: {resistance} Ohms')

    fluke5522a.write("STBY")
    
    # Calculate and print summary statistics
    average_resistance = statistics.mean(measurements)
    min_resistance = min(measurements)
    max_resistance = max(measurements)
    stddev_resistance = statistics.stdev(measurements)
    
    print('\nSummary Statistics:')
    print(f'Average Resistance: {average_resistance:.6f} Ohms')
    print(f'Minimum Resistance: {min_resistance:.6f} Ohms')
    print(f'Maximum Resistance: {max_resistance:.6f} Ohms')
    print(f'Standard Deviation: {stddev_resistance:.6f} Ohms')
    
    # Close Connections
    fluke5522a.close()
    hp3458a.close()
    print('Closed instrument connections')

except Exception as err:
    print('Exception: ' + str(err))

finally:
    # Perform clean up operations
    print('Complete')
