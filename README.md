# 🌱 GreenScan

**GreenScan** is a sustainability-focused project that helps manufacturers and consumers understand the **degradability of products** using **QR codes**.  
Each product is assigned a unique QR code that contains information about its **decomposition status, degradability score, and estimated decomposition years**.

---

## 🚀 Features

- ✅ **Material Selection** – Manufacturers select raw materials and their quantities.  
- ✅ **Degradability Calculation** – Python function computes product degradability score & years.  
- ✅ **Database Storage** – Product degradability data is stored for future reporting.  
- ✅ **QR Code Generation** – A unique QR code is created for every product.  
- ✅ **Consumer Transparency** – Scanning the QR code reveals degradability details.  
- ✅ **PDF Tags** – Generate and download multiple QR tags for printing.  

---

## 🖥️ How It Works

1. Manufacturer opens the **home page** and selects raw materials.  
2. Enters the **quantity** of each material.  
3. Data is sent to the **Flask backend**.  
4. A **Python function** calculates degradability score, status, and decomposition years.  
5. Data is **stored in a database**.  
6. A **unique QR code** is generated and linked to the product.  
7. Consumers scan the QR code to view degradability details.  

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS (Responsive Design)  
- **Database:** SQLite  
- **PDF Generation:** ReportLab  
- **QR Codes:** `qrcode` Python library  
