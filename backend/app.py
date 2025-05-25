from flask import Flask, jsonify
import MySQLdb
import os
from time import sleep
from contextlib import closing

app = Flask(__name__)

# Configuração via variáveis de ambiente
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'mysql-service')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'meubanco')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', '3306'))

def test_db_connection():
    """Testa a conexão com o MySQL"""
    try:
        with closing(MySQLdb.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            passwd=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT']
        )) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT 1")
                return True
    except Exception:
        return False

@app.route('/api/health')
def health_check():
    """Endpoint para health check do Kubernetes"""
    if test_db_connection():
        return jsonify({"status": "healthy"}), 200
    return jsonify({"status": "unhealthy"}), 503

@app.route('/api/data')
def get_data():
    try:
        with closing(MySQLdb.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            passwd=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT']
        )) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT * FROM items")
                data = cursor.fetchall()
                return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Espera até que o MySQL esteja disponível
    while not test_db_connection():
        print("Aguardando MySQL ficar disponível...")
        sleep(5)
    
    app.run(host='0.0.0.0', port=5000)