# SKARAB_BINGO
This repository contains code for programming the digital back-end of the BINGO radio telescope.

## Overview

This repository contains firmware and control scripts for the SKARAB platform used in the BINGO (Baryon Oscillation Spectroscopic Survey) radio telescope project. The firmware is designed to work with the SKARAB (Square Kilometre Array Reconfigurable Application Board) platform equipped with Virtex-7 FPGA and ADC mezzanine cards.

## Firmware Directories

### 1. baseband_23mhz

This directory contains firmware for a baseband processing system operating at 23 MHz bandwidth.

#### Contents:
- `pulsar_23mhz_baseband_debug (1).slx`: Simulink model for the baseband processing firmware
- `bingo_dec16_32k_2024-09-17_1610.fpg`: Compiled FPGA firmware file
- `pulsar_23mhz_conplot.py`: Python script for controlling the firmware and plotting spectra

#### Usage:
To run the baseband firmware, use the following command:

```bash
python pulsar_23mhz_conplot.py <skarab IP or hostname> -l <accumulation length> -b <fpgfile name>
```

Replace:
- `<skarab IP or hostname>` with the IP address of your SKARAB system
- `<accumulation length>` with the desired number of accumulations
- `<fpgfile name>` with the firmware file (`bingo_dec16_32k_2024-09-17_1610.fpg`)

### 2. bingo_dec16_32k_

This directory contains firmware implementing a spectrometer with 16x decimation and 32K points.

#### Contents:
- `bingo_dec16_32k.slx`: Simulink model for the spectrometer firmware
- `bingo_dec16_32k.py`: Python control script for the spectrometer

#### Usage:
To run the bingo_dec16_32k firmware, use the following command:

```bash
python bingo_dec16_32k.py <skarab IP or hostname> -l <accumulation length> -b <fpgfile name>
```

Replace:
- `<skarab IP or hostname>` with the IP address of your SKARAB system
- `<accumulation length>` with the desired number of accumulations
- `<fpgfile name>` with the appropriate firmware file

### 3. decimation8_1k_

This directory contains firmware implementing a system with 8x decimation and 1K points.

#### Contents:
- `decimation8_1k (1).slx`: Simulink model for the decimation firmware
- `decimation8_1k (1).py`: Python control script

#### Usage:
To run the decimation8_1k firmware, use the following command:

```bash
python decimation8_1k\ (1).py <skarab IP or hostname> -l <accumulation length> -b <fpgfile name>
```

Replace:
- `<skarab IP or hostname>` with the IP address of your SKARAB system
- `<accumulation length>` with the desired number of accumulations
- `<fpgfile name>` with the appropriate firmware file

## Requirements

- Python 2.7
- [casperfpga](https://github.com/casper-astro/casperfpga) library
- MATLAB & Simulink (for development)
- Xilinx Vivado (for development)
- SKARAB hardware platform with ADC mezzanine cards

## Hardware Overview

The SKARAB platform uses:
- Virtex-7 XC7VX690T FPGA
- TI ADC32RF45 ADC mezzanine cards (14-bit, 3 GSPS per channel)
- QSFP+ Ethernet interfaces

For more detailed information about the hardware and its capabilities, see the `Nota_tecnica_SKARAB/main.tex` document.

## CASPER Toolflow

This project is built using the CASPER toolflow methodology. For beginners, refer to the `CASPER_tut_intro/CASPER_tut_intro.txt` document which provides an introduction to Simulink-based firmware development for CASPER platforms.

## Generating .fpg Files with mlib_devel

To generate new .fpg files using the CASPER toolflow and mlib_devel package, follow these steps:

### Prerequisites

1. Install the mlib_devel package:
   ```bash
   git clone -b master https://github.com/peralex/mlib_devel
   cd mlib_devel
   ```

2. Install the required dependencies:
   ```bash
   sudo apt install python3-dev
   pip3 install -r requirements.txt
   ```

3. Configure your environment by creating a startsg.local file with the following content:
   ```
   export XILINX_PATH=/tools/Xilinx/Vivado/2019.1
   export MATLAB_PATH=/usr/local/MATLAB/R2018a
   export PLATFORM=lin64
   export JASPER_BACKEND=vivado
   export LD_PRELOAD=${LD_PRELOAD}:"/usr/lib/x86_64-linux-gnu/libexpat.so"
   export CASPER_PYTHON_VENV_ON_START=/home/bingo/casper_venv
   ```

4. Start MATLAB with the CASPER toolflow:
   ```bash
   ./startsg startsg.local
   ```

### Compiling Simulink Models to .fpg Files

1. Open your Simulink model (e.g., `bingo_dec16_32k.slx`) in MATLAB.

2. Run the complete build process by clicking the "Compile" button in your Simulink model or by running the following command in the MATLAB command window:
   ```matlab
   jasper_frontend
   ```

3. The compilation process consists of two stages:
   - Stage 1: Xilinx System Generator compiles Xilinx blocks in your Simulink design to a circuit that can be implemented on your FPGA.
   - Stage 2: Synthesis of your design through Vivado, which turns your design into a physical implementation.

4. After successful compilation, the .fpg file will be created in the 'outputs' folder in the working directory of your Simulink model.

### Advanced Compilation

For advanced users who want to run the two stages of compilation separately (to free up MATLAB sooner), you can run the first stage from the MATLAB prompt with:
```matlab
>> jasper_frontend
```

After completion, the last message printed will tell you how to finish the compile. It will look something like:
```bash
python /path_to/mlib_devel/jasper_library/exec_flow.py -m /home/user/path_to/your_model.slx --middleware --backend --software
```

Run this command in a separate terminal after sourcing appropriate environment variables.

## Programming the FPGA

Reconfiguration of CASPER FPGA boards is achieved using the casperfpga python library:

1. Navigate to the folder containing your .fpg file.

2. Start interactive python:
   ```bash
   ipython
   ```

3. Import the fpga control library:
   ```python
   import casperfpga
   ```

4. Connect to the board:
   ```python
   fpga = casperfpga.CasperFpga('SKARAB hostname or IP address')
   ```

5. Program the FPGA with your .fpg file:
   ```python
   fpga.upload_to_ram_and_program('your_fpgfile.fpg')
   ```

## Contributing

Any modifications to the firmware should follow the CASPER development guidelines and be tested thoroughly before deployment.