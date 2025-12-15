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

## Installing and Using casperfpga

The casperfpga package is responsible for the initial contact with the SKARAB board. It allows you to use existing .fpg files and test board functionalities via Python 2.7 through the computer terminal.

### Installation Steps (Ubuntu 16.04)

1. Install Python 2.7:
   ```bash
   sudo apt install python2.7
   ```

2. Install virtualenv to create virtual environments:
   ```bash
   sudo apt install virtualenv
   ```

3. Create a virtual environment:
   ```bash
   virtualenv -p python2 cfpga_venv
   ```

4. Activate the virtual environment:
   ```bash
   source cfpga_venv/bin/activate
   ```

5. Install git:
   ```bash
   sudo apt install git
   ```

6. Clone the CASPER repository:
   ```bash
   git clone https://github.com/casper-astro/casperfpga
   ```

7. Navigate to the CASPER repository:
   ```bash
   cd casperfpga
   ```

8. Install some requirements:
   ```bash
   sudo apt install build-essential && sudo apt install python-dev
   ```

9. Install the casperfpga requirements:
   ```bash
   pip install -r requirements.txt
   ```

10. Navigate to the progska folder:
    ```bash
    cd progska
    ```

11. Compile progska:
    ```bash
    make
    ```

12. Return to the casperfpga folder:
    ```bash
    cd ..
    ```

13. Install the casperfpga package:
    ```bash
    pip install .
    ```

14. Exit the casperfpga folder:
    ```bash
    cd ..
    ```

15. Install matplotlib:
    ```bash
    pip install matplotlib
    ```

16. Install network tools:
    ```bash
    sudo apt install net-tools
    ```

17. Go to internet settings ("Network Settings") and configure:
    - "Shared to other computers" for IPv4
    - "Ignore" for IPv6

18. Configure MTU to 9000 in "Identity" and restart the 40GbE connection after these steps.

19. To test, check the SKARAB IP with 40GbE connection:
    ```bash
    arp -a
    ```

### Running with IPython

After completing all these steps, the SKARAB can be operated through the IPython IDE:

1. Run IPython (IDE used to operate SKARAB):
   ```bash
   ipython
   ```
   (always run with the Python environment activated)

2. Inside the IPython IDE, import the casperfpga module:
   ```python
   import casperfpga
   ```

3. Check the installed version of casperfpga:
   ```python
   casperfpga.__version__
   ```
   (note that there are two underscores "__" before and after the word version, without spaces)

4. Establish connection with SKARAB:
   ```python
   fpga = casperfpga.CasperFpga('10.42.0.201')
   ```

5. Upload your .fpg file to SKARAB:
   ```python
   fpga.upload_to_ram_and_program('file.fpg')
   ```

## Generating .fpg Files with mlib_devel

To generate new .fpg files using the CASPER toolflow and mlib_devel package, follow these steps:

### Prerequisites

1. Install basic dependencies:
   ```bash
   sudo apt-get install libstdc++6
   sudo apt-get install libgtk2.0-0
   sudo apt-get install dpkg-dev
   sudo apt install python3-pip
   sudo apt install python-dev
   sudo apt install libtinfo5 libncurses5
   sudo add-apt-repository ppa:rock-core/qt4
   sudo apt update
   sudo apt install libqtcore4 libqtgui4
   ```

2. Install MATLAB R2018a:
   - Download MATLAB R2018a from the Mathworks website
   - Extract and install it following the standard installation procedure

3. Install Vivado 2019.1:
   - Download Vivado 2019.1 from Xilinx website
   - Extract the archive:
     ```bash
     tar -xvzf Xilinx_Vivado_SDK_2019.1_0524_1430.tar.gz
     ```
   - Navigate to the extracted folder and run the installer:
     ```bash
     cd Xilinx_Vivado_SDK_2019.1_0524_1430
     sudo ./xsetup
     ```
   - Select "Vivado HL System Edition" and "Vivado Design Suite" under "Design Tools"
   - After installation, test Vivado execution from `/tools/Xilinx/Vivado/2019.1/bin`

4. Configure Python environment:
   ```bash
   sudo apt install python3-venv
   python3 -m venv casper_venv
   source casper_venv/bin/activate
   ```

5. Install the mlib_devel package:
   ```bash
   git clone -b master https://github.com/peralex/mlib_devel
   cd mlib_devel
   ```

6. Add the following requirements to the requirements.txt file:
   ```
   numpy < 1.9
   colorlog
   pyaml
   odict
   #xml2vhdl requirements
   lxml==4.3.0
   pyyaml==3.13
   -e
   git+http://github.com/casper-astro/
   xml2vhdl#egg=xml2vhdl_ox-0.2.2-py3.5.egg
   &subdirectory=scripts/python/xml2vhdl-ox
   ```

7. Before installing the requirements, install python3-dev:
   ```bash
   sudo apt install python3-dev
   ```

8. Install the requirements for mlib_devel:
   ```bash
   pip3 install -r requirements.txt
   ```

9. Configure the startsg.local.example file. Put the following lines in the file:
   ```
   export XILINX_PATH=/tools/Xilinx/Vivado/2019.1
   export MATLAB_PATH=/usr/local/MATLAB/R2018a
   export PLATFORM=lin64
   export JASPER_BACKEND=vivado
   export LD_PRELOAD=${LD_PRELOAD}:"/usr/lib/x86_64-linux-gnu/libexpat.so"
   export CASPER_PYTHON_VENV_ON_START=/home/bingo/casper_venv
   ```

10. Execute mlib_devel using the python3 environment:
    ```bash
    ./startsg startsg.local.example
    ```

### Compiling Simulink Models to .fpg Files

1. Open your Simulink model (e.g., `bingo_dec16_32k.slx`) in MATLAB.

2. With your Simulink model open, run the following command in the MATLAB command window:
   ```matlab
   jasper
   ```

3. The compilation process consists of two stages:
   - Stage 1: Xilinx System Generator compiles Xilinx blocks in your Simulink design to a circuit that can be implemented on your FPGA.
   - Stage 2: Synthesis of your design through Vivado, which turns your design into a physical implementation.

4. After successful compilation, the .fpg file will be created in the `outputs` folder within your model's directory (e.g., `model_folder/outputs/`).

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