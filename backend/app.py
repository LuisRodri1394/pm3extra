from flask import Flask, jsonify
import MySQLdb

app = Flask(__name__)

#Configurando o banco (Substituido por variaveis de ambiente no kubernetes)

app.config['MYSQL_HOST'] = 'mysql-service'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'meubanco'


@app.route('/api/data')
def get_data():
    try:
        conn = MySQLdb.connect(host=app.config['MYSQL_HOST'],
                               user=app.config['MYSQL_USER'],
                               passwd=app.config['MYSQL_PASSWORD'],
                               db=app.config['MYSQL_DB'])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        data = cursor.fetchall()
        return jsonify({"data":data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)    