from pathlib import Path

pasta_alvo = Path.home() / "Downloads"

categorias = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Musica": [".mp3", ".wav"],
}
# inverte o dicionário: extensão -> categoria (facilita a busca)
extensao_para_categoria = {}
for categoria, exts in categorias.items():
    for ext in exts:
        extensao_para_categoria[ext.lower()] = categoria

# Listando e movendo os arquivos
arquivos = [f for f in pasta_alvo.iterdir() if f.is_file()]

for arquivo in arquivos:
    if arquivo.name == "organizar.py":
        continue # não mover o próprio script

    ext = arquivo.suffix.lower()
    categoria = extensao_para_categoria.get(ext, "Outros")
    pasta_destino = pasta_alvo / categoria
    pasta_destino.mkdir(exist_ok=True)
    arquivo.rename(pasta_destino / arquivo.name)
    
    print(f"Movido {arquivo.name} → {categoria}/")