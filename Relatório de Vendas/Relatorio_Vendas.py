import os
import base64
import pandas as pd
import matplotlib.pyplot as plt

# Diretório do script (garante que o CSV seja encontrado independente de onde o script é executado)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# carregando os dados
df = pd.read_csv(os.path.join(BASE_DIR, 'vendas.csv'), parse_dates=['data'])
df['receita'] = df['quantidade'] * df['preco']

# agrupando as vendas por mês
df['mes'] = df['data'].dt.to_period('M')
vendas_por_mes = df.groupby('mes')['receita'].sum()
print(vendas_por_mes)

# Produto mais vendido e maior receita
vendas_prod = df.groupby('produto').agg({'quantidade': 'sum', 'receita': 'sum'})
mais_vendido = vendas_prod['quantidade'].idxmax()
maior_receita = vendas_prod['receita'].idxmax()
print(f"Mais vendido: {mais_vendido}")
print(f"Maior receita: {maior_receita}")

# Gráfico: vendas por mês
vendas_por_mes.index = vendas_por_mes.index.astype(str)
plt.figure()
vendas_por_mes.plot(kind='bar')
plt.title("Vendas por mês")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "vendas_mes.png"))

# Gráfico: top 5 produtos
top5 = vendas_prod.nlargest(5, 'receita')
plt.figure()
plt.bar(top5.index, top5['receita'])
plt.title("Top 5 produtos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "top5.png"))

print("Gráficos salvos: vendas_mes.png e top5.png")

# Gerando o relatório em texto com as descobertas e as imagens embutidas (Base64)
def imagem_para_base64(caminho):
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

linhas = []
linhas.append("=" * 60)
linhas.append("RELATÓRIO DE VENDAS")
linhas.append("=" * 60)
linhas.append("")
linhas.append(">> Vendas por mês (receita):")
linhas.append(vendas_por_mes.to_string())
linhas.append("")
linhas.append(f">> Produto mais vendido (quantidade): {mais_vendido}")
linhas.append(f">> Produto com maior receita: {maior_receita}")
linhas.append("")
linhas.append(">> Resumo por produto:")
linhas.append(vendas_prod.to_string())
linhas.append("")
linhas.append("=" * 60)
linhas.append("IMAGENS EMBUTIDAS (Base64)")
linhas.append("Decodifique em: https://base64.guru/converter/decode/image")
linhas.append("=" * 60)

for nome_arquivo in ("vendas_mes.png", "top5.png"):
    caminho = os.path.join(BASE_DIR, nome_arquivo)
    linhas.append("")
    linhas.append(f"--- {nome_arquivo} (Base64 puro abaixo) ---")
    linhas.append(imagem_para_base64(caminho))

with open(os.path.join(BASE_DIR, "report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print("Relatório salvo: report.txt")

# Gerando também um relatório HTML com as imagens visíveis diretamente no navegador
html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Relatório de Vendas</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0;
         max-width: 800px; margin: 40px auto; padding: 0 20px; }}
  h1 {{ border-bottom: 2px solid #38bdf8; padding-bottom: 8px; }}
  h2 {{ color: #38bdf8; margin-top: 32px; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
  th, td {{ border: 1px solid #334155; padding: 8px 12px; text-align: left; }}
  th {{ background: #1e293b; }}
  .destaque {{ background: #1e293b; border-left: 4px solid #22c55e;
               padding: 12px 16px; margin-top: 12px; }}
  img {{ max-width: 100%; border: 1px solid #334155; border-radius: 8px;
        margin-top: 12px; background: white; }}
</style>
</head>
<body>
<h1>📊 Relatório de Vendas</h1>

<h2>Vendas por mês (receita)</h2>
{vendas_por_mes.to_frame().to_html()}

<h2>Descobertas</h2>
<div class="destaque">
  <p>🏆 Produto mais vendido (quantidade): <strong>{mais_vendido}</strong></p>
  <p>💰 Produto com maior receita: <strong>{maior_receita}</strong></p>
</div>

<h2>Resumo por produto</h2>
{vendas_prod.to_html()}

<h2>Gráfico — Vendas por mês</h2>
<img src="data:image/png;base64,{imagem_para_base64(os.path.join(BASE_DIR, 'vendas_mes.png'))}" alt="Vendas por mês">

<h2>Gráfico — Top 5 produtos</h2>
<img src="data:image/png;base64,{imagem_para_base64(os.path.join(BASE_DIR, 'top5.png'))}" alt="Top 5 produtos">

</body>
</html>
"""

with open(os.path.join(BASE_DIR, "report.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("Relatório HTML salvo: report.html")
