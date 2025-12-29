### file: README.md
# Painel de Cadastro de Usuários (Flask + SQLite)


Projeto simples para cadastrar usuários (CPF, nome, email, telefone, observações) e armazenar arquivos (PDF, DOCX, imagens, etc.) como BLOBs no banco SQLite.


**Recursos**
- Cadastrar, editar e visualizar usuários
- Pesquisar por nome ou CPF
- Adicionar observações em texto
- Fazer upload de arquivos (salvos no banco como BLOB)
- Ver/baixar/excluir arquivos do usuário


**Como usar**
1. Crie um ambiente virtual: `python -m venv venv` e ative-o.
2. Instale dependências: `pip install -r requirements.txt`.
3. Rode o script de inicialização do banco: `python db_init.py`.
4. Inicie: `python main.py` e abra `http://127.0.0.1:5000`.


Observação: por simplicidade os arquivos são guardados no banco como BLOBs. Para produção, recomenda-se armazenar arquivos no sistema de arquivos ou S3 e guardar apenas referências no banco.