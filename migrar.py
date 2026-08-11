import sqlite3
from supabase import create_client, Client

# COLOQUE SUAS CREDENCIAIS AQUI
url = "https://enqvbqwwmuyfvdenygig.supabase.co"
key = "sb_publishable_IFem9Umn4XNDTHL_krkFug_z94M3U5k"
supabase: Client = create_client(url, key)

# Conecta no seu banco local
conn = sqlite3.connect("banco_publicidade.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM campanhas")
colunas = [description[0] for description in cursor.description]
linhas = cursor.fetchall()

print(f"Encontrados {len(linhas)} registros. Iniciando migração...")

for linha in linhas:
    dados = dict(zip(colunas, linha))
    
    # Removemos o ID antigo para o Supabase gerar um novo ID limpo na nuvem
    if 'id' in dados:
        del dados['id']
    
    # Executa a inserção na nuvem
    try:
        supabase.table("campanhas").insert(dados).execute()
        print(f"✅ Sucesso: {dados.get('parceiro_local', 'Sem nome')}")
    except Exception as e:
        print(f"❌ Erro ao enviar {dados.get('parceiro_local')}: {e}")
        
print("🚀 Migração concluída com sucesso!")