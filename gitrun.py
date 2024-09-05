import git
from pathlib import Path

# Caminho para o diretório do repositório Git
repo_path = './'
repo = git.Repo(repo_path)

# Verifica se existem modificações no repositório
if repo.is_dirty(untracked_files=True):
    # Adiciona todos os arquivos modificados e não rastreados
    repo.git.add(all=True)

    # Mensagem de commit
    commit_message = "Comitando com gitpython"  

    # Faz o commit
    repo.index.commit(commit_message)

    # Opcional: Push para o repositório remoto
    origin = repo.remote(name='origin')
    origin.push()

    print("Arquivos comitados e enviados para o repositório remoto.")
else:
    print("Não há mudanças para comitar.")
