# Wood Delivery Calculator

This repository contains two parts:

- **WDC-Client**: client application and PyInstaller executable configuration
- **WDC-Service**: Python package for the wood delivery service

## Structure

- `WDC-Client/` - client script and executable build config
- `WDC-Service/` - package source and setup script

## Build the service package

```bash
cd WDC-Service
python setup.py sdist
