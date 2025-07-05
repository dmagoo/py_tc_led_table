# TC LED Table Control System

A LED table control system with Python bindings, featuring real-time touch sensing, Art-Net support, and advanced visual effects.

## Folder Structure

```
/home/kacper/py_tc_led_table/
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── .gitmodules                    # Git submodules (external dependencies)
├── CMakeLists.txt                 # Main CMake configuration
├── README.md                      # Project documentation
├── pyproject.toml                 # Modern Python packaging
├── requirements.txt               # Python dependencies
├── config.ini                     # Runtime configuration
│
├── cmake/                         # CMake helper modules
│   ├── CompilerSettings.cmake
│   ├── Dependencies.cmake
│   └── Install.cmake
│
├── src/                           # Source code
│   ├── CMakeLists.txt             # C++ library build configuration
│   ├── tc_led_table/              # C++ core library
│   │   ├── core/                  # Core C++ classes
│   │   ├── config/                # Configuration management
│   │   ├── api/                   # Public API
│   │   └── platform/              # Platform-specific code
│   │
│   # Python application code
│   ├── apps/                      # LED table applications
│   ├── artnet/                    # Art-Net implementation
│   ├── communication/             # MQTT and messaging
│   ├── config/                    # Python configuration
│   ├── effects/                   # Visual effects
│   ├── generators/                # Data generators
│   ├── pygame/                    # Simulator and display
│   ├── runner/                    # Application runner
│   ├── system/                    # System management
│   ├── web/                       # Flask web interface
│   └── utils.py                   # Utilities
│
├── bindings/                      # Python-C++ bindings
│   ├── CMakeLists.txt             # Binding build configuration
│   └── src/                       # pybind11 binding code
│
├── python/                        # Python package structure
│   ├── examples/                  # Example applications
│   └── tc_led_table/              # Built Python extensions
│
├── external/                      # External dependencies
│   ├── CLI11/                     # Command line parsing
│   ├── Unity/                     # Testing framework
│   └── libartnet/                 # Art-Net library
│
├── tests/                         # Test suite
│   ├── cpp/                       # C++ unit tests
│   └── python/                    # Python tests
│
├── examples/                      # Example applications
├── docs/                          # Documentation
├── scripts/                       # Build and utility scripts
└── build/                         # Build output (generated)
```

## Features

### Core Functionality
- **Real-time LED Control**: High-performance C++ core for millisecond-precision LED updates
- **Touch Sensing**: Multi-point capacitive touch detection with noise filtering
- **Network Communication**: Art-Net protocol support for distributed control
- **Python Integration**: Full Python API for rapid prototyping and application development
- **Cross-Platform**: Supports Windows and Linux with optimized platform-specific implementations

### Visual Effects System
- **Generator Framework**: Modular generator system for procedural animations
- **Effect Composition**: Layer multiple effects with blending modes
- **Real-time Processing**: Hardware-accelerated effects processing
- **Touch Interaction**: Touch-responsive effects and interactive applications

### Applications
- **Web Interface**: RESTful API and web dashboard for remote control
- **Game Framework**: pygame-based interactive games and applications
- **Art-Net Bridge**: Professional lighting protocol integration
- **System Integration**: systemd services and udev rules for embedded deployment

## Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone --recursive https://github.com/yourusername/py-tc-led-table.git
cd py-tc-led-table
```

**Note:** The `--recursive` flag downloads git submodules for CLI11, Unity, and libartnet. pybind11 is automatically downloaded via CMake's FetchContent when building Python bindings.

2. **Create and activate virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

3. **Install Python package:**
```bash
pip install -e .
```

4. **Build C++ components (alternative):**
```bash
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

### Configuration

1. **Copy sample configuration:**
```bash
cp config/config.sample.ini config/config.ini
```

2. **Update configuration:**
Edit `config/config.ini` with your hardware configuration.

## Usage

### Python API

```python
import tc_led_table as tlt

# Initialize the LED table
table = tlt.LedTable("config/config.ini")

# Set individual pixel
table.set_pixel(x=5, y=3, color=(255, 0, 0))

# Apply effect
from tc_led_table.effects import RippleEffect
effect = RippleEffect(center=(10, 10), color=(0, 255, 0))
table.apply_effect(effect)

# Start interactive application
from tc_led_table.apps import TouchGame
app = TouchGame(table)
app.run()
```

### Web Interface

Start the web server:
```bash
tc-led-table web --host 0.0.0.0 --port 8080
```

Access the dashboard at `http://localhost:8080`

### Command Line

```bash
# Run built-in applications
tc-led-table app ripple
tc-led-table app snake

# Monitor touch events
tc-led-table monitor

# System status
tc-led-table status
```

## Architecture

### Key Components

1. **Core Library (C++)**: High-performance LED control and touch sensing
2. **Python Bindings**: pybind11-based interface for C++ functionality  
3. **Effects Framework**: Modular system for visual effects and animations
4. **Communication Layer**: Art-Net protocol implementation
5. **Web Interface**: Flask-based REST API and dashboard
6. **Application Framework**: Base classes for interactive applications

## Hardware Setup

### LED Configuration
- **Supported**: WS2812B, SK6812, APA102 LED strips
- **Data Protocol**: SPI or GPIO-based timing
- **Power Requirements**: Calculate based on LED count and brightness

### Touch Sensing
- **Technology**: Capacitive touch sensing via I2C
- **Sensitivity**: Configurable threshold and noise filtering
- **Multi-touch**: Supports simultaneous touch points

### Network Setup
- **Art-Net**: Standard Art-Net universe configuration
- **WiFi**: WPA2/WPA3 with fallback hotspot mode

## API Reference

### Core Classes

- `LedTable`: Main interface for LED control
- `TouchSensor`: Touch event handling
- `ArtNetReceiver`: Art-Net protocol support
- `EffectManager`: Visual effects management

### Effect System

- `BaseEffect`: Base class for all effects
- `PixelEffect`: Per-pixel color effects
- `GeneratorEffect`: Procedural animation effects
- `CompositeEffect`: Layer multiple effects