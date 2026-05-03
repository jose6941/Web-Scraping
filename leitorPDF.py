import pdfplumber
import re
import json
import os
from datetime import datetime

def extrair_dados_legislacao(caminho_pdf):
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pag = pagina.extract_text()
            if texto_pag:
                texto_completo += texto_pag + "\n"

    modalidade_match = re.search(r'(PORTARIA|DECRETO|RESOLUÇÃO)', texto_completo, re.IGNORECASE)
    modalidade = modalidade_match.group(1).capitalize() if modalidade_match else "Portaria"

    num_pattern = re.search(r'(?:Nº|№|No)\s*([\d.]+)(?:/(\d{4}))?', texto_completo)
    numero_limpo = int(num_pattern.group(1).replace('.', '')) if num_pattern else 0
    ano_doc = int(num_pattern.group(2)) if num_pattern and num_pattern.group(2) else None

    data_formatada = None
    regex_data = r'(\d{1,2})\s+de\s+(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})'
    meses = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6,
        "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
    }
    datas_encontradas = list(re.finditer(regex_data, texto_completo, re.IGNORECASE))
    if datas_encontradas:
        ultima_data = datas_encontradas[-1]
        dia = int(ultima_data.group(1))
        mes = meses[ultima_data.group(2).lower()]
        ano = int(ultima_data.group(3))
        data_formatada = datetime(ano, mes, dia).strftime("%Y-%m-%d %H:%M:%S")
        if not ano_doc: ano_doc = ano

    ementa = ""
    ementa_match = re.search(r'Art\.\s*1[º|o]\.\s*(.*?)(?=\n\s*Art\.\s*2|\n\s*Artigo\s*2)', texto_completo, re.DOTALL)
    
    if ementa_match:
        trecho_bruto = ementa_match.group(1)
        linhas = [linha.strip() for linha in trecho_bruto.split('\n') if linha.strip()]
        linhas_limpas = []
        for linha in linhas:
            if "Parágrafo único" in linha:
                break
            linhas_limpas.append(linha)
        
        ementa = " ".join(linhas_limpas)
        ementa = re.sub(r'\s+', ' ', ementa).strip()

    nome_arquivo = os.path.basename(caminho_pdf)
    
    return {
        "ementa": f"Art. 1º. {ementa}",
        "modalidade": modalidade,
        "data": data_formatada,
        "ano": ano_doc,
        "numero": numero_limpo,
        "complementoNumero": f"/{ano_doc}" if ano_doc else "",
        "arquivos": [{
            "nome": f"{modalidade} {numero_limpo}/{ano_doc}",
            "arquivo": nome_arquivo,
            "principal": "S"
        }]
    }

def gerar_json_final(pasta_origem, nome_saida="resultado.json"):
    resultados = []
    if not os.path.exists(pasta_origem):
        return
        
    for arquivo in os.listdir(pasta_origem):
        if arquivo.lower().endswith(".pdf"):
            dados = extrair_dados_legislacao(os.path.join(pasta_origem, arquivo))
            resultados.append(dados)
    
    with open(nome_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

gerar_json_final("./pdfs")