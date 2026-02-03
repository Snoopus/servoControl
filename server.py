from flask import Flask, request, jsonify
from flask_cors import CORS
import pigpio

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# GPIO pins for servos
HORIZONTAL_SERVO_PIN = 17  # Left/Right servo
VERTICAL_SERVO_PIN = 27    # Up/Down servo

# Servo position limits (in microseconds for pigpio)
MIN_PULSE = 500   # Minimum pulse width
MAX_PULSE = 2500  # Maximum pulse width
STEP = 100        # Movement step size

# Initialize pigpio
pi = pigpio.pi()

# Current servo positions (start at center)
horizontal_position = 1500
vertical_position = 1500

# Set initial positions
pi.set_servo_pulsewidth(HORIZONTAL_SERVO_PIN, horizontal_position)
pi.set_servo_pulsewidth(VERTICAL_SERVO_PIN, vertical_position)

@app.route('/button-press', methods=['POST'])
def button_press():
    global horizontal_position, vertical_position
    
    data = request.get_json()
    direction = data.get('direction')
    
    print(f"Button pressed: {direction}")
    
    # Update servo positions based on direction
    if direction == 'left':
        horizontal_position = max(MIN_PULSE, horizontal_position - STEP)
        pi.set_servo_pulsewidth(HORIZONTAL_SERVO_PIN, horizontal_position)
    elif direction == 'right':
        horizontal_position = min(MAX_PULSE, horizontal_position + STEP)
        pi.set_servo_pulsewidth(HORIZONTAL_SERVO_PIN, horizontal_position)
    elif direction == 'up':
        vertical_position = max(MIN_PULSE, vertical_position - STEP)
        pi.set_servo_pulsewidth(VERTICAL_SERVO_PIN, vertical_position)
    elif direction == 'down':
        vertical_position = min(MAX_PULSE, vertical_position + STEP)
        pi.set_servo_pulsewidth(VERTICAL_SERVO_PIN, vertical_position)
    
    return jsonify({
        'status': 'success',
        'direction': direction,
        'horizontal_position': horizontal_position,
        'vertical_position': vertical_position
    }), 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        # Cleanup on exit
        pi.set_servo_pulsewidth(HORIZONTAL_SERVO_PIN, 0)
        pi.set_servo_pulsewidth(VERTICAL_SERVO_PIN, 0)
        pi.stop()
