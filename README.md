# 💱 Currency Converter – Desktop App

A sleek, offline-cached currency converter powered by Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).  
Works out of the box on Windows, macOS and Linux.

---

## ✨ Features

- ⚡ Instant conversion with live **mid-market** rates  
- 🔍 **Searchable** currency picker (type to filter 160+ codes)  
- 🌓 One-click **Dark / Light** theme switch  
- 💾 Local 1-hour cache → stays inside free API quota  
- 🧵 Background auto-refresh (30 min) – GUI never freezes  
- 📦 Single-file executable available (no Python required)  

---

## 🖼️ Preview

![Screenshot](assets/screenshot.png)  
*(replace with your own image or remove this line)*

---

## 🚀 Quick Start (from source)

1. Clone or download the repo  
   ```bash
   git clone https://github.com/YOUR_GITHUB/currency-converter.git
   cd currency-converter
   ```

2. Create & activate a virtual environment  
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

4. Get a free API key  
   - [exchangerate-api.com](https://app.exchangerate-api.com/sign-up) (1 500 calls / month)  
   - Paste the key into `.env`:  
     ```
     API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
     ```

5. Run  
   ```bash
   python main.py
   ```

---

## 🛠️ Build Stand-alone Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icon.ico --name CurrencyConverter main.py
```

The ready-to-share binary appears in `dist/CurrencyConverter.exe` (or `.app` on macOS).

---

## 📁 Project Layout

```
currency-converter/
├── main.py                 # GUI entry point
├── converter/
│   ├── __init__.py
│   ├── api.py             # API wrapper + cache
│   └── logic.py           # high-level helpers
├── currency_picker.py     # searchable pop-up
├── assets/
│   ├── icon.ico
│   └── screenshot.png
├── requirements.txt
├── .env.example           # copy to .env and fill
├── .gitignore
└── README.md
```

---

## 🤝 Contributing

Pull-requests welcome!  
Please open an issue first for big changes.

---

## 📄 License

MIT – feel free to use in any project, commercial or personal.
