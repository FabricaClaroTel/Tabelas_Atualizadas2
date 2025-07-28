from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    csv_path = r"C:\Users\f119031\Documents\painel_atualizacoes\dados.csv"

    if not os.path.exists(csv_path):
        return f"Arquivo CSV não encontrado em: {csv_path}"

    # Lê o CSV com separador ponto-e-vírgula, interpreta as datas com dayfirst=True
    df = pd.read_csv(csv_path, sep=';', dayfirst=True, parse_dates=['DATA_IMPORT', 'DH_LIGACAO'])

    # Converte as datas para string formatada dd/mm/yyyy para exibir no HTML
    df['DH_LIGACAO'] = df['DH_LIGACAO'].dt.strftime('%d/%m/%Y')
    df['DATA_IMPORT'] = df['DATA_IMPORT'].dt.strftime('%d/%m/%Y')

    data = df.to_dict(orient="records")

    # DEBUG: mostra no console para confirmar
    print(data)

    return render_template("index.html", data=data)

if __name__ == "__main__":
    # O Flask vai escutar em todas as interfaces (0.0.0.0) para aceitar conexões externas
    # O IP que os outros usarão é 10.89.144.33 na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
