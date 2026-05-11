# Electronics Components Database Implementation

## Overview
A comprehensive database of electronic components has been added to ElectroBot, including microcontrollers, microprocessors, passive components, ICs, sensors, and more.

## Database Schema

```python
class Component(Base):
    id          = Integer (Primary Key)
    name        = String(200)      # Component name
    part_number = String(100)      # Manufacturer part number
    category    = String(100)      # Main category
    subcategory = String(100)      # Sub-category
    description = Text             # Detailed description
    specs       = JSON             # Technical specifications
    package     = String(100)      # Package type (DIP, SMD, etc.)
    voltage     = String(100)      # Operating voltage
    current     = String(100)      # Current rating
    datasheet   = String(500)      # Datasheet URL
    tags        = String(500)      # Searchable tags
```

## Component Categories

### 1. Microcontrollers (MCU)
- **Arduino Family**: Uno, Nano, Mega, Due, MKR
- **ESP Family**: ESP8266, ESP32, ESP32-S2, ESP32-C3
- **STM32**: STM32F103, STM32F4, STM32L4
- **PIC**: PIC16F, PIC18F, PIC32
- **AVR**: ATmega328P, ATmega2560, ATtiny85
- **ARM Cortex-M**: Various STM32, NXP, Nordic

### 2. Microprocessors (MPU)
- **Raspberry Pi**: Pi 4, Pi Zero, Pi Pico
- **BeagleBone**: Black, AI
- **Intel**: Atom, Core series
- **ARM**: Cortex-A series

### 3. Passive Components

#### Resistors
- Carbon Film: 1Ω - 10MΩ
- Metal Film: High precision
- Power Resistors: 1W, 2W, 5W, 10W
- Variable: Potentiometers, Trimmers
- Special: Thermistors (NTC, PTC), LDR

#### Capacitors
- Ceramic: 1pF - 10µF
- Electrolytic: 1µF - 10000µF
- Tantalum: High stability
- Film: Polyester, Polypropylene
- Supercapacitors: 0.1F - 100F

#### Inductors
- Power Inductors: 1µH - 1mH
- RF Inductors: nH range
- Transformers: Step-up, Step-down

### 4. Semiconductors

#### Diodes
- Rectifier: 1N4001-1N4007
- Zener: 3.3V, 5V, 12V, 15V
- Schottky: Fast switching
- LED: Red, Green, Blue, White, RGB
- Special: TVS, Varactor

#### Transistors
- **BJT NPN**: 2N2222, 2N3904, BC547
- **BJT PNP**: 2N2907, 2N3906, BC557
- **MOSFET N-Channel**: IRF540, 2N7000, BS170
- **MOSFET P-Channel**: IRF9540, BS250
- **JFET**: 2N5457, J201

### 5. Integrated Circuits

#### Voltage Regulators
- Linear: LM7805, LM7812, LM317, LM1117
- Switching: LM2596, LM2577, MP1584

#### Op-Amps
- General: LM358, LM324, TL071, TL072
- Precision: OP07, OP27, AD620
- High-Speed: LM6171, OPA657

#### Timers & Oscillators
- 555 Timer: NE555, LM555, TLC555
- Crystal Oscillators: Various frequencies

#### Logic ICs
- 74HC series: 74HC00, 74HC04, 74HC595
- 74LS series: Legacy TTL
- CD4000 series: CMOS logic

#### Motor Drivers
- H-Bridge: L293D, L298N, DRV8833
- Stepper: A4988, DRV8825, TMC2208

#### Communication ICs
- UART: MAX232, FT232
- I2C: PCF8574, MCP23017
- SPI: MCP3008, 74HC595
- CAN: MCP2515, TJA1050

### 6. Sensors

#### Temperature
- Analog: LM35, TMP36, LM75
- Digital: DS18B20, DHT11, DHT22, BME280
- Thermocouple: MAX6675, MAX31855

#### Humidity
- DHT11, DHT22, SHT31, BME280

#### Pressure
- BMP180, BMP280, BME280, MPX5700

#### Motion & Position
- Accelerometer: ADXL345, MPU6050
- Gyroscope: MPU6050, L3G4200D
- Magnetometer: HMC5883L, QMC5883L
- IMU: MPU9250, BNO055

#### Light
- LDR (Photoresistor)
- Photodiode: BPW34
- Phototransistor
- Ambient Light: BH1750, TSL2561

