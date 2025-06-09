from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Criar banco de dados
def criar_db():
    conn = sqlite3.connect('financas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS despesas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 descricao TEXT,
                 categoria TEXT,
                 valor REAL,
                 data TEXT,
                 tipo TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('financas.db')
    c = conn.cursor()
    
    # Busca contas fixas
    c.execute("SELECT * FROM despesas WHERE tipo = 'fixa'")
    contas_fixas = c.fetchall()
    
    # Busca gastos variáveis
    c.execute("SELECT * FROM despesas WHERE tipo = 'variavel' ORDER BY data DESC")
    gastos_diarios = c.fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         contas_fixas=contas_fixas,
                         gastos_diarios=gastos_diarios)

@app.route('/add', methods=['POST'])
def add_despesa():
    descricao = request.form['descricao']
    categoria = request.form['categoria']
    valor = float(request.form['valor'])
    data = request.form['data']
    tipo = request.form['tipo']
    
    conn = sqlite3.connect('financas.db')
    c = conn.cursor()
    c.execute("INSERT INTO despesas (descricao, categoria, valor, data, tipo) VALUES (?, ?, ?, ?, ?)",
              (descricao, categoria, valor, data, tipo))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    criar_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
    if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)