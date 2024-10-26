<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robot Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #2c3e50;
            color: #ecf0f1;
            text-align: center;
            margin: 0;
            padding: 0;
        }

        .container {
            display: inline-block;
            margin: 40px auto;
            padding: 20px;
            background-color: #34495e;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3);
            width: 350px;
        }

        .top-controls {
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .enable-switch label {
            font-size: 1.1rem;
            color: #16a085;
        }

        select {
            background-color: #16a085;
            color: #fff;
            padding: 6px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
        }

        #cameraButton {
            width: 100%;
            padding: 12px;
            background-color: #e74c3c;
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            margin-bottom: 20px;
            transition: background-color 0.3s;
        }

        #cameraButton:hover {
            background-color: #c0392b;
        }

        #cameraFeed {
            padding: 20px;
            background-color: #34495e;
            border: 2px solid #ecf0f1;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 1.2rem;
        }

        .control-panel {
            margin: 20px 0;
        }

        .control-row {
            display: flex;
            justify-content: space-around;
            margin-bottom: 10px;
        }

        .control-button {
            background-color: #3498db;
            border: none;
            border-radius: 50%;
            color: #fff;
            padding: 18px;
            font-size: 1.5rem;
            cursor: pointer;
            width: 60px;
            height: 60px;
            transition: background-color 0.3s;
        }

        .control-button:hover {
            background-color: #2980b9;
        }

        .sliders {
            margin-top: 20px;
        }

        .slider {
            margin: 15px 0;
        }

        .slider label {
            display: block;
            font-size: 1rem;
            margin-bottom: 5px;
        }

        .slider input {
            width: 100%;
        }

        .slider span {
            font-size: 1.2rem;
            color: #16a085;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="top-controls">
            <div class="enable-switch">
                <label>ENABLE:</label>
                <input type="checkbox" id="enable" onchange="toggleEnable()">
            </div>
            <select id="robotId">
                <option value="robot1">ID_Robot</option>
            </select>
        </div>
        
        <div class="control-panel">
            <div class="control-row">
                <button class="control-button" id="up" onclick="sendStraightSpeed('+')">↑</button>
            </div>
            <div class="control-row">
                <button class="control-button" id="left" onclick="sendRotationSpeed('+')">←</button>
                <button class="control-button" id="stop" onclick="sendCommand('STOP')">⦿</button>
                <button class="control-button" id="right" onclick="sendRotationSpeed('-')">→</button>
            </div>
            <div class="control-row">
                <button class="control-button" id="down" onclick="sendStraightSpeed('-')">↓</button>
            </div>
        </div>

        <div class="sliders">
            <div class="slider">
                <label>Straight speed: <span id="straightSpeed">0</span></label>
                <input type="range" min="0" max="100" value="0" id="straightSpeedSlider" oninput="updateStraightSpeed()">
            </div>
            <div class="slider">
                <label>Rotation speed: <span id="rotationSpeed">0</span></label>
                <input type="range" min="0" max="100" value="0" id="rotationSpeedSlider" oninput="updateRotationSpeed()">
            </div>
        </div>
    </div>

    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
    <script>
        const brokerUrl = 'wss://604b372efa0e444ebbe062ca5d3e2243.s1.eu.hivemq.cloud:8884/mqtt';
        const options = {
            username: 'truong',
            password: 'Lhh12345@@',
            clientId: 'web-client-' + Math.random().toString(16).substr(2, 8),
            protocolVersion: 4,
            clean: true,
        };

        const client = mqtt.connect(brokerUrl, options);

        client.on('connect', function () {
            console.log('Connected to MQTT Broker!');
        });

        client.on('error', function (err) {
            console.error('Connection error: ', err);
            client.end();
        });

        function sendCommand(command) {
            const topic = 'esp8266/client';
            client.publish(topic, command, { qos: 0, retain: false });
            console.log(`Command "${command}" sent`);
        }

        function updateStraightSpeed() {
            const speed = document.getElementById('straightSpeedSlider').value;
            document.getElementById('straightSpeed').innerText = speed;
        }

        function updateRotationSpeed() {
            const speed = document.getElementById('rotationSpeedSlider').value;
            document.getElementById('rotationSpeed').innerText = speed;
        }

        function sendStraightSpeed(direction) {
            const speed = document.getElementById('straightSpeedSlider').value;
            sendCommand(`${direction}STRAIGHT_SPEED:${speed}`);
            console.log(`${direction}STRAIGHT_SPEED:${speed} sent`);
        }

        function sendRotationSpeed(direction) {
            const speed = document.getElementById('rotationSpeedSlider').value;
            sendCommand(`${direction}ROTATION_SPEED:${speed}`);
            console.log(`${direction}ROTATION_SPEED:${speed} sent`);
        }

        function toggleEnable() {
            const isEnabled = document.getElementById('enable').checked;
            sendCommand(isEnabled ? 'ENABLE' : 'DISABLE');
        }
    </script>
</body>
</html>
