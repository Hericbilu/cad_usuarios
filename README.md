# User Registration Panel (Flask + SQLite)

A simple project to register users (CPF, name, email, phone, notes) and store files (PDF, DOCX, images, etc.) as BLOBs in a SQLite database.

## 🔗 Online Demo
[https://cad-usuarios-d52x.onrender.com](https://cad-usuarios-d52x.onrender.com)

**Features**
- Create, edit, and view users
- Search by name or CPF
- Add text notes
- Upload files (stored in the database as BLOBs)
- View/download/delete user files

**How to use**
1. Create a virtual environment: `python -m venv venv` and activate it.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the database initialization script: `python db_init.py`.
4. Start the app: `python main.py` and open `http://127.0.0.1:5000`.

**Note:** For simplicity, files are stored in the database as BLOBs. For production, it is recommended to store files in the file system or S3 and save only references in the database.

---

**Created by:** Heric Rodrigues Peres
