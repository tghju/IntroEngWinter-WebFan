import network
import socket
from machine import Pin, PWM


# ---- Motor control pins ----
en_pwm = PWM(Pin(13)) 
en_pwm.freq(1000)
en_pwm.duty_u16(0)

motor_in1 = Pin(14, Pin.OUT)
motor_in2 = Pin(15, Pin.OUT)
#led = Pin(10, Pin.OUT)
led = PWM(Pin(10))
led.freq(1000)

def motor_off():
    '''Set each motor pin to 0 and then set the duty cycle to the enable pin
    to zero.'''
    ### YOUR CODE HERE
    motor_in1.value(0)
    motor_in2.value(0)
    en_pwm.duty_u16(0)
    #led.value(0)
    led.duty_u16(0)

def motor_forward():
    '''Set each motor_in1 pin to 1, and motor_in2 to 0.
    '''
    ### YOUR CODE HERE
    motor_in1.value(1)
    motor_in2.value(0)
    #led.value(1)
    
def set_speed(percent):
    '''Set the en_pwm to the given percent of 65535.
    REMEMBER THAT percent in this case is a number between 0 and 100'''
    ### YOUR CODE HERE
    en_pwm.duty_u16(int((percent*65535)/100))
    led.duty_u16(int(percent*65535/100))
    
# ---- Wi-Fi Access Point ----
ap = network.WLAN(network.AP_IF)
ap.config(essid="FANIX", password="pico1234")
ap.active(True)
print("AP IP:", ap.ifconfig()[0])

# ---- HTML page ----
def webpage(state, speed):
    return f"""
    <html>
    <head>
        <title>Pico Fan Control</title>
        <script>
            function sendSpeed(value) {{
                fetch("/set?speed=" + value);
                document.getElementById("speedValue").innerText = value;
            }}
        </script>
    </head>
    <body>
        <h1>Pico Fan Control</h1>

        <p>Fan is currently: <b>{state}</b></p>

        <a href="/?fan=on"><button>Turn ON</button></a>
        <a href="/?fan=off"><button>Turn OFF</button></a>

        <h3>Speed: <span id="speedValue">{speed}</span>%</h3>

        <input type="range" min="0" max="100" value="{speed}"
               oninput="sendSpeed(this.value)">
    </body>
    </html>
    """

# ---- HTTP Server ----
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Listening on", addr)

state = "OFF"
speed = 0
motor_off()


while True:
    cl, addr = s.accept()
    request = cl.recv(1024).decode()
    print(request)

    # ON/OFF logic
    if "/?fan=on" in request:
        ### Here you need to do 3 things. Use the helper functions
        ### defined above to set the motor forward, set the speed, and
        ### then set the state variable to "ON"
        
        ### YOUR CODE HERE
        
        motor_forward()
        set_speed(30)
        fan_state = "ON"
        
    elif "/?fan=off" in request:
        motor_off()
        speed = 0
        fan_state = "OFF"

    # Speed change (live)
    if "/set?speed=" in request:
        try:
            new_speed = int(request.split("speed=")[1].split()[0])
            new_speed = max(0, min(100, new_speed))
            speed = new_speed
            if speed > 0:
                motor_forward()
                state = "ON"
            set_speed(speed)
        except:
            pass

    # Send webpage back (unless AJAX call)
    if "GET /set?" not in request:
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.send(webpage(state, speed))

    cl.close()

