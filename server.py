from flask import Flask, request, jsonify
from flask_cors import CORS
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# GPIO pins for servos
HORIZONTAL_SERVO_PIN = 17  # Left/Right servo
VERTICAL_SERVO_PIN = 27    # Up/Down servo

# Use pigpio factory for better servo control
factory = PiGPIOFactory()

# Initialize servos with custom pulse widths
horizontal_servo = Servo(HORIZONTAL_SERVO_PIN, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
vertical_servo = Servo(VERTICAL_SERVO_PIN, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

# Servo value range is -1 to 1, we'll use 0 (center) as starting position
STEP = 0.1  # Movement step size in servo value units

# Set initial positions (0 = center)
horizontal_servo.value = 0
vertical_servo.value = 0

@app.route('/button-press', methods=['POST'])
def button_press():
    data = request.get_json()
    direction = data.get('direction')
    
    print(f"Button pressed: {direction}")
    
    # Update servo positions based on direction
    # Servo values range from -1 (min) to 1 (max)
    if direction == 'left':
        horizontal_servo.value = max(-1, horizontal_servo.value - STEP)
    elif direction == 'right':
        horizontal_servo.value = min(1, horizontal_servo.value + STEP)
    elif direction == 'up':
        vertical_servo.value = max(-1, vertical_servo.value - STEP)
    elif direction == 'down':
        vertical_servo.value = min(1, vertical_servo.value + STEP)
    
    return jsonify({
        'status': 'success',
        'direction': direction,
        'horizontal_position': horizontal_servo.value,
        'vertical_position': vertical_servo.value
    }), 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        # Cleanup on exit
        pi.set_servo_pulsewidth(HORIZONTAL_SERVO_PIN, 0)
        pi.set_servo_pulsewidth(VERTICAL_SERVO_PIN, 0)
        pi.stop()
horizontal_servo.close()
vertical_servo.close()