# app.py (Versão Refatorada para Hospedagem 24/7)

from flask import Flask, render_template, request
from datetime import datetime
# Os imports 'os' e 'werkzeug.utils' não são mais necessários 
# após remover a lógica de upload e salvamento local de arquivos. 

# --- CONFIGURAÇÃO E FILTRO DE DATA ---

def today_filter(date_str):
    """Filtro Jinja para retornar a data de hoje formatada."""
    # O argumento date_str não é usado, mas mantemos o padrão de filtro.
    return datetime.now().strftime('%d/%m/%Y')

app = Flask(__name__)
# Registra o filtro 'today' para ser usado nos templates Jinja
app.jinja_env.filters['today'] = today_filter 

# NOTA: Removemos as configurações UPLOAD_FOLDER, ALLOWED_EXTENSIONS e allowed_file
# pois elas se referem a uploads locais, que não são ideais para servidores hospedados.

# --- ROTAS DA APLICAÇÃO ---

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'GET':
        # Carrega o formulário
        return render_template('formulario.html')

    if request.method == 'POST':
        # 1. Coleta os dados do formulário
        nome_produto = request.form.get('nome_produto')
        descricao = request.form.get('descricao')
        
        # CAMPOS DE CÁLCULO
        # Coletamos o valor em string para lidar com possíveis erros.
        comprimento_mm_str = request.form.get('comprimento') 
        valor_m_str = request.form.get('valor_m') 
        
        # NOTE: A linha 'file = request.files.get('foto')' pode ser removida, 
        # mas não causa erro se for mantida, pois não a utilizamos mais.
        
        # --- Lógica de Imagem (Apenas para garantir que a variável exista) ---
        # Definimos caminho_foto como None, pois não salvamos localmente.
        # Se você quiser o upload, precisaremos integrar um serviço de nuvem.
        caminho_foto = None 
        
        # 3. Realiza o Cálculo do Orçamento: Comprimento(m) * Valor/m
        valor_total = None 
        comprimento_m = None
        v = None 
        
        try:
            # Converte e calcula
            c_mm = float(comprimento_mm_str)
            v = float(valor_m_str)
            
            comprimento_m = c_mm / 1000 
            valor_total = comprimento_m * v
            
        except (ValueError, TypeError):
            # Lidar com erros de conversão (se o usuário digitar texto ou deixar vazio)
            valor_total = None
            
        # Formatação dos resultados para exibição
        # Usa os valores originais 'valor_m_str' e 'comprimento_mm_str' em caso de erro.
        valor_m_formatado = f"{v:.2f}".replace('.', ',') if v is not None else valor_m_str
        comprimento_m_formatado = f"{comprimento_m:.3f}".replace('.', ',') if comprimento_m is not None else None
        
        # Mensagem de erro se o cálculo falhou
        valor_total_formatado = f"{valor_total:.2f}".replace('.', ',') if valor_total is not None else "Erro no cálculo: Verifique os valores."
        
        # 4. Envia os dados para a página de orçamento
        return render_template(
            'orcamento.html',
            nome=nome_produto,
            descricao=descricao,
            comprimento_mm=comprimento_mm_str, 
            comprimento_m=comprimento_m_formatado,
            valor_m=valor_m_formatado,
            valor_total=valor_total_formatado,
            caminho_foto=caminho_foto # Será None, desabilitando a imagem no template
        )


# --- EXECUÇÃO DA APLICAÇÃO ---
if __name__ == '__main__':
    # Removemos a criação da pasta de upload.
    # Em produção (Render/Gunicorn), esta parte não será executada.
    app.run(debug=True)