from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
from io import BytesIO
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max por request
app.secret_key = os.environ.get('FLASK_SECRET', 'troque_esta_chave_para_producao')
DB = 'data.db'

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    q = request.args.get('q', '').strip()
    conn = get_db_connection()
    if q:
        cur = conn.execute("SELECT * FROM users WHERE cpf = ? OR name LIKE ? ORDER BY created_at DESC", (q, f'%{q}%'))
    else:
        cur = conn.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    conn.close()
    return render_template('index.html', users=users, q=q)

@app.route('/users/new', methods=['GET','POST'])
def create_user():
    if request.method == 'POST':
        cpf = request.form.get('cpf','').strip()
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        phone = request.form.get('phone','').strip()
        notes = request.form.get('notes','').strip()
        if not cpf or not name:
            flash('CPF e nome são obrigatórios.')
            return redirect(url_for('create_user'))
        conn = get_db_connection()
        try:
            cur = conn.execute('INSERT INTO users (cpf,name,email,phone,notes) VALUES (?,?,?,?,?)', (cpf,name,email,phone,notes))
            user_id = cur.lastrowid
            files = request.files.getlist('files')
            for f in files:
                if f and f.filename:
                    filename = secure_filename(f.filename)
                    data = f.read()
                    content_type = f.content_type
                    conn.execute('INSERT INTO files (user_id,filename,content_type,data) VALUES (?,?,?,?)', (user_id, filename, content_type, data))
            conn.commit()
            flash('Usuário criado com sucesso.')
            return redirect(url_for('view_user', user_id=user_id))
        except sqlite3.IntegrityError:
            flash('CPF já cadastrado.')
            return redirect(url_for('create_user'))
        finally:
            conn.close()
    return render_template('create_user.html')

@app.route('/users/<int:user_id>', methods=['GET','POST'])
def view_user(user_id):
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        phone = request.form.get('phone','').strip()
        notes = request.form.get('notes','').strip()
        conn.execute('UPDATE users SET name=?, email=?, phone=?, notes=? WHERE id=?', (name,email,phone,notes,user_id))
        files = request.files.getlist('files')
        for f in files:
            if f and f.filename:
                filename = secure_filename(f.filename)
                data = f.read()
                content_type = f.content_type
                conn.execute('INSERT INTO files (user_id,filename,content_type,data) VALUES (?,?,?,?)', (user_id, filename, content_type, data))
        conn.commit()

    user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    if not user:
        conn.close()
        flash('Usuário não encontrado.')
        return redirect(url_for('index'))
    files = conn.execute('SELECT id,filename,content_type,uploaded_at FROM files WHERE user_id=? ORDER BY uploaded_at DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('view_user.html', user=user, files=files)

@app.route('/files/<int:file_id>/download')
def download_file(file_id):
    conn = get_db_connection()
    f = conn.execute('SELECT filename,content_type,data FROM files WHERE id=?', (file_id,)).fetchone()
    conn.close()
    if not f:
        flash('Arquivo não encontrado.')
        return redirect(url_for('index'))
    return send_file(BytesIO(f['data']), download_name=f['filename'], mimetype=f['content_type'], as_attachment=True)

@app.route('/files/<int:file_id>/delete', methods=['POST'])
def delete_file(file_id):
    conn = get_db_connection()
    row = conn.execute('SELECT user_id FROM files WHERE id=?', (file_id,)).fetchone()
    if not row:
        conn.close()
        flash('Arquivo não encontrado.')
        return redirect(url_for('index'))
    user_id = row['user_id']
    conn.execute('DELETE FROM files WHERE id=?', (file_id,))
    conn.commit()
    conn.close()
    flash('Arquivo removido.')
    return redirect(url_for('view_user', user_id=user_id))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    flash('Usuário excluído.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
