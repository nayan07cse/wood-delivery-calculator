# 🚚 Wood Delivery Calculator

A Python-based application for calculating wood delivery orders, consisting of:

- 🧮 Client Application (can be converted into a standalone executable)
- 📦 Service Package (installable Python package)

---

## 📂 Project Structure

.
├── WDC-Client/        # Client application
│   ├── wdc_client.py
│   └── wdc_client.spec
│
├── WDC-Service/       # Python service package
│   ├── setup.py
│   └── wdc_service/
│       ├── __init__.py
│       ├── delivery_update.py
│       ├── get_wdc_data.py
│       └── wdc_service.py
│
├── README.md
└── .gitignore

---

## ⚙️ Features

- Python package creation using setuptools
- Standalone executable generation using PyInstaller
- Modular architecture (client + service separation)
- Supports packaging and deployment workflows

---

## 🧰 Requirements

- Python 3.12
- pip or conda
- PyInstaller

---

## 🚀 Getting Started

### Clone the repository

git clone https://github.com/nayan07cse/wood-delivery-calculator.git
cd wood-delivery-calculator

---

## 📦 Build the Service Package

cd WDC-Service
python setup.py sdist

Output will be created in:

dist/wdc_service-1.0.tar.gz

### Install the package

pip install dist/wdc_service-1.0.tar.gz

---

## 🖥️ Build the Client Executable

cd WDC-Client
pyinstaller wdc_client.py

---

## ▶️ Run the Client

### Option 1: Run executable

cd dist
./wdc_client

### Option 2: Run in development mode

cd WDC-Client
python wdc_client.py

---

## 🧱 Technologies Used

- Python 3.12
- setuptools
- PyInstaller

---

## 📌 Notes

- build/, dist/, and .egg-info/ folders are auto-generated
- These folders are excluded from Git using .gitignore
- macOS users may need to allow execution:
  System Settings → Privacy & Security → "Open Anyway"

---

## 👨‍💻 Author

Nayan Nath

---

## 📄 License

This project is for educational purposes.