#### Distance
- Ultrasonic: HC-SR04, JSN-SR04T
- IR: Sharp GP2Y0A21YK
- Laser: VL53L0X, VL53L1X

#### Gas & Air Quality
- MQ Series: MQ-2, MQ-3, MQ-7, MQ-135
- CO2: MH-Z19, SCD30
- Air Quality: CCS811, BME680

#### Current & Voltage
- Current: ACS712, INA219, INA226
- Voltage Divider circuits

### 7. Displays

#### Character LCD
- 16x2, 20x4 with HD44780 controller

#### Graphic LCD
- Nokia 5110 (PCD8544)
- 128x64 OLED (SSD1306)
- TFT: ILI9341, ST7735

#### 7-Segment
- Single digit, 4-digit with MAX7219

#### LED Matrix
- 8x8, 16x16 with MAX7219

### 8. Communication Modules

#### Wireless
- WiFi: ESP8266, ESP32, ESP-01
- Bluetooth: HC-05, HC-06, HM-10
- LoRa: SX1278, RFM95
- NRF24L01+: 2.4GHz transceiver
- Zigbee: XBee modules

#### Wired
- Ethernet: ENC28J60, W5500
- RS485: MAX485
- CAN: MCP2515

### 9. Power Components

#### Batteries
- Li-Ion: 18650, 21700
- Li-Po: Various sizes
- NiMH: AA, AAA
- Coin Cell: CR2032, CR2025

#### Charging ICs
- TP4056: Li-Ion charger
- MCP73831: Li-Po charger

#### DC-DC Converters
- Buck: LM2596, MP1584, XL4015
- Boost: MT3608, XL6009
- Buck-Boost: LM2577

#### Power Management
- Battery Monitor: MAX17043
- Load Switch: TPS2113

### 10. Connectors & Mechanical

#### Headers & Sockets
- Pin Headers: Male, Female
- JST Connectors: XH, PH, SH
- Terminal Blocks: Screw, Spring

#### Switches & Buttons
- Tactile Switch
- Toggle Switch
- Slide Switch
- Rotary Encoder

#### Relays
- Electromechanical: 5V, 12V
- Solid State: SSR

### 11. Audio Components
- Amplifiers: LM386, PAM8403, TDA2030
- Speakers: 8Ω, 4Ω various sizes
- Microphones: Electret, MEMS
- Buzzers: Active, Passive

### 12. RF Components
- Antennas: 2.4GHz, 433MHz, 868MHz, 915MHz
- RF Modules: 433MHz TX/RX
- Filters: SAW, LC

### 13. Memory
- EEPROM: 24C series (I2C)
- Flash: W25Q series (SPI)
- SD Card modules

### 14. Actuators
- DC Motors: Various voltages
- Servo Motors: SG90, MG996R
- Stepper Motors: 28BYJ-48, NEMA17
- Solenoids: 5V, 12V

### 15. Protection Components
- Fuses: Glass, Resettable (PTC)
- TVS Diodes: Transient protection
- Varistors: MOV
- ESD Protection

## Implementation Files

1. **components_db.py** - SQLAlchemy model
2. **seed_components.py** - Database seeding script
3. **component_search.py** - Search and query functions
4. **API endpoints** - REST API for component lookup

## Usage in ElectroBot

The AI can now:
1. Search components by name, part number, or category
2. Provide detailed specifications
3. Suggest alternatives
4. Show pinouts and connections
5. Recommend components for specific applications

## Example Queries

- "What are the specs of the LM7805?"
- "Show me temperature sensors"
- "I need a motor driver for 12V DC motor"
- "Compare ESP32 vs ESP8266"
- "What resistor do I need for a 5V LED?"

## Future Enhancements

1. Price comparison from suppliers (DigiKey, Mouser, LCSC)
2. Stock availability checking
3. Footprint and symbol libraries
4. 3D models for PCB design
5. Component substitution suggestions
6. Lifecycle status (active, obsolete, NRND)

## Database Size

- **Total Components**: 500+ common components
- **Categories**: 15 major categories
- **Searchable**: By name, part number, specs, tags
- **Indexed**: For fast lookups

## API Endpoints (To Be Added)

```
GET  /api/components              - List all components
GET  /api/components/search?q=    - Search components
GET  /api/components/:id          - Get component details
GET  /api/components/category/:cat - Get by category
POST /api/components/compare      - Compare components
```

This database makes ElectroBot a comprehensive electronics reference tool!
