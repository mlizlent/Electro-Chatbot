"""
Circuit Animator - Generate animated SVG circuit diagrams
"""
import re
from typing import Optional, Dict, List, Tuple


class CircuitAnimator:
    """Generate animated SVG circuit diagrams with current flow visualization."""
    
    # Component SVG templates
    COMPONENTS = {
        'resistor': {
            'width': 60,
            'height': 20,
            'svg': '''<g>
                <rect x="-30" y="-10" width="60" height="20" fill="none" stroke="#4a9eff" stroke-width="2" rx="3"/>
                <path d="M-30,0 L-20,-8 L-10,8 L0,-8 L10,8 L20,-8 L30,0" stroke="#4a9eff" stroke-width="2" fill="none"/>
            </g>'''
        },
        'capacitor': {
            'width': 40,
            'height': 40,
            'svg': '''<g>
                <line x1="-20" y1="-15" x2="-20" y2="15" stroke="#4a9eff" stroke-width="3"/>
                <line x1="20" y1="-15" x2="20" y2="15" stroke="#4a9eff" stroke-width="3"/>
                <line x1="-20" y1="0" x2="-30" y2="0" stroke="#4a9eff" stroke-width="2"/>
                <line x1="20" y1="0" x2="30" y2="0" stroke="#4a9eff" stroke-width="2"/>
            </g>'''
        },
        'led': {
            'width': 40,
            'height': 40,
            'svg': '''<g>
                <circle cx="0" cy="0" r="15" fill="none" stroke="#4a9eff" stroke-width="2"/>
                <path d="M-8,-8 L8,8 M-8,8 L8,-8" stroke="#4a9eff" stroke-width="2"/>
                <path d="M10,-10 L15,-15 L12,-15 M10,-10 L10,-13" stroke="#ffaa00" stroke-width="1.5" fill="none"/>
                <path d="M15,-5 L20,-10 L17,-10 M15,-5 L15,-8" stroke="#ffaa00" stroke-width="1.5" fill="none"/>
            </g>'''
        },
        'battery': {
            'width': 40,
            'height': 50,
            'svg': '''<g>
                <line x1="-15" y1="-20" x2="-15" y2="20" stroke="#4a9eff" stroke-width="4"/>
                <line x1="15" y1="-10" x2="15" y2="10" stroke="#4a9eff" stroke-width="2"/>
                <text x="-25" y="5" font-size="14" fill="#4a9eff">+</text>
                <text x="20" y="5" font-size="14" fill="#4a9eff">-</text>
            </g>'''
        },
        'ic': {
            'width': 80,
            'height': 60,
            'svg': '''<g>
                <rect x="-40" y="-30" width="80" height="60" fill="#1a1a2e" stroke="#4a9eff" stroke-width="2" rx="5"/>
                <circle cx="-30" cy="-20" r="3" fill="#4a9eff"/>
                <text x="0" y="5" font-size="12" fill="#4a9eff" text-anchor="middle">IC</text>
            </g>'''
        },
        'ground': {
            'width': 30,
            'height': 30,
            'svg': '''<g>
                <line x1="0" y1="0" x2="0" y2="10" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-15" y1="10" x2="15" y2="10" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-10" y1="15" x2="10" y2="15" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-5" y1="20" x2="5" y2="20" stroke="#4a9eff" stroke-width="2"/>
            </g>'''
        },
        'switch': {
            'width': 50,
            'height': 20,
            'svg': '''<g>
                <circle cx="-20" cy="0" r="3" fill="#4a9eff"/>
                <circle cx="20" cy="0" r="3" fill="#4a9eff"/>
                <line x1="-17" y1="0" x2="10" y2="-10" stroke="#4a9eff" stroke-width="2"/>
            </g>'''
        }
    }
    
    def __init__(self):
        self.components: List[Dict] = []
        self.wires: List[Tuple] = []
        self.width = 800
        self.height = 600
        
    def detect_circuit_type(self, description: str) -> str:
        """Detect the type of circuit from description."""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['555', 'timer', 'astable', 'monostable', 'ne555']):
            return '555_timer'
        elif any(word in desc_lower for word in ['esp32', 'mqtt', 'iot', 'wifi', 'temperature sensor', 'dht', 'dht22', 'dht11']):
            return 'esp32_mqtt'
        elif any(word in desc_lower for word in ['arduino', 'uno', 'nano', 'mega', 'microcontroller']):
            return 'arduino_led'
        elif any(word in desc_lower for word in ['voltage regulator', '7805', 'lm317', 'lm7805']):
            return 'voltage_regulator'
        elif any(word in desc_lower for word in ['led', 'blink', 'flash', 'light emitting']):
            return 'led_circuit'
        elif any(word in desc_lower for word in ['transistor', 'bjt', 'npn', 'pnp', 'switch']):
            return 'transistor_switch'
        elif any(word in desc_lower for word in ['voltage divider', 'resistor divider']):
            return 'voltage_divider'
        else:
            return 'generic'
    
    def generate_555_timer(self) -> str:
        """Generate animated 555 timer circuit."""
        svg = f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <style>
                    @keyframes current-flow {{
                        0% {{ stroke-dashoffset: 1000; }}
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    .current-path {{
                        stroke: #00ff88;
                        stroke-width: 3;
                        stroke-dasharray: 10 5;
                        animation: current-flow 2s linear infinite;
                        opacity: 0.8;
                    }}
                </style>
            </defs>
            
            <!-- Background -->
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>
            
            <!-- Title -->
            <text x="400" y="30" font-size="20" fill="#4a9eff" text-anchor="middle" font-weight="bold">
                555 Timer Astable Circuit
            </text>
            
            <!-- VCC -->
            <g transform="translate(400, 80)">
                <line x1="0" y1="0" x2="0" y2="30" stroke="#ff4444" stroke-width="3"/>
                <text x="10" y="15" font-size="14" fill="#ff4444">VCC</text>
            </g>
            
            <!-- 555 IC -->
            <g transform="translate(400, 250)">
                <rect x="-60" y="-50" width="120" height="100" fill="#1a1a2e" stroke="#4a9eff" stroke-width="3" rx="8"/>
                <text x="0" y="-5" font-size="16" fill="#4a9eff" text-anchor="middle" font-weight="bold">555</text>
                <text x="0" y="15" font-size="12" fill="#4a9eff" text-anchor="middle">TIMER</text>
                
                <!-- Pins -->
                <circle cx="-60" cy="-30" r="4" fill="#4a9eff"/>
                <circle cx="-60" cy="0" r="4" fill="#4a9eff"/>
                <circle cx="-60" cy="30" r="4" fill="#4a9eff"/>
                <circle cx="60" cy="-30" r="4" fill="#4a9eff"/>
                <circle cx="60" cy="0" r="4" fill="#4a9eff"/>
                <circle cx="60" cy="30" r="4" fill="#4a9eff"/>
                
                <!-- Pin labels -->
                <text x="-70" y="-25" font-size="10" fill="#888" text-anchor="end">GND</text>
                <text x="-70" y="5" font-size="10" fill="#888" text-anchor="end">TRG</text>
                <text x="-70" y="35" font-size="10" fill="#888" text-anchor="end">OUT</text>
                <text x="70" y="-25" font-size="10" fill="#888">VCC</text>
                <text x="70" y="5" font-size="10" fill="#888">DIS</text>
                <text x="70" y="35" font-size="10" fill="#888">THR</text>
            </g>
            
            <!-- R1 (10kΩ) -->
            <g transform="translate(250, 150)">
                <rect x="-30" y="-10" width="60" height="20" fill="none" stroke="#4a9eff" stroke-width="2" rx="3"/>
                <path d="M-30,0 L-20,-6 L-10,6 L0,-6 L10,6 L20,-6 L30,0" stroke="#4a9eff" stroke-width="2" fill="none"/>
                <text x="0" y="-20" font-size="12" fill="#4a9eff" text-anchor="middle">R1</text>
                <text x="0" y="30" font-size="10" fill="#888" text-anchor="middle">10kΩ</text>
            </g>
            
            <!-- R2 (2kΩ) -->
            <g transform="translate(550, 150)">
                <rect x="-30" y="-10" width="60" height="20" fill="none" stroke="#4a9eff" stroke-width="2" rx="3"/>
                <path d="M-30,0 L-20,-6 L-10,6 L0,-6 L10,6 L20,-6 L30,0" stroke="#4a9eff" stroke-width="2" fill="none"/>
                <text x="0" y="-20" font-size="12" fill="#4a9eff" text-anchor="middle">R2</text>
                <text x="0" y="30" font-size="10" fill="#888" text-anchor="middle">2kΩ</text>
            </g>
            
            <!-- C1 (Timing Capacitor) -->
            <g transform="translate(550, 350)">
                <line x1="-20" y1="-15" x2="-20" y2="15" stroke="#4a9eff" stroke-width="3"/>
                <line x1="20" y1="-15" x2="20" y2="15" stroke="#4a9eff" stroke-width="3"/>
                <text x="0" y="-25" font-size="12" fill="#4a9eff" text-anchor="middle">C1</text>
                <text x="0" y="35" font-size="10" fill="#888" text-anchor="middle">0.01µF</text>
            </g>
            
            <!-- LED -->
            <g transform="translate(250, 400)">
                <circle cx="0" cy="0" r="20" fill="none" stroke="#4a9eff" stroke-width="2"/>
                <path d="M-10,-10 L10,10 M-10,10 L10,-10" stroke="#4a9eff" stroke-width="2"/>
                <circle cx="0" cy="0" r="20" fill="#ff4444" opacity="0.3">
                    <animate attributeName="opacity" values="0.3;0.9;0.3" dur="1s" repeatCount="indefinite"/>
                </circle>
                <text x="0" y="-35" font-size="12" fill="#4a9eff" text-anchor="middle">LED</text>
            </g>
            
            <!-- Ground -->
            <g transform="translate(400, 500)">
                <line x1="0" y1="0" x2="0" y2="15" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-20" y1="15" x2="20" y2="15" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-15" y1="20" x2="15" y2="20" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-10" y1="25" x2="10" y2="25" stroke="#4a9eff" stroke-width="2"/>
                <text x="0" y="45" font-size="12" fill="#888" text-anchor="middle">GND</text>
            </g>
            
            <!-- Wiring -->
            <path d="M400,110 L400,150 L250,150" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M250,150 L250,200 L340,200 L340,220" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M460,220 L550,220 L550,150" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M550,150 L550,110 L400,110" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M460,250 L550,250 L550,280" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M460,280 L550,280" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M550,380 L550,450 L400,450 L400,500" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M340,280 L250,280 L250,380" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M250,420 L250,450 L400,450" stroke="#4a9eff" stroke-width="2" fill="none"/>
            
            <!-- Animated current flow -->
            <path d="M400,110 L400,150 L250,150 L250,200 L340,200 L340,220" 
                  class="current-path" fill="none"/>
            <path d="M340,280 L250,280 L250,380 L250,420 L250,450 L400,450 L400,500" 
                  class="current-path" fill="none" style="animation-delay: 0.5s"/>
            
            <!-- Info text -->
            <text x="400" y="560" font-size="12" fill="#888" text-anchor="middle">
                Frequency ≈ 1.44 / ((R1 + 2×R2) × C1) ≈ 6 kHz
            </text>
        </svg>'''
        return svg
    
    def generate_led_circuit(self) -> str:
        """Generate simple LED circuit with animation."""
        svg = f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <style>
                    @keyframes current-flow {{
                        0% {{ stroke-dashoffset: 1000; }}
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    .current-path {{
                        stroke: #00ff88;
                        stroke-width: 3;
                        stroke-dasharray: 10 5;
                        animation: current-flow 1.5s linear infinite;
                        opacity: 0.8;
                    }}
                </style>
            </defs>
            
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>
            
            <text x="400" y="40" font-size="20" fill="#4a9eff" text-anchor="middle" font-weight="bold">
                LED Circuit with Current Limiting Resistor
            </text>
            
            <!-- Battery -->
            <g transform="translate(200, 300)">
                <line x1="-15" y1="-25" x2="-15" y2="25" stroke="#4a9eff" stroke-width="4"/>
                <line x1="15" y1="-15" x2="15" y2="15" stroke="#4a9eff" stroke-width="2"/>
                <text x="-35" y="5" font-size="16" fill="#ff4444">+</text>
                <text x="30" y="5" font-size="16" fill="#4a9eff">-</text>
                <text x="0" y="50" font-size="12" fill="#888" text-anchor="middle">9V</text>
            </g>
            
            <!-- Resistor -->
            <g transform="translate(400, 200)">
                <rect x="-40" y="-12" width="80" height="24" fill="none" stroke="#4a9eff" stroke-width="2" rx="4"/>
                <path d="M-40,0 L-25,-8 L-10,8 L5,-8 L20,8 L35,-8 L40,0" stroke="#4a9eff" stroke-width="2" fill="none"/>
                <text x="0" y="-25" font-size="14" fill="#4a9eff" text-anchor="middle">R1</text>
                <text x="0" y="35" font-size="12" fill="#888" text-anchor="middle">1kΩ</text>
            </g>
            
            <!-- LED -->
            <g transform="translate(600, 300)">
                <circle cx="0" cy="0" r="25" fill="none" stroke="#4a9eff" stroke-width="3"/>
                <path d="M-12,-12 L12,12 M-12,12 L12,-12" stroke="#4a9eff" stroke-width="3"/>
                <circle cx="0" cy="0" r="25" fill="#ff4444" opacity="0.3">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="0.8s" repeatCount="indefinite"/>
                </circle>
                <path d="M15,-15 L25,-25 L20,-25 M15,-15 L15,-20" stroke="#ffaa00" stroke-width="2" fill="none">
                    <animate attributeName="opacity" values="0.5;1;0.5" dur="0.8s" repeatCount="indefinite"/>
                </path>
                <path d="M20,-8 L30,-18 L25,-18 M20,-8 L20,-13" stroke="#ffaa00" stroke-width="2" fill="none">
                    <animate attributeName="opacity" values="0.5;1;0.5" dur="0.8s" repeatCount="indefinite"/>
                </path>
                <text x="0" y="-45" font-size="14" fill="#4a9eff" text-anchor="middle">LED</text>
                <text x="0" y="50" font-size="11" fill="#888" text-anchor="middle">Red 5mm</text>
            </g>
            
            <!-- Wiring -->
            <path d="M215,300 L360,300 L360,200" stroke="#4a9eff" stroke-width="3" fill="none"/>
            <path d="M440,200 L600,200 L600,275" stroke="#4a9eff" stroke-width="3" fill="none"/>
            <path d="M600,325 L600,400 L200,400 L200,325" stroke="#4a9eff" stroke-width="3" fill="none"/>
            
            <!-- Animated current -->
            <path d="M215,300 L360,300 L360,200 L440,200 L600,200 L600,275" 
                  class="current-path" fill="none"/>
            <path d="M600,325 L600,400 L200,400 L200,325" 
                  class="current-path" fill="none" style="animation-delay: 0.7s"/>
            
            <!-- Info -->
            <text x="400" y="500" font-size="13" fill="#888" text-anchor="middle">
                Current = (9V - 2V) / 1kΩ = 7mA (Safe for standard LED)
            </text>
            <text x="400" y="520" font-size="12" fill="#666" text-anchor="middle">
                Power dissipated in resistor = 7mA × 7V = 49mW
            </text>
        </svg>'''
        return svg
    
    def generate_generic_circuit(self, description: str) -> str:
        """Generate a generic circuit representation."""
        svg = f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>
            
            <text x="400" y="40" font-size="20" fill="#4a9eff" text-anchor="middle" font-weight="bold">
                Circuit Diagram
            </text>
            
            <text x="400" y="300" font-size="16" fill="#888" text-anchor="middle">
                {description[:60]}
            </text>
            
            <text x="400" y="350" font-size="13" fill="#666" text-anchor="middle">
                Detailed schematic generation coming soon...
            </text>
        </svg>'''
        return svg
    
    def generate(self, description: str) -> str:
        """Generate animated circuit based on description."""
        circuit_type = self.detect_circuit_type(description)
        
        if circuit_type == '555_timer':
            return self.generate_555_timer()
        elif circuit_type == 'led_circuit':
            return self.generate_led_circuit()
        elif circuit_type == 'arduino_led':
            return self.generate_arduino_led()
        elif circuit_type == 'voltage_regulator':
            return self.generate_voltage_regulator()
        elif circuit_type == 'transistor_switch':
            return self.generate_transistor_switch()
        elif circuit_type == 'voltage_divider':
            return self.generate_voltage_divider()
        elif circuit_type == 'esp32_mqtt':
            return self.generate_esp32_mqtt()
        else:
            return self.generate_generic_circuit(description)

    def generate_esp32_mqtt(self) -> str:
        """Generate animated ESP32 temperature sensor with MQTT circuit."""
        return f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <style>
                    @keyframes current-flow {{
                        0% {{ stroke-dashoffset: 800; }}
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    @keyframes data-pulse {{
                        0%,100% {{ opacity: 0.2; stroke-width: 2; }}
                        50% {{ opacity: 1; stroke-width: 4; }}
                    }}
                    @keyframes wifi-pulse {{
                        0%   {{ opacity: 0; r: 5; }}
                        50%  {{ opacity: 1; r: 18; }}
                        100% {{ opacity: 0; r: 30; }}
                    }}
                    @keyframes temp-read {{
                        0%,100% {{ fill: #4a9eff; }}
                        50%     {{ fill: #ff6644; }}
                    }}
                    .current-path {{ stroke: #00ff88; stroke-width: 2.5; stroke-dasharray: 8 4;
                        animation: current-flow 2s linear infinite; opacity: 0.8; fill: none; }}
                    .data-path {{ stroke: #ffaa00; stroke-width: 2; stroke-dasharray: 6 4;
                        animation: data-pulse 1.5s ease-in-out infinite; fill: none; }}
                    .wifi-ring {{ fill: none; stroke: #4a9eff; animation: wifi-pulse 2s ease-out infinite; }}
                    .temp-indicator {{ animation: temp-read 3s ease-in-out infinite; }}
                </style>
            </defs>
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>

            <!-- Title -->
            <text x="400" y="32" font-size="19" fill="#4a9eff" text-anchor="middle" font-weight="bold">ESP32 Temperature Sensor with MQTT</text>

            <!-- ESP32 board -->
            <g transform="translate(300, 290)">
                <rect x="-75" y="-90" width="150" height="180" fill="#1a2a1a" stroke="#00cc44" stroke-width="3" rx="8"/>
                <text x="0" y="-55" font-size="14" fill="#00ff44" text-anchor="middle" font-weight="bold">ESP32</text>
                <text x="0" y="-35" font-size="10" fill="#00aa44" text-anchor="middle">DevKit v1</text>
                <!-- WiFi antenna symbol -->
                <path d="M-15,-75 Q0,-85 15,-75" stroke="#4a9eff" stroke-width="2" fill="none"/>
                <path d="M-25,-75 Q0,-95 25,-75" stroke="#4a9eff" stroke-width="1.5" fill="none" opacity="0.6"/>
                <!-- Pins left -->
                <circle cx="-75" cy="-50" r="4" fill="#00ff44"/>
                <circle cx="-75" cy="-20" r="4" fill="#00ff44"/>
                <circle cx="-75" cy="10"  r="4" fill="#ff4444"/>
                <circle cx="-75" cy="40"  r="4" fill="#888"/>
                <circle cx="-75" cy="70"  r="4" fill="#888"/>
                <!-- Pins right -->
                <circle cx="75" cy="-50" r="4" fill="#ffaa00"/>
                <circle cx="75" cy="-20" r="4" fill="#ffaa00"/>
                <circle cx="75" cy="10"  r="4" fill="#888"/>
                <!-- Pin labels left -->
                <text x="-88" y="-45" font-size="8" fill="#00ff44" text-anchor="end">3.3V</text>
                <text x="-88" y="-15" font-size="8" fill="#00ff44" text-anchor="end">GND</text>
                <text x="-88" y="15"  font-size="8" fill="#ff4444" text-anchor="end">GPIO4</text>
                <!-- Pin labels right -->
                <text x="88" y="-45" font-size="8" fill="#ffaa00">GPIO21</text>
                <text x="88" y="-15" font-size="8" fill="#ffaa00">GPIO22</text>
                <!-- USB -->
                <rect x="-20" y="78" width="40" height="14" fill="#333" stroke="#555" rx="2"/>
                <text x="0" y="89" font-size="7" fill="#888" text-anchor="middle">USB</text>
            </g>

            <!-- DHT22 Sensor -->
            <g transform="translate(560, 200)">
                <rect x="-35" y="-55" width="70" height="110" fill="#1a1a2e" stroke="#4a9eff" stroke-width="2.5" rx="6"/>
                <text x="0" y="-25" font-size="12" fill="#4a9eff" text-anchor="middle" font-weight="bold">DHT22</text>
                <text x="0" y="-8"  font-size="9"  fill="#888"   text-anchor="middle">Temp/Humidity</text>
                <!-- Sensor reading animation -->
                <rect x="-20" y="5" width="40" height="18" fill="#0d1a2e" rx="3"/>
                <text x="0" y="18" font-size="9" text-anchor="middle" class="temp-indicator">25.4°C</text>
                <!-- Pins -->
                <circle cx="-35" cy="35" r="4" fill="#ff4444"/>
                <circle cx="-12" cy="55" r="4" fill="#4a9eff"/>
                <circle cx="12"  cy="55" r="4" fill="#888"/>
                <circle cx="35"  cy="35" r="4" fill="#888"/>
                <text x="-35" y="50"  font-size="7" fill="#ff4444" text-anchor="middle">VCC</text>
                <text x="-12" y="70"  font-size="7" fill="#4a9eff" text-anchor="middle">DATA</text>
                <text x="12"  cy="70" font-size="7" fill="#888"    text-anchor="middle">NC</text>
                <text x="35"  y="50"  font-size="7" fill="#888"    text-anchor="middle">GND</text>
            </g>

            <!-- Pull-up resistor -->
            <g transform="translate(480, 155)">
                <rect x="-25" y="-10" width="50" height="20" fill="none" stroke="#4a9eff" stroke-width="2" rx="3"/>
                <path d="M-25,0 L-16,-6 L-7,6 L2,-6 L11,6 L20,-6 L25,0" stroke="#4a9eff" stroke-width="1.5" fill="none"/>
                <text x="0" y="-18" font-size="10" fill="#4a9eff" text-anchor="middle">R1</text>
                <text x="0" y="28"  font-size="9"  fill="#888"   text-anchor="middle">10kΩ</text>
            </g>

            <!-- MQTT Broker (cloud) -->
            <g transform="translate(660, 290)">
                <ellipse cx="0" cy="-10" rx="55" ry="30" fill="#0d1a2e" stroke="#4a9eff" stroke-width="2"/>
                <ellipse cx="-25" cy="5" rx="35" ry="22" fill="#0d1a2e" stroke="#4a9eff" stroke-width="2"/>
                <ellipse cx="25"  cy="5" rx="35" ry="22" fill="#0d1a2e" stroke="#4a9eff" stroke-width="2"/>
                <rect x="-55" y="5" width="110" height="25" fill="#0d1a2e"/>
                <text x="0" y="-5"  font-size="11" fill="#4a9eff" text-anchor="middle" font-weight="bold">MQTT</text>
                <text x="0" y="12"  font-size="10" fill="#4a9eff" text-anchor="middle">Broker</text>
                <text x="0" y="28"  font-size="8"  fill="#888"   text-anchor="middle">broker.hivemq.com</text>
                <!-- WiFi rings -->
                <circle cx="0" cy="-30" r="8"  class="wifi-ring" style="animation-delay:0s"/>
                <circle cx="0" cy="-30" r="8"  class="wifi-ring" style="animation-delay:0.7s"/>
                <circle cx="0" cy="-30" r="8"  class="wifi-ring" style="animation-delay:1.4s"/>
            </g>

            <!-- Power supply -->
            <g transform="translate(120, 290)">
                <rect x="-30" y="-40" width="60" height="80" fill="#1a1a2e" stroke="#ff4444" stroke-width="2" rx="5"/>
                <text x="0" y="-15" font-size="11" fill="#ff4444" text-anchor="middle">3.3V</text>
                <text x="0" y="5"   font-size="10" fill="#ff4444" text-anchor="middle">PSU</text>
                <text x="0" y="22"  font-size="9"  fill="#888"   text-anchor="middle">500mA</text>
                <circle cx="30" cy="-10" r="4" fill="#ff4444"/>
                <circle cx="30" cy="10"  r="4" fill="#888"/>
            </g>

            <!-- Ground rail -->
            <line x1="80" y1="450" x2="720" y2="450" stroke="#4a9eff" stroke-width="1.5" stroke-dasharray="5 3" opacity="0.5"/>
            <text x="400" y="468" font-size="10" fill="#555" text-anchor="middle">GND Rail</text>

            <!-- Power wires -->
            <path d="M150,280 L225,280" stroke="#ff4444" stroke-width="2.5" fill="none"/>
            <path d="M150,300 L150,450" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <!-- ESP32 to DHT22 data wire -->
            <path d="M375,240 L455,240 L455,200 L525,200" stroke="#ffaa00" stroke-width="2" fill="none"/>
            <!-- Pull-up to 3.3V -->
            <path d="M480,145 L480,120 L300,120 L300,200" stroke="#ff4444" stroke-width="1.5" fill="none" stroke-dasharray="4 2"/>
            <!-- DHT22 GND -->
            <path d="M560,255 L560,450" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <!-- ESP32 GND -->
            <path d="M225,270 L225,450" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <!-- WiFi data to MQTT -->
            <path d="M375,290 L605,290" stroke="#4a9eff" stroke-width="1.5" stroke-dasharray="4 2" fill="none"/>

            <!-- Animated current flow -->
            <path d="M150,280 L225,280 L225,240 L225,200" class="current-path"/>
            <path d="M375,240 L455,240 L455,200 L525,200" class="data-path"/>
            <path d="M375,290 L605,290" class="data-path" style="animation-delay:0.8s"/>

            <!-- Topic label -->
            <rect x="370" y="305" width="160" height="22" fill="#0d1a2e" rx="4" opacity="0.8"/>
            <text x="450" y="320" font-size="9" fill="#ffaa00" text-anchor="middle">Topic: home/sensor/temperature</text>

            <!-- Info bar -->
            <rect x="50" y="490" width="700" height="40" fill="#0d1117" rx="6"/>
            <text x="400" y="507" font-size="11" fill="#888" text-anchor="middle">GPIO4 → DHT22 DATA (10kΩ pull-up to 3.3V)  |  Publishes every 5s via WiFi</text>
            <text x="400" y="523" font-size="10" fill="#555" text-anchor="middle">Libraries: DHT.h · PubSubClient.h · WiFi.h</text>
        </svg>'''

    def generate_generic_circuit(self, description: str) -> str:
        """Generate a generic circuit block diagram."""
        # Extract a short title from description
        words = description.strip().split()
        title = ' '.join(words[:6]) if words else 'Circuit Diagram'
        title = title[:50]

        return f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <style>
                    @keyframes current-flow {{
                        0% {{ stroke-dashoffset: 600; }}
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    .current-path {{ stroke: #00ff88; stroke-width: 2.5; stroke-dasharray: 8 4;
                        animation: current-flow 2s linear infinite; opacity: 0.8; fill: none; }}
                </style>
            </defs>
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>

            <text x="400" y="35" font-size="18" fill="#4a9eff" text-anchor="middle" font-weight="bold">{title}</text>

            <!-- Power supply block -->
            <g transform="translate(130, 280)">
                <rect x="-50" y="-40" width="100" height="80" fill="#1a1a2e" stroke="#ff4444" stroke-width="2" rx="6"/>
                <text x="0" y="-10" font-size="12" fill="#ff4444" text-anchor="middle">POWER</text>
                <text x="0" y="10"  font-size="11" fill="#ff4444" text-anchor="middle">SUPPLY</text>
                <text x="0" y="28"  font-size="10" fill="#888"   text-anchor="middle">VCC / GND</text>
                <circle cx="50" cy="-15" r="5" fill="#ff4444"/>
                <circle cx="50" cy="15"  r="5" fill="#4a9eff"/>
            </g>

            <!-- Main IC / Controller block -->
            <g transform="translate(350, 280)">
                <rect x="-70" y="-60" width="140" height="120" fill="#1a1a2e" stroke="#4a9eff" stroke-width="3" rx="8"/>
                <text x="0" y="-15" font-size="14" fill="#4a9eff" text-anchor="middle" font-weight="bold">MAIN IC</text>
                <text x="0" y="8"   font-size="11" fill="#4a9eff" text-anchor="middle">Controller</text>
                <text x="0" y="28"  font-size="10" fill="#888"   text-anchor="middle">Processing Unit</text>
                <circle cx="-70" cy="-30" r="5" fill="#ff4444"/>
                <circle cx="-70" cy="0"   r="5" fill="#4a9eff"/>
                <circle cx="-70" cy="30"  r="5" fill="#ffaa00"/>
                <circle cx="70"  cy="-30" r="5" fill="#00ff88"/>
                <circle cx="70"  cy="0"   r="5" fill="#00ff88"/>
                <circle cx="70"  cy="30"  r="5" fill="#888"/>
                <text x="-83" y="-25" font-size="8" fill="#ff4444" text-anchor="end">VCC</text>
                <text x="-83" y="5"   font-size="8" fill="#4a9eff" text-anchor="end">GND</text>
                <text x="-83" y="35"  font-size="8" fill="#ffaa00" text-anchor="end">IN</text>
                <text x="83"  y="-25" font-size="8" fill="#00ff88">OUT1</text>
                <text x="83"  y="5"   font-size="8" fill="#00ff88">OUT2</text>
            </g>

            <!-- Output block -->
            <g transform="translate(600, 280)">
                <rect x="-55" y="-45" width="110" height="90" fill="#1a1a2e" stroke="#00ff88" stroke-width="2" rx="6"/>
                <text x="0" y="-10" font-size="12" fill="#00ff88" text-anchor="middle">OUTPUT</text>
                <text x="0" y="10"  font-size="11" fill="#00ff88" text-anchor="middle">LOAD</text>
                <text x="0" y="28"  font-size="10" fill="#888"   text-anchor="middle">Device / Sensor</text>
                <circle cx="-55" cy="-15" r="5" fill="#00ff88"/>
                <circle cx="-55" cy="15"  r="5" fill="#4a9eff"/>
            </g>

            <!-- Wires -->
            <path d="M180,265 L280,265" stroke="#ff4444" stroke-width="2.5" fill="none"/>
            <path d="M180,295 L180,420 L350,420" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M420,250 L545,250" stroke="#00ff88" stroke-width="2.5" fill="none"/>
            <path d="M420,280 L545,280" stroke="#00ff88" stroke-width="2.5" fill="none"/>
            <path d="M545,265 L545,420 L350,420" stroke="#4a9eff" stroke-width="2" fill="none"/>

            <!-- Animated current -->
            <path d="M180,265 L280,265 L280,250 L280,280" class="current-path"/>
            <path d="M420,250 L545,250 L545,265" class="current-path" style="animation-delay:0.5s"/>
            <path d="M420,280 L545,280" class="current-path" style="animation-delay:1s"/>

            <!-- Info -->
            <text x="400" y="490" font-size="12" fill="#888" text-anchor="middle">
                Refer to the datasheet for exact pin connections and voltage levels
            </text>
            <text x="400" y="510" font-size="11" fill="#555" text-anchor="middle">
                Always add decoupling capacitors (100nF) near VCC pins
            </text>
        </svg>'''

    def generate_arduino_led(self) -> str:
        """Generate animated Arduino LED blink circuit."""
        return f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <style>
                    @keyframes current-flow {{
                        0% {{ stroke-dashoffset: 800; }}
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    @keyframes blink {{
                        0%, 49% {{ opacity: 1; }}
                        50%, 100% {{ opacity: 0.1; }}
                    }}
                    .current-path {{ stroke: #00ff88; stroke-width: 3; stroke-dasharray: 10 5;
                        animation: current-flow 1.5s linear infinite; opacity: 0.8; }}
                    .led-glow {{ animation: blink 1s step-end infinite; }}
                </style>
            </defs>
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>
            <text x="400" y="35" font-size="20" fill="#4a9eff" text-anchor="middle" font-weight="bold">Arduino LED Blink Circuit</text>

            <!-- Arduino board -->
            <g transform="translate(200, 280)">
                <rect x="-80" y="-100" width="160" height="200" fill="#1a3a1a" stroke="#00aa44" stroke-width="3" rx="8"/>
                <text x="0" y="-60" font-size="13" fill="#00ff44" text-anchor="middle" font-weight="bold">ARDUINO</text>
                <text x="0" y="-40" font-size="11" fill="#00cc44" text-anchor="middle">UNO</text>
                <!-- Pins -->
                <circle cx="80" cy="-60" r="5" fill="#00ff44"/>
                <circle cx="80" cy="-30" r="5" fill="#00ff44"/>
                <circle cx="80" cy="0"   r="5" fill="#00ff44"/>
                <circle cx="80" cy="30"  r="5" fill="#888"/>
                <circle cx="80" cy="60"  r="5" fill="#888"/>
                <text x="90" y="-55" font-size="9" fill="#00cc44">5V</text>
                <text x="90" y="-25" font-size="9" fill="#00cc44">GND</text>
                <text x="90" y="5"   font-size="9" fill="#00cc44">D13</text>
                <!-- USB port -->
                <rect x="-80" y="70" width="30" height="20" fill="#333" stroke="#555" stroke-width="1" rx="2"/>
                <text x="-65" y="84" font-size="8" fill="#888" text-anchor="middle">USB</text>
            </g>

            <!-- Resistor -->
            <g transform="translate(450, 200)">
                <rect x="-35" y="-12" width="70" height="24" fill="none" stroke="#4a9eff" stroke-width="2" rx="4"/>
                <path d="M-35,0 L-22,-8 L-9,8 L4,-8 L17,8 L30,-8 L35,0" stroke="#4a9eff" stroke-width="2" fill="none"/>
                <text x="0" y="-22" font-size="12" fill="#4a9eff" text-anchor="middle">R1</text>
                <text x="0" y="32" font-size="11" fill="#888" text-anchor="middle">220Ω</text>
            </g>

            <!-- LED -->
            <g transform="translate(600, 280)">
                <circle cx="0" cy="0" r="28" fill="none" stroke="#4a9eff" stroke-width="2.5"/>
                <path d="M-12,-12 L12,12 M-12,12 L12,-12" stroke="#4a9eff" stroke-width="2.5"/>
                <circle cx="0" cy="0" r="28" fill="#ff4444" class="led-glow"/>
                <!-- Light rays -->
                <g class="led-glow">
                    <line x1="20" y1="-20" x2="35" y2="-35" stroke="#ffaa00" stroke-width="2"/>
                    <line x1="28" y1="0"   x2="45" y2="0"   stroke="#ffaa00" stroke-width="2"/>
                    <line x1="20" y1="20"  x2="35" y2="35"  stroke="#ffaa00" stroke-width="2"/>
                </g>
                <text x="0" y="-48" font-size="13" fill="#4a9eff" text-anchor="middle">LED</text>
                <text x="0" y="52" font-size="11" fill="#888" text-anchor="middle">Red 5mm</text>
            </g>

            <!-- Ground symbol -->
            <g transform="translate(400, 480)">
                <line x1="0" y1="0" x2="0" y2="15" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-20" y1="15" x2="20" y2="15" stroke="#4a9eff" stroke-width="2.5"/>
                <line x1="-13" y1="21" x2="13" y2="21" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-6"  y1="27" x2="6"  y2="27" stroke="#4a9eff" stroke-width="2"/>
                <text x="0" y="45" font-size="11" fill="#888" text-anchor="middle">GND</text>
            </g>

            <!-- Wires -->
            <path d="M280,220 L450,220 L450,188" stroke="#4a9eff" stroke-width="2.5" fill="none"/>
            <path d="M485,200 L600,200 L600,252" stroke="#4a9eff" stroke-width="2.5" fill="none"/>
            <path d="M600,308 L600,400 L400,400 L400,480" stroke="#4a9eff" stroke-width="2.5" fill="none"/>
            <path d="M280,250 L320,250 L320,400 L400,400" stroke="#4a9eff" stroke-width="2.5" fill="none"/>

            <!-- Animated current -->
            <path d="M280,220 L450,220 L450,188 L485,200 L600,200 L600,252" class="current-path" fill="none"/>
            <path d="M600,308 L600,400 L400,400 L400,480" class="current-path" fill="none" style="animation-delay:0.6s"/>

            <!-- Info -->
            <text x="400" y="545" font-size="12" fill="#888" text-anchor="middle">Pin 13 → 220Ω → LED → GND  |  Blink: 1 second on / 1 second off</text>
        </svg>'''

    def generate_voltage_regulator(self) -> str:
        """Generate animated LM7805 voltage regulator circuit."""
        return f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <style>
                    @keyframes current-flow {{
                        0% {{ stroke-dashoffset: 800; }}
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    .current-path {{ stroke: #00ff88; stroke-width: 3; stroke-dasharray: 10 5;
                        animation: current-flow 2s linear infinite; opacity: 0.8; }}
                </style>
            </defs>
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>
            <text x="400" y="35" font-size="20" fill="#4a9eff" text-anchor="middle" font-weight="bold">LM7805 Voltage Regulator (12V → 5V)</text>

            <!-- Input battery -->
            <g transform="translate(120, 280)">
                <line x1="-15" y1="-30" x2="-15" y2="30" stroke="#4a9eff" stroke-width="5"/>
                <line x1="15"  y1="-18" x2="15"  y2="18" stroke="#4a9eff" stroke-width="2.5"/>
                <text x="-32" y="5" font-size="15" fill="#ff4444">+</text>
                <text x="25"  y="5" font-size="15" fill="#4a9eff">−</text>
                <text x="0" y="55" font-size="13" fill="#888" text-anchor="middle">12V IN</text>
            </g>

            <!-- C1 input capacitor -->
            <g transform="translate(240, 280)">
                <line x1="-3" y1="-25" x2="-3" y2="25" stroke="#4a9eff" stroke-width="4"/>
                <line x1="3"  y1="-25" x2="3"  y2="25" stroke="#4a9eff" stroke-width="2"/>
                <text x="0" y="-38" font-size="11" fill="#4a9eff" text-anchor="middle">C1</text>
                <text x="0" y="42"  font-size="10" fill="#888"   text-anchor="middle">0.33µF</text>
            </g>

            <!-- LM7805 IC -->
            <g transform="translate(400, 280)">
                <rect x="-45" y="-45" width="90" height="90" fill="#1a1a2e" stroke="#4a9eff" stroke-width="3" rx="6"/>
                <text x="0" y="-8"  font-size="14" fill="#4a9eff" text-anchor="middle" font-weight="bold">LM7805</text>
                <text x="0" y="12"  font-size="11" fill="#4a9eff" text-anchor="middle">+5V REG</text>
                <circle cx="-45" cy="0" r="5" fill="#ff4444"/>
                <circle cx="45"  cy="0" r="5" fill="#00ff44"/>
                <circle cx="0"   cy="45" r="5" fill="#888"/>
                <text x="-58" y="5"  font-size="9" fill="#ff4444" text-anchor="end">IN</text>
                <text x="58"  y="5"  font-size="9" fill="#00ff44">OUT</text>
                <text x="0"   y="62" font-size="9" fill="#888" text-anchor="middle">GND</text>
            </g>

            <!-- C2 output capacitor -->
            <g transform="translate(560, 280)">
                <line x1="-3" y1="-25" x2="-3" y2="25" stroke="#4a9eff" stroke-width="4"/>
                <line x1="3"  y1="-25" x2="3"  y2="25" stroke="#4a9eff" stroke-width="2"/>
                <text x="0" y="-38" font-size="11" fill="#4a9eff" text-anchor="middle">C2</text>
                <text x="0" y="42"  font-size="10" fill="#888"   text-anchor="middle">0.1µF</text>
            </g>

            <!-- Output load -->
            <g transform="translate(680, 280)">
                <rect x="-25" y="-35" width="50" height="70" fill="none" stroke="#00ff44" stroke-width="2" rx="4"/>
                <text x="0" y="-45" font-size="11" fill="#00ff44" text-anchor="middle">LOAD</text>
                <text x="0" y="5"   font-size="12" fill="#00ff44" text-anchor="middle">5V</text>
            </g>

            <!-- Ground rail -->
            <line x1="100" y1="420" x2="720" y2="420" stroke="#4a9eff" stroke-width="2" stroke-dasharray="6 3"/>
            <text x="400" y="445" font-size="11" fill="#888" text-anchor="middle">GND Rail</text>

            <!-- Wires -->
            <path d="M135,280 L240,280" stroke="#ff4444" stroke-width="2.5" fill="none"/>
            <path d="M243,280 L355,280" stroke="#ff4444" stroke-width="2.5" fill="none"/>
            <path d="M445,280 L557,280" stroke="#00ff44" stroke-width="2.5" fill="none"/>
            <path d="M563,280 L655,280" stroke="#00ff44" stroke-width="2.5" fill="none"/>
            <path d="M120,310 L120,420" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M240,305 L240,420" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M400,325 L400,420" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M560,305 L560,420" stroke="#4a9eff" stroke-width="2" fill="none"/>
            <path d="M680,315 L680,420" stroke="#4a9eff" stroke-width="2" fill="none"/>

            <!-- Animated current -->
            <path d="M135,280 L240,280 L243,280 L355,280" class="current-path" fill="none"/>
            <path d="M445,280 L557,280 L563,280 L655,280" class="current-path" fill="none" style="animation-delay:0.5s"/>

            <!-- Info -->
            <text x="400" y="490" font-size="12" fill="#888" text-anchor="middle">Input: 7–35V  |  Output: 5V regulated  |  Max current: 1A</text>
            <text x="400" y="510" font-size="11" fill="#666" text-anchor="middle">Add heatsink if input voltage is high or current &gt; 500mA</text>
        </svg>'''

    def generate_transistor_switch(self) -> str:
        """Generate animated NPN transistor switch circuit."""
        return f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <style>
                    @keyframes current-flow {{
                        0% {{ stroke-dashoffset: 800; }}
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    .current-path {{ stroke: #00ff88; stroke-width: 3; stroke-dasharray: 10 5;
                        animation: current-flow 1.8s linear infinite; opacity: 0.8; }}
                    .led-on {{ animation: led-pulse 1.8s ease-in-out infinite; }}
                    @keyframes led-pulse {{ 0%,100% {{ opacity:0.4; }} 50% {{ opacity:1; }} }}
                </style>
            </defs>
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>
            <text x="400" y="35" font-size="20" fill="#4a9eff" text-anchor="middle" font-weight="bold">NPN Transistor Switch Circuit</text>

            <!-- VCC -->
            <g transform="translate(400, 80)">
                <line x1="0" y1="0" x2="0" y2="25" stroke="#ff4444" stroke-width="3"/>
                <text x="15" y="18" font-size="13" fill="#ff4444">VCC (5V)</text>
            </g>

            <!-- Collector resistor -->
            <g transform="translate(400, 160)">
                <rect x="-30" y="-12" width="60" height="24" fill="none" stroke="#4a9eff" stroke-width="2" rx="4"/>
                <path d="M-30,0 L-20,-7 L-8,7 L4,-7 L16,7 L28,-7 L30,0" stroke="#4a9eff" stroke-width="2" fill="none"/>
                <text x="45" y="5" font-size="11" fill="#4a9eff">RC</text>
                <text x="45" y="18" font-size="10" fill="#888">1kΩ</text>
            </g>

            <!-- LED (load) -->
            <g transform="translate(400, 250)">
                <circle cx="0" cy="0" r="22" fill="none" stroke="#4a9eff" stroke-width="2.5"/>
                <path d="M-10,-10 L10,10 M-10,10 L10,-10" stroke="#4a9eff" stroke-width="2.5"/>
                <circle cx="0" cy="0" r="22" fill="#ff4444" class="led-on"/>
                <text x="35" y="5" font-size="11" fill="#4a9eff">LED</text>
            </g>

            <!-- NPN Transistor (2N2222) -->
            <g transform="translate(400, 360)">
                <circle cx="0" cy="0" r="35" fill="#1a1a2e" stroke="#4a9eff" stroke-width="2.5"/>
                <text x="0" y="-5"  font-size="12" fill="#4a9eff" text-anchor="middle" font-weight="bold">2N2222</text>
                <text x="0" y="12"  font-size="10" fill="#888"   text-anchor="middle">NPN</text>
                <!-- C, B, E pins -->
                <circle cx="0"   cy="-35" r="4" fill="#4a9eff"/>
                <circle cx="-35" cy="0"   r="4" fill="#ffaa00"/>
                <circle cx="0"   cy="35"  r="4" fill="#4a9eff"/>
                <text x="0"   y="-45" font-size="9" fill="#4a9eff" text-anchor="middle">C</text>
                <text x="-48" y="5"   font-size="9" fill="#ffaa00">B</text>
                <text x="0"   y="52"  font-size="9" fill="#4a9eff" text-anchor="middle">E</text>
            </g>

            <!-- Base resistor -->
            <g transform="translate(230, 360)">
                <rect x="-30" y="-12" width="60" height="24" fill="none" stroke="#ffaa00" stroke-width="2" rx="4"/>
                <path d="M-30,0 L-20,-7 L-8,7 L4,-7 L16,7 L28,-7 L30,0" stroke="#ffaa00" stroke-width="2" fill="none"/>
                <text x="0" y="-22" font-size="11" fill="#ffaa00" text-anchor="middle">RB</text>
                <text x="0" y="32"  font-size="10" fill="#888"   text-anchor="middle">10kΩ</text>
            </g>

            <!-- Input signal -->
            <g transform="translate(120, 360)">
                <rect x="-30" y="-25" width="60" height="50" fill="#1a1a2e" stroke="#ffaa00" stroke-width="2" rx="5"/>
                <text x="0" y="-5"  font-size="10" fill="#ffaa00" text-anchor="middle">INPUT</text>
                <text x="0" y="12"  font-size="11" fill="#ffaa00" text-anchor="middle">3.3V</text>
            </g>

            <!-- Ground -->
            <g transform="translate(400, 480)">
                <line x1="0" y1="0" x2="0" y2="12" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-18" y1="12" x2="18" y2="12" stroke="#4a9eff" stroke-width="2.5"/>
                <line x1="-12" y1="18" x2="12" y2="18" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-6"  y1="24" x2="6"  y2="24" stroke="#4a9eff" stroke-width="2"/>
                <text x="0" y="40" font-size="11" fill="#888" text-anchor="middle">GND</text>
            </g>

            <!-- Wires -->
            <path d="M400,105 L400,148" stroke="#ff4444" stroke-width="2.5" fill="none"/>
            <path d="M400,172 L400,228" stroke="#4a9eff" stroke-width="2.5" fill="none"/>
            <path d="M400,272 L400,325" stroke="#4a9eff" stroke-width="2.5" fill="none"/>
            <path d="M400,395 L400,480" stroke="#4a9eff" stroke-width="2.5" fill="none"/>
            <path d="M150,360 L200,360" stroke="#ffaa00" stroke-width="2.5" fill="none"/>
            <path d="M260,360 L365,360" stroke="#ffaa00" stroke-width="2.5" fill="none"/>

            <!-- Animated current -->
            <path d="M400,105 L400,148 L400,172 L400,228 L400,272 L400,325" class="current-path" fill="none"/>
            <path d="M150,360 L200,360 L260,360 L365,360" class="current-path" fill="none" style="animation-delay:0.4s"/>

            <!-- Info -->
            <text x="400" y="545" font-size="12" fill="#888" text-anchor="middle">Base current = (3.3V − 0.7V) / 10kΩ = 0.26mA  |  Collector current ≈ hFE × IB</text>
        </svg>'''

    def generate_voltage_divider(self) -> str:
        """Generate animated voltage divider circuit."""
        return f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <style>
                    @keyframes current-flow {{
                        0% {{ stroke-dashoffset: 600; }}
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    .current-path {{ stroke: #00ff88; stroke-width: 3; stroke-dasharray: 10 5;
                        animation: current-flow 2s linear infinite; opacity: 0.8; }}
                </style>
            </defs>
            <rect width="{self.width}" height="{self.height}" fill="#0a0a1a"/>
            <text x="400" y="35" font-size="20" fill="#4a9eff" text-anchor="middle" font-weight="bold">Voltage Divider Circuit</text>

            <!-- VCC -->
            <g transform="translate(400, 80)">
                <line x1="0" y1="0" x2="0" y2="30" stroke="#ff4444" stroke-width="3"/>
                <text x="15" y="20" font-size="13" fill="#ff4444">VIN (12V)</text>
            </g>

            <!-- R1 -->
            <g transform="translate(400, 180)">
                <rect x="-35" y="-15" width="70" height="30" fill="none" stroke="#4a9eff" stroke-width="2" rx="4"/>
                <path d="M-35,0 L-22,-9 L-9,9 L4,-9 L17,9 L30,-9 L35,0" stroke="#4a9eff" stroke-width="2" fill="none"/>
                <text x="55" y="0"  font-size="13" fill="#4a9eff">R1</text>
                <text x="55" y="16" font-size="11" fill="#888">10kΩ</text>
            </g>

            <!-- Midpoint / output -->
            <g transform="translate(400, 280)">
                <circle cx="0" cy="0" r="8" fill="#ffaa00" stroke="#ff8800" stroke-width="2"/>
                <text x="20" y="-15" font-size="13" fill="#ffaa00">VOUT</text>
                <text x="20" y="5"   font-size="12" fill="#ffaa00">= 6V</text>
                <!-- Output wire to right -->
                <line x1="8" y1="0" x2="100" y2="0" stroke="#ffaa00" stroke-width="2.5" stroke-dasharray="5 3"/>
                <text x="115" y="5" font-size="11" fill="#888">To ADC / Load</text>
            </g>

            <!-- R2 -->
            <g transform="translate(400, 380)">
                <rect x="-35" y="-15" width="70" height="30" fill="none" stroke="#4a9eff" stroke-width="2" rx="4"/>
                <path d="M-35,0 L-22,-9 L-9,9 L4,-9 L17,9 L30,-9 L35,0" stroke="#4a9eff" stroke-width="2" fill="none"/>
                <text x="55" y="0"  font-size="13" fill="#4a9eff">R2</text>
                <text x="55" y="16" font-size="11" fill="#888">10kΩ</text>
            </g>

            <!-- Ground -->
            <g transform="translate(400, 470)">
                <line x1="0" y1="0" x2="0" y2="15" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-20" y1="15" x2="20" y2="15" stroke="#4a9eff" stroke-width="2.5"/>
                <line x1="-13" y1="21" x2="13" y2="21" stroke="#4a9eff" stroke-width="2"/>
                <line x1="-6"  y1="27" x2="6"  y2="27" stroke="#4a9eff" stroke-width="2"/>
                <text x="0" y="45" font-size="11" fill="#888" text-anchor="middle">GND</text>
            </g>

            <!-- Wires -->
            <path d="M400,110 L400,165" stroke="#ff4444" stroke-width="2.5" fill="none"/>
            <path d="M400,195 L400,272" stroke="#4a9eff" stroke-width="2.5" fill="none"/>
            <path d="M400,288 L400,365" stroke="#4a9eff" stroke-width="2.5" fill="none"/>
            <path d="M400,395 L400,470" stroke="#4a9eff" stroke-width="2.5" fill="none"/>

            <!-- Animated current -->
            <path d="M400,110 L400,165 L400,195 L400,272 L400,288 L400,365 L400,395 L400,470" class="current-path" fill="none"/>

            <!-- Formula box -->
            <rect x="100" y="220" width="220" height="80" fill="#0d1a2e" stroke="#4a9eff" stroke-width="1.5" rx="8"/>
            <text x="210" y="245" font-size="13" fill="#4a9eff" text-anchor="middle" font-weight="bold">Formula</text>
            <text x="210" y="268" font-size="12" fill="#aaa"   text-anchor="middle">VOUT = VIN × R2/(R1+R2)</text>
            <text x="210" y="288" font-size="12" fill="#00ff88" text-anchor="middle">= 12 × 10k/(10k+10k) = 6V</text>

            <!-- Info -->
            <text x="400" y="545" font-size="12" fill="#888" text-anchor="middle">Equal resistors → output = half of input  |  Use for ADC input scaling</text>
        </svg>'''


def generate_animated_circuit(description: str) -> Optional[str]:
    """Generate an animated SVG circuit diagram."""
    try:
        animator = CircuitAnimator()
        svg = animator.generate(description)
        if svg:
            # Make SVG fully responsive: add viewBox and set width to 100%
            # so it scales to fit any container without clipping
            svg = svg.replace(
                f'width="{animator.width}" height="{animator.height}"',
                f'width="100%" height="auto" viewBox="0 0 {animator.width} {animator.height}" preserveAspectRatio="xMidYMid meet"'
            )
        return svg
    except Exception as e:
        print(f"Circuit animation error: {e}")
        return None
