import os
import shutil
from datetime import datetime
import platform

def get_creation_time(file_path):
    """
    Retorna a data de criação de um arquivo, compatível com Windows e Unix.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(file_path)
    else:
        stat = os.stat(file_path)
        try:
            return stat.st_birthtime
        except AttributeError:
            # Em sistemas Linux, vamos usar a última modificação como fallback.
            return stat.st_mtime

def organize_videos_by_date(folder_path):
    """
    Organiza os vídeos em subpastas baseadas na data de criação dentro de cada pasta mensal.
    Evita criar subpastas desnecessárias se o vídeo já estiver na pasta correta.
    """
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                file_path = os.path.join(root, file)
                creation_time = get_creation_time(file_path)
                date_folder_name = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
                # Define a nova pasta baseando-se diretamente no caminho inicial fornecido, não no root atual do loop
                new_folder_path = os.path.join(folder_path, date_folder_name)

                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                
                final_path = os.path.join(new_folder_path, file)
                if file_path != final_path: # Checa se o arquivo já está no local final desejado
                    shutil.move(file_path, final_path)
                    print(f'Movido: {file_path} -> {final_path}')
                else:
                    print(f'O vídeo {file} já está na pasta correta: {new_folder_path}')

if __name__ == "__main__":
    folder_path = input("Digite o caminho da pasta contendo os vídeos: ").strip()
    organize_videos_by_date(folder_path)
    print("Organização dos vídeos por data concluída.")
