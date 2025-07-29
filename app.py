from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/painel")
def painel():
    csv_path = os.path.join(os.path.dirname(__file__), "dados.csv")

    if not os.path.exists(csv_path):
        return f"Arquivo CSV não encontrado em: {csv_path}"

    df = pd.read_csv(csv_path, sep=';', dayfirst=True, parse_dates=['DT_BASE', 'DATA_IMPORT'])

    df['DT_BASE'] = df['DT_BASE'].dt.strftime('%d/%m/%Y')
    df['DATA_IMPORT'] = df['DATA_IMPORT'].dt.strftime('%d/%m/%Y')

    data = df.to_dict(orient="records")

    return render_template("painel.html", data=data)

@app.route("/analise_duplicidade")
def analise_duplicidade():
    return render_template("analise_duplicidade.html")

@app.route("/verificacao_base")
def verificacao_base():
    csv_path = os.path.join(os.path.dirname(__file__), "verificacao_base.csv")

    if not os.path.exists(csv_path):
        return f"Arquivo CSV não encontrado em: {csv_path}"

    # Lê o CSV com separador correto e tratamento de aspas
    df = pd.read_csv(csv_path, sep=';', quotechar='"')

    # Remove espaços em branco
    df['VALIDA'] = df['VALIDA'].str.strip()
    df['BASE'] = df['BASE'].str.strip()

    # Considera "feliz" se a frase CONTÉM "ESTA CERTO BASE"
    df['status'] = df['VALIDA'].apply(lambda x: 'feliz' if 'ESTA CERTO BASE' in x else 'triste')

    data = df.to_dict(orient="records")

    return render_template("verificacao_base.html", data=data)


# ⚠️ ESSENCIAL PARA RODAR O FLASK
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
