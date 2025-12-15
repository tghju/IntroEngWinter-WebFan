<!-- command: render -->

# Web-Controlled Fan with the Raspberry Pi Pico W

In this project, you will control a DC motor (a fan) using your **phone or laptop** instead of a potentiometer. The Raspberry Pi Pico W will:

- Create its own Wi-Fi network
- Act as a web server
- Send a webpage to your browser
- Receive commands from that webpage
- Use those commands to control a motor through an L293D motor driver

This README explains **how the code works**, line by line, and helps you understand how hardware, Python, and the web all connect.

You are **expected to read this carefully** before filling in the missing code sections.

---

## IMPORTANT: Personalize Your Network Name

Before running your code, **you must change the Wi-Fi network name (SSID)** so that it is unique to you.

Everyone in the room running a Pico W at the same time **cannot** use the same network name.  
If multiple devices broadcast `PICO-FAN`, phones will have trouble connecting to the correct one.

### What you should do

Find this line in the code:

```python
ap.config(essid="PICO-FAN", password="pico1234")
```

Change `"PICO-FAN"` to something that identifies **you**, for example:

- Your first name  
- Your initials  
- Your name plus a number  

Examples:
- `ALEX-FAN`
- `JAMIE-PICO`
- `SAM-FAN-3`

Do **not** change anything else on that line.

You will connect your phone to *your own* network during testing.

---

## Big Picture: What Is Happening?

1. The Pico W creates a Wi-Fi network with your personalized name
2. Your phone connects to that network
3. Your browser requests a webpage from the Pico
4. The Pico sends back an HTML page with buttons and a slider
5. When you interact with the page, the browser sends requests back to the Pico
6. The Pico reads those requests and controls the motor

This is exactly how the internet works — just on a very small scale.

---

## Imports: Tools We Need

```python
import network
import socket
from machine import Pin, PWM
```

- `network` lets the Pico create a Wi-Fi access point
- `socket` allows the Pico to send and receive data using HTTP
- `Pin` controls GPIO pins
- `PWM` allows us to send pulse-width-modulated signals to control motor speed

---

## Motor Setup

```python
en_pwm = PWM(Pin(13)) 
en_pwm.freq(1000)
en_pwm.duty_u16(0)

motor_in1 = Pin(14, Pin.OUT)
motor_in2 = Pin(15, Pin.OUT)
```

These pins connect to the **L293D motor driver**:

- `motor_in1` and `motor_in2` control direction
- `en_pwm` controls speed using PWM
- The PWM frequency is set to 1000 Hz (1 kHz)
- The motor starts off (duty cycle = 0)

---

## Helper Functions (YOU WRITE PARTS OF THESE)

These functions make the rest of the code easier to read and safer to use.

### `motor_off()`

```python
def motor_off():
    '''Set each motor pin to 0 and then set the duty cycle to the enable pin
    to zero.'''
    ### YOUR CODE HERE
```

This function should:
- Stop the motor
- Turn off the enable pin
- Leave the system in a safe state

You **must** write the code that does this.

---

### `motor_forward()`

```python
def motor_forward():
    '''Set each motor_in1 pin to 1, and motor_in2 to 0.
    '''
    ### YOUR CODE HERE
```

This function sets the motor direction.

You are responsible for:
- Choosing which pin is HIGH
- Choosing which pin is LOW

---

### `set_speed(percent)`

```python
def set_speed(percent):
    '''Set the en_pwm to the given percent of 65535.
    REMEMBER THAT percent in this case is a number between 0 and 100'''
    ### YOUR CODE HERE
```

PWM uses a number between **0 and 65535**.

This function must:
- Convert a percentage (0–100)
- Into a PWM duty cycle
- Then apply it to the enable pin

You must decide how to do that conversion.

---

## Creating a Wi-Fi Network

```python
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="YOUR-NAME-HERE", password="pico1234")
print("AP IP:", ap.ifconfig()[0])
```

This turns the Pico into a **Wi-Fi access point**.

- Your phone connects to *your personalized network name*
- The password is `pico1234`
- The Pico prints its IP address (usually `192.168.4.1`)

That IP address is what you type into your browser.

---

## The Webpage (HTML + JavaScript)

The Pico sends a webpage written in HTML.  
Your browser displays it and runs the JavaScript inside it.

HTML controls **what you see**.  
JavaScript controls **how the page talks back to the Pico**.

Values like `{state}` and `{speed}` are filled in by Python *before* the page is sent.

---

## JavaScript: Sending Speed Updates

```html
function sendSpeed(value) {
    fetch("/set?speed=" + value);
    document.getElementById("speedValue").innerText = value;
}
```

This code runs **on your phone**, not on the Pico.

When the slider moves:
- The browser sends a request like `/set?speed=42`
- The Pico receives it
- The motor speed updates immediately

---

## The HTTP Server

The Pico runs a very small web server.

```python
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
```

- Port 80 is the standard HTTP port
- The server waits for browser requests
- Only one request is handled at a time

---

## Handling Requests

```python
if "/?fan=on" in request:
```

This checks whether the browser clicked the **ON** button.

### YOU MUST WRITE THIS PART

In this block, you must:
1. Set the motor direction
2. Set the motor speed
3. Update the `state` variable to `"ON"`

Use the helper functions you wrote earlier.

---

## Final Thoughts

This project combines:
- Python
- Electronics
- Networking
- HTML
- JavaScript

That is **real embedded systems engineering**.

Take your time. Read carefully.  
If something breaks, trace the path of information:
Browser → Wi-Fi → Pico → Motor.

