# Cheche Collection POS 

## 1. Project Overview

**Cheche Collection POS** is a fully offline, Python-based Android Point of Sale system built with:

| Layer | Technology |
|-------|-----------|
| UI | KivyMD 1.1 (Material Design 3) |
| Database | SQLite 3 (WAL mode, foreign keys) |
| Analytics | Matplotlib (Agg backend) |
| Packaging | Buildozer + python-for-android |
| Language | Python 3.10+ |

---

## 2. Folder Structure

```
boutique_pos/
├── main.py                     ← App entry point
├── buildozer.spec              ← Android build config
├── requirements.txt            ← Desktop dev dependencies
│
├── database/
│   ├── __init__.py
│   ├── schema.py               ← All CREATE TABLE + indexes
│   └── db_manager.py           ← Singleton DB, all SQL operations
│
├── ui/
│   ├── login_screen.py
│   ├── main_screen.py          ← BottomNavigation shell
│   ├── dashboard.py     ← KPI cards + charts
│   ├── inventory.py     ← Product CRUD + stock adjust
│   ├── sales.py         ← POS / cart / checkout / receipt
│   ├── reports.py       ← Reports + CSV/XLSX export
│   └── settings.py      ← Users, categories, suppliers, backup
│
│
├── core/
│   ├── session.py              ← Current user session
│   ├── formatters.py           ← Currency, date helpers
│   └── export.py               ← CSV / Excel export
│
```

---

## 3. Database Schema (SQLite)

```
users               – admin / cashier accounts
categories          – product categories
suppliers           – supplier directory
products            – full product catalog (SKU, prices, stock)
customers           – optional customer/credit tracking
sales               – sale headers (invoice, totals, payment)
sale_items          – line items for each sale
stock_adjustments   – audit trail for manual stock changes
schema_meta         – version tracking
```

**Default login:** `admin` / `admin123`  (change immediately in Settings)

---

## 4. Features Implemented

### Authentication
- Login screen with SHA-256 password hashing
- Role-based access: `admin` (full access) vs `cashier` (POS + inventory view)
- Session held in memory; cleared on logout

### Inventory Management
- Add / Edit / Deactivate products
- Fields: name, SKU, category, buying price, selling price, stock qty,
  low-stock threshold, supplier, image path
- Search by name, SKU, or category
- Manual stock adjustment with reason + notes (full audit trail)
- Low-stock alerts in dashboard + settings

### POS / Sales
- Barcode/SKU search, add to cart, adjust quantities
- Per-item discount (%) + cart-level discount
- Tax rate configurable via `SalesTab.TAX_RATE` (default 0 = off; set 0.16 for 16 % VAT)
- Receipt preview with invoice number
- Payment methods: cash, M-Pesa, card, credit
- Atomic sale commit (sale + stock decrement in one transaction)
- Void sale (restores stock)

### Dashboard
- KPI cards: today/week/month sales, transactions, low-stock count, stock value, profit estimate
- Charts: 7-day trend line, top products bar, category pie, profit bar
- All loaded in background thread (UI stays responsive)

### Reports
- Sales report (date range)
- Inventory report
- Profit estimate report
- Low-stock report
- Export to CSV or Excel (.xlsx via openpyxl)
- Files saved to `BoutiquePOS/exports/` on device storage

### Settings
- Manage users (admin only)
- Manage categories & suppliers
- Change password
- Hot database backup
- Low-stock overview

---

## 5. Running on Desktop (Development)

### Prerequisites
```bash
# Ubuntu / Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# macOS (Homebrew)
brew install python

# Windows – use Python 3.10+ from python.org
```

### Setup
```bash
git clone   # or just copy the folder
cd boutique_pos

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install kivy==2.3.0 kivymd==1.2.0 matplotlib openpyxl pillow

python main.py
```

You should see a phone-sized window (400×780 px) with the login screen.

---

## 6. Packaging for Android (APK)

### System requirements
- **Ubuntu 20.04 / 22.04** (64-bit) – recommended
- 8 GB RAM, 20 GB free disk
- Internet during first build (downloads Android NDK/SDK)

### Install Buildozer
```bash
sudo apt update && sudo apt install -y \
    git zip unzip openjdk-17-jdk python3-pip \
    libffi-dev libssl-dev autoconf automake libtool \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

pip install --upgrade buildozer cython==0.29.36
```

### Build debug APK
```bash
cd boutique_pos
buildozer android debug
```
- First build downloads ~2 GB of tools.  Subsequent builds are fast.
- Resulting APK: `bin/boutique_pos-1.0.0-armeabi-v7a-debug.apk`

### Deploy to a connected device
```bash
buildozer android debug deploy run
```
Or copy the APK to the phone and install manually (enable "Unknown Sources").

### Release build (signed)
```bash
buildozer android release
# Then sign with jarsigner / apksigner using your keystore
```

---

## 7. Android Permissions

| Permission | Reason |
|-----------|--------|
| `WRITE_EXTERNAL_STORAGE` | Save exports + backups to Downloads |
| `READ_EXTERNAL_STORAGE` | Read product images from gallery |
| `CAMERA` | Barcode scanning (future feature) |
| `INTERNET` | Not currently used; reserved for future cloud sync |
| `VIBRATE` | Haptic feedback on sale complete |

---

## 8. Customisation Checklist

| Task | Where |
|------|-------|
| Change currency symbol | `utils/formatters.py` → `CURRENCY_SYMBOL` |
| Enable VAT | `screens/sales_screen.py` → `SalesTab.TAX_RATE = 0.16` |
| Change shop name | `main.py` → `BoutiqueApp.shop_name` |
| Change theme colour | `main.py` → `self.theme_cls.primary_palette` |
| Set low-stock default threshold | Per product when creating; or edit DB directly |
| Add product image support | Set `image_path` when creating a product; display in inventory list |

---

## 9. Common Issues

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: kivy` | Activate venv and `pip install kivy==2.3.0` |
| Black screen on Android | Check `buildozer.spec` `requirements=` includes all packages |
| Charts not showing | `pip install matplotlib` on desktop; add to `requirements=` in spec |
| Export fails on Android | Grant storage permission in phone Settings → App Permissions |
| Build fails: NDK | Run `buildozer android clean` then rebuild |

---

## 10. Extending the App

### Add barcode scanning (camera)
1. Add `pyzbar` and `opencv-python` to `requirements.txt` and `buildozer.spec`
2. In `sales_screen.py`, open a KivyMD `MDDialog` with a `Camera` widget
3. Read frames, pass to `pyzbar.decode()`, use result as search query

### Cloud sync
1. Add a `sync/` module with an API client (requests)
2. Call sync after each sale / stock adjustment
3. Add `INTERNET` permission (already in spec)

### Receipt printing (Bluetooth thermal printer)
1. Add `python-escpos` to requirements
2. Use `jnius` on Android to access Bluetooth API
3. Format receipt text and send via ESC/POS commands

---

## 11. Security Notes

- Passwords are hashed with SHA-256 + a fixed salt.  For production, replace
  `database/db_manager.py::_hash_password` with `bcrypt`.
- The SQLite file is stored in the app's private data directory on Android
  (not world-readable without root).
- Backup files go to external storage – protect them on the device.
