import zipfile
import os
import shutil
import tkinter as tk
from tkinter import filedialog

def descompactar_e_mesclar(caminho_dos_zips, caminho_destino):
    # Mude o diretório de trabalho para a pasta dos arquivos .zip
    os.chdir(caminho_dos_zips)

    # Lista todos os arquivos no diretório
    arquivos = os.listdir(caminho_dos_zips)

    # Filtra apenas os arquivos .zip, ignorando arquivos ocultos e inválidos
    zips = [f for f in arquivos if f.endswith('.zip') and not f.startswith('._')]

    total_zips = len(zips)
    print(f"Total de arquivos zip encontrados: {total_zips}")

    for idx, zip_nome in enumerate(zips, start=1):
        try:
            print(f"Processando o arquivo {idx}/{total_zips}: {zip_nome}")
            with zipfile.ZipFile(zip_nome, 'r') as zip_ref:
                # Extrai todos os arquivos para uma pasta temporária
                zip_ref.extractall('temp')
                print(f"Arquivo {zip_nome} descompactado com sucesso.")

                # Mover o conteúdo extraído para o destino mesclando as pastas
                for root, dirs, files in os.walk('temp'):
                    for file in files:
                        caminho_relativo = os.path.relpath(root, 'temp')
                        destino_final = os.path.join(caminho_destino, caminho_relativo)
                        os.makedirs(destino_final, exist_ok=True)
                        shutil.move(os.path.join(root, file), os.path.join(destino_final, file))
                        print(f"Movendo arquivo {file} para {destino_final}")

                # Limpa a pasta temporária
                shutil.rmtree('temp')
                print(f"Temp limpo para o próximo arquivo.")
        except zipfile.BadZipFile:
            print(f"Arquivo inválido: {zip_nome}. Pulando este arquivo.")
        except Exception as e:
            print(f"Erro ao processar {zip_nome}: {e}")

    print("Todos os arquivos foram descompactados e mesclados com sucesso!")

def selecionar_pasta_origem():
    caminho_dos_zips = filedialog.askdirectory(title="Selecione a pasta de origem")
    entry_origem.delete(0, tk.END)
    entry_origem.insert(0, caminho_dos_zips)

def selecionar_pasta_destino():
    caminho_destino = filedialog.askdirectory(title="Selecione a pasta de destino")
    entry_destino.delete(0, tk.END)
    entry_destino.insert(0, caminho_destino)

def iniciar_processo():
    caminho_dos_zips = entry_origem.get()
    caminho_destino = entry_destino.get()
    if not caminho_dos_zips or not caminho_destino:
        print("Por favor, selecione ambas as pastas de origem e destino.")
    else:
        descompactar_e_mesclar(caminho_dos_zips, caminho_destino)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Descompactar e Mesclar Zips")

# Botão e entrada para selecionar a pasta de origem
btn_origem = tk.Button(root, text="Selecionar Pasta de Origem", command=selecionar_pasta_origem)
btn_origem.grid(row=0, column=0, padx=10, pady=10)
entry_origem = tk.Entry(root, width=50)
entry_origem.grid(row=0, column=1, padx=10, pady=10)

# Botão e entrada para selecionar a pasta de destino
btn_destino = tk.Button(root, text="Selecionar Pasta de Destino", command=selecionar_pasta_destino)
btn_destino.grid(row=1, column=0, padx=10, pady=10)
entry_destino = tk.Entry(root, width=50)
entry_destino.grid(row=1, column=1, padx=10, pady=10)

# Botão para iniciar o processo
btn_iniciar = tk.Button(root, text="Iniciar", command=iniciar_processo)
btn_iniciar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
