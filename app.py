from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Caminho relativo para o arquivo CSV na mesma pasta do app.py
    csv_path = os.path.join(os.path.dirname(__file__), "dados.csv")

    if not os.path.exists(csv_path):
        return f"Arquivo CSV não encontrado em: {csv_path}"

    # Lê o CSV com separador ponto-e-vírgula, interpreta as datas com dayfirst=True
    df = pd.read_csv(csv_path, sep=';', dayfirst=True, parse_dates=['DATA_IMPORT', 'DH_LIGACAO'])

    # Formata as datas para string no formato dd/mm/yyyy
    df['DH_LIGACAO'] = df['DH_LIGACAO'].dt.strftime('%d/%m/%Y')
    df['DATA_IMPORT'] = df['DATA_IMPORT'].dt.strftime('%d/%m/%Y')

    data = df.to_dict(orient="records")

    return render_template("index.html", data=data)

if __name__ == "__main__":
    # No Render, o Flask deve escutar todas as interfaces na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
