from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    csv_path = os.path.join(os.path.dirname(__file__), "dados.csv")

    if not os.path.exists(csv_path):
        return f"Arquivo CSV não encontrado em: {csv_path}"

    # Lê CSV com separador ; e converte as datas
    df = pd.read_csv(csv_path, sep=';', dayfirst=True, parse_dates=['DT_BASE', 'DATA_IMPORT'])

    # Formata as datas para dd/mm/yyyy
    df['DT_BASE'] = df['DT_BASE'].dt.strftime('%d/%m/%Y')
    df['DATA_IMPORT'] = df['DATA_IMPORT'].dt.strftime('%d/%m/%Y')

    data = df.to_dict(orient="records")

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
