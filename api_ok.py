import psycopg2
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    conn = psycopg2.connect("host=localhost dbname=db_PDB user=postgres password=postgresql")
    cur = conn.cursor()

    filter_value = request.args.get('v1')  # Mengambil nilai filter dari parameter v1

    if filter_value:
        cur.execute('SELECT * FROM public.tbl_klasifikasi_text WHERE v1 = %s', (filter_value,))
    else:
        cur.execute('SELECT * FROM public.tbl_klasifikasi_text')

    data = cur.fetchall()

    if data:
        columns = [desc[0] for desc in cur.description]
        results = []
        for row in data:
            results.append(dict(zip(columns, row)))

        json_results = json.dumps(results)
        return json_results
    else:
        return "Data not found"

if __name__ == '__main__':
    app.run(debug=True)
