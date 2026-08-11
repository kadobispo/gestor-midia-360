
import streamlit as st
import pandas as pd
from supabase import create_client, Client
import base64
import uuid
from datetime import date

# ==========================================
# CONFIGURAÇÃO E ESTILIZAÇÃO
# ==========================================
st.markdown("""
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 95% !important; }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #f8fafc; background-attachment: fixed; background-image: linear-gradient(120deg, #fdfbfb 0%, #e2ebf0 100%); }
    div.stButton > button:first-child { background-color: rgba(255, 255, 255, 0.9); color: #1e293b; font-size: 16px !important; font-weight: 600; height: 80px !important; width: 100% !important; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06); transition: all 0.2s ease; display: flex; justify-content: center; align-items: center; text-align: center; line-height: 1.2; white-space: normal !important; }
    div.stButton > button:first-child:hover { background-color: #ffffff; color: #4f46e5; border-color: #c7d2fe; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04); transform: translateY(-3px); }
    div[data-testid="stExpander"] { background-color: #ffffff !important; border-radius: 12px !important; border: 1px solid #e2e8f0 !important; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important; margin-bottom: 10px !important; transition: all 0.2s ease; }
    div[data-testid="stExpander"]:hover { border-color: #cbd5e1 !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important; }
    div[data-testid="stExpander"] details summary { padding: 12px 18px !important; font-weight: 600 !important; color: #1e293b !important; }
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: 600 !important; color: #64748b !important; padding-bottom: 12px !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #4f46e5 !important; }
    .stSelectbox > div > div, .stTextInput > div > div, .stNumberInput > div > div { border-radius: 8px !important; border: 1px solid #e2e8f0 !important; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important; }
    div[data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 700 !important; color: #0f172a !important; letter-spacing: -1px; }
    div[data-testid="stMetricLabel"] { font-size: 0.9rem !important; font-weight: 500 !important; color: #64748b !important; }
    .btn-discreto { text-decoration: none; font-size: 20px; color: #94a3b8; background: #f1f5f9; padding: 6px 12px; border-radius: 8px; transition: all 0.2s ease; display: inline-flex; align-items: center; justify-content: center; border: 1px solid transparent; }
    .btn-discreto:hover { background: #ffffff; color: #4f46e5; border-color: #e2e8f0; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1); transform: scale(1.05); }
    
    /* Estilo para botões pequenos nas opções de foto */
    .btn-pequeno > div > div > button {
        height: 40px !important;
        font-size: 14px !important;
    }
    
    @media print { .stButton, .btn-discreto, .stSelectbox, .stRadio, .stExpander { display: none !important; } }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONEXÃO COM O SUPABASE
# ==========================================
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error("Erro ao conectar no banco de dados. Verifique os Secrets.")
    st.stop()

def upload_imagem(arquivo):
    if arquivo is not None:
        file_extension = arquivo.name.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        file_bytes = arquivo.getvalue()
        
        supabase.storage.from_("fotos_midia").upload(
            path=file_name,
            file=file_bytes,
            file_options={"content-type": arquivo.type}
        )
        url_imagem = supabase.storage.from_("fotos_midia").get_public_url(file_name)
        return url_imagem
    return None
    
def excluir_imagem(url_imagem):
    try:
        # Extrai o nome do arquivo da URL (ex: 'uuid.jpg')
        nome_arquivo = url_imagem.split('/')[-1]
        
        # Remove a imagem do bucket no Supabase
        supabase.storage.from_("fotos_midia").remove([nome_arquivo])
        return True
    except Exception as e:
        st.error(f"Erro ao remover a imagem do Storage: {e}")
        return False

def carregar_dados():
    response = supabase.table("campanhas").select("*").execute()
    return pd.DataFrame(response.data)

df_completo = carregar_dados()

# ==========================================
# 3. ESTADO DA INTERFACE E TÍTULO
# ==========================================
if 'midia_selecionada' not in st.session_state:
    st.session_state.midia_selecionada = None
if 'sub_categoria' not in st.session_state:
    st.session_state.sub_categoria = "Todas as Categorias"

st.markdown("<h1 style='text-align: center; color: #1E293B; padding-top: 0px;'>🖥️ Sistema de Controle de Publicidade 360°</h1>", unsafe_allow_html=True)

st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
with col_b1:
    if st.button("📱 Todos", use_container_width=True): st.session_state.midia_selecionada = "Todos"; st.session_state.sub_categoria = "Todas as Categorias"
with col_b2:
    if st.button("🖼️ Outdoors", use_container_width=True): st.session_state.midia_selecionada = "OUTDOOR"; st.session_state.sub_categoria = "Todas as Categorias"
with col_b3:
    if st.button("🧱 Muros", use_container_width=True): st.session_state.midia_selecionada = "MURO"; st.session_state.sub_categoria = "Todas as Categorias"
with col_b4:
    if st.button("📺 Telas / TV", use_container_width=True): st.session_state.midia_selecionada = "TELAS"; st.session_state.sub_categoria = "Todas as Categorias"
with col_b5:
    if st.button("🚌 Busdoor", use_container_width=True): st.session_state.midia_selecionada = "BUSDOOR"; st.session_state.sub_categoria = "Todas as Categorias"

st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
col_b6, col_b7, col_b8, col_b9, col_b10 = st.columns(5)
with col_b6:
    if st.button("📢 Som", use_container_width=True): st.session_state.midia_selecionada = "SOM"; st.session_state.sub_categoria = "Todas as Categorias"
with col_b7:
    if st.button("🤝 Digital", use_container_width=True): st.session_state.midia_selecionada = "DIGITAL"; st.session_state.sub_categoria = "Todas as Categorias"
with col_b8:
    if st.button("🏋️ Locais", use_container_width=True): st.session_state.midia_selecionada = "ESTABELECIMENTO"; st.session_state.sub_categoria = "Todas as Categorias"
with col_b9:
    if st.button("🏢 Condomínios", use_container_width=True): st.session_state.midia_selecionada = "CONDOMINIO"; st.session_state.sub_categoria = "Todas as Categorias"
with col_b10:
    st.empty() 

# ==========================================
# 4. ÁREA OCULTA E SUB-FILTROS
# ==========================================
if st.session_state.midia_selecionada is not None and not df_completo.empty:
    df_categoria = df_completo.copy()

    if st.session_state.midia_selecionada == "OUTDOOR":
        df_categoria = df_categoria[df_categoria['formato'].str.upper().str.contains('OUTDOOR|TRIEDO|TREINO|PLACA', na=False)]
    elif st.session_state.midia_selecionada == "TELAS":
        df_categoria = df_categoria[df_categoria['formato'].str.upper().str.contains('TELÃO|LED|TV|INDOOR', na=False)]
    elif st.session_state.midia_selecionada == "MURO":
        df_categoria = df_categoria[df_categoria['formato'].str.upper().str.contains('MURO', na=False)]
    elif st.session_state.midia_selecionada == "BUSDOOR":
        df_categoria = df_categoria[df_categoria['formato'].str.upper().str.contains('BUSDOOR|ÔNIBUS', na=False)]
    elif st.session_state.midia_selecionada == "SOM":
        df_categoria = df_categoria[df_categoria['formato'].str.upper().str.contains('SOM|RÁDIO|RADIO|COMERCIO', na=False)]
    elif st.session_state.midia_selecionada == "DIGITAL":
        df_categoria = df_categoria[df_categoria['formato'].str.upper().str.contains('INFLUENCER|SITE|INSTAGRAN|PÁGINA|CORREDOR|CANTOR', na=False)]
    elif st.session_state.midia_selecionada == "ESTABELECIMENTO":
        df_categoria = df_categoria[df_categoria['formato'].str.upper().str.contains('ACADEMIA|BAR|BALNEARIO|CHURACARIA|RESTAURANTE|SORVETERIA|FUTEBOL|LANCHONETE|IGREJA', na=False)]
    elif st.session_state.midia_selecionada == "CONDOMINIO":
        df_categoria = df_categoria[df_categoria['formato'].str.upper().str.contains('CONDOMINIO|CONDOMÍNIO|RESIDENCIAL', na=False)]

    st.markdown("<hr style='margin: 15px 0px 10px 0px; border: none; border-top: 1px solid #cbd5e1;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 15px; font-weight: bold; color: #475569; margin-bottom: 5px;'>🔎 Busca em: {st.session_state.midia_selecionada}</div>", unsafe_allow_html=True)
    
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        categorias_disponiveis = df_categoria['formato'].dropna().unique().tolist()
        categorias_disponiveis.insert(0, "Todas as Categorias")
        filtro_categoria_selecionado = st.selectbox("📌 Qual categoria específica?", categorias_disponiveis, key="filtro_sub_categoria")
    
    with col_filtro2:
        cidades_disponiveis = df_categoria['cidade'].dropna().unique().tolist()
        cidades_disponiveis.insert(0, "Todas as Cidades")
        filtro_cidade_selecionado = st.selectbox("📍 Filtrar resultados por cidade:", cidades_disponiveis, key="filtro_cidade")

    df_final = df_categoria.copy()
    if filtro_categoria_selecionado != "Todas as Categorias":
        df_final = df_final[df_final['formato'] == filtro_categoria_selecionado]
    if filtro_cidade_selecionado != "Todas as Cidades":
        df_final = df_final[df_final['cidade'] == filtro_cidade_selecionado]

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    aba_lista, aba_dashboard = st.tabs(["📑 Gerenciamento (Lista)", "📊 Dashboard"])

    with aba_lista:
        link_download = ""
        if not df_final.empty:
            df_export = df_final[['formato', 'parceiro_local', 'cidade', 'responsavel', 'contato', 'publicidade', 'tipo_investimento', 'valor', 'status']]
            csv = df_export.to_csv(index=False).encode('utf-8')
            b64 = base64.b64encode(csv).decode()
            link_download = f'<a href="data:file/csv;base64,{b64}" download="relatorio_midias.csv" class="btn-discreto" title="Baixar Planilha">📥</a>'
            
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; margin-bottom: 20px;">
                <span style="font-size: 15px; color: #475569; font-weight: 500;">Exibindo <b style="color:#0f172a;">{len(df_final)}</b> resultados encontrados.</span>
                <div style="display: flex; gap: 10px; align-items: center;">
                    {link_download}
                    <a href="javascript:window.print()" class="btn-discreto" title="Imprimir Relatório">🖨️</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if not df_final.empty:
            for index, row in df_final.iterrows():
                icone_status = "🟢" if row.get('status') in ["Ativo", "ok"] else ("🟡" if row.get('status') == "Negociação" else "🔴")
                titulo_linha = f"{icone_status} {row.get('parceiro_local', '')} | 📍 {row.get('cidade', '')} | 🔹 {row.get('formato', '')}"
                
                with st.expander(titulo_linha):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("**👤 Dados do Contato**")
                        st.write(f"**Responsável:** {row.get('responsavel', '')}")
                        st.write(f"**Telefone:** {row.get('contato', '')}")
                        
                    with c2:
                        st.markdown("**📅 Prazos e Valores**")
                        st.write(f"**Renovação:** {row.get('data_fim', 'Não definido')}")
                        if row.get('tipo_investimento') == 'Cortesia':
                            st.write("**Investimento:** 🎁 Cortesia / Permuta")
                        else:
                            st.write(f"**Investimento:** 💰 R$ {float(row.get('valor', 0)):,.2f}")
                            
                    with c3:
                        st.markdown("**⚙️ Gestão Rápida**")
                        status_atual = row.get('status', 'Ativo')
                        opcoes_status = ["Ativo", "Negociação", "Pausado", "Cancelado", "ok"]
                        idx_status = opcoes_status.index(status_atual) if status_atual in opcoes_status else 0
                        novo_status = st.selectbox("Alterar Status:", opcoes_status, index=idx_status, key=f"status_{row['id']}")
                        
                        if novo_status != status_atual:
                            supabase.table("campanhas").update({"status": novo_status}).eq("id", row['id']).execute()
                            st.rerun()
                            
                        st.write("")
                        if st.button("🗑️ Deletar Ponto", key=f"del_{row['id']}", type="primary"):
                            supabase.table("campanhas").delete().eq("id", row['id']).execute()
                            # Se tiver imagem, exclui do storage também
                            if row.get('imagem_path'):
                                excluir_imagem(row['imagem_path'])
                            st.rerun()

                    st.info(f"**📣 Detalhe da Publicidade:** {row.get('publicidade', 'Não especificado')}")

                    # EXIBIR IMAGEM SE EXISTIR NO BANCO
                    if row.get('imagem_path'):
                        st.markdown("**📸 Foto do Ponto**")
                        st.image(row['imagem_path'], use_container_width=True)
                        
                        # Opção para remover apenas a foto
                        st.markdown("<div class='btn-pequeno'>", unsafe_allow_html=True)
                        if st.button("❌ Remover Foto", key=f"rm_foto_{row['id']}"):
                            # 1. Remove do storage
                            excluido = excluir_imagem(row['imagem_path'])
                            if excluido:
                                # 2. Atualiza o banco de dados definindo imagem_path como NULL
                                supabase.table("campanhas").update({"imagem_path": None}).eq("id", row['id']).execute()
                                st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("---")
                    with st.expander("✏️ Editar Dados e Anexar Foto"):
                        with st.form(f"form_edit_{row['id']}"):
                            ec1, ec2, ec3 = st.columns(3)
                            with ec1:
                                e_formato = st.text_input("Categoria", value=str(row.get('formato', '')))
                                e_parceiro = st.text_input("Local / Empresa", value=str(row.get('parceiro_local', '')))
                                e_cidade = st.text_input("Cidade", value=str(row.get('cidade', '')))
                                e_foto = st.file_uploader("📸 Nova Foto", type=['png', 'jpg', 'jpeg'], key=f"foto_edit_{row['id']}")
                            with ec2:
                                e_responsavel = st.text_input("Responsável", value=str(row.get('responsavel', '')))
                                e_contato = st.text_input("Telefone", value=str(row.get('contato', '')))
                                e_publicidade = st.text_input("Detalhe da Publicidade", value=str(row.get('publicidade', '')))
                            with ec3:
                                e_data = st.text_input("Vencimento/Renovação", value=str(row.get('data_fim', '')))
                                e_tipo_inv = st.radio("Pagamento", ["💰 Valor Financeiro", "🎁 Cortesia"], index=0 if row.get('tipo_investimento') == 'Valor' else 1, key=f"radio_edit_{row['id']}")
                                if "Valor" in e_tipo_inv:
                                    try: val_atual = float(row.get('valor', 0))
                                    except: val_atual = 0.0
                                    e_valor = st.number_input("R$", value=val_atual, min_value=0.0, key=f"valor_edit_{row['id']}")
                                    tipo_salvar = "Valor"
                                else:
                                    e_valor = 0.0
                                    tipo_salvar = "Cortesia"

                            if st.form_submit_button("💾 Guardar Alterações"):
                                url_nova_foto = row.get('imagem_path')
                                # Se enviou uma nova foto, faz upload
                                if e_foto is not None:
                                    # Opcional: Se já existia uma foto, exclui a antiga do storage para não ocupar espaço inútil
                                    if row.get('imagem_path'):
                                        excluir_imagem(row['imagem_path'])
                                        
                                    url_nova_foto = upload_imagem(e_foto)
                                    
                                supabase.table("campanhas").update({
                                    "formato": e_formato, "parceiro_local": e_parceiro, "cidade": e_cidade,
                                    "responsavel": e_responsavel, "contato": e_contato, "valor": e_valor,
                                    "tipo_investimento": tipo_salvar, "data_fim": e_data, "publicidade": e_publicidade,
                                    "imagem_path": url_nova_foto
                                }).eq("id", row['id']).execute()
                                st.rerun()

    with aba_dashboard:
        st.markdown("<br>", unsafe_allow_html=True)
        if not df_final.empty:
            metrica1, metrica2, metrica3, metrica4 = st.columns(4)
            df_final['valor'] = pd.to_numeric(df_final['valor'], errors='coerce').fillna(0)
            df_investimento = df_final[df_final['tipo_investimento'] == 'Valor']
            
            metrica1.metric("📍 Total de Pontos", len(df_final))
            metrica2.metric("💰 Total Investido (R$)", f"R$ {df_investimento['valor'].sum():,.2f}")
            metrica3.metric("🎁 Permutas/Cortesias", len(df_final[df_final['tipo_investimento'] == 'Cortesia']))
            metrica4.metric("🟢 Pontos Ativos", len(df_final[df_final['status'].isin(['Ativo', 'ok'])]))
            
            st.markdown("<hr style='margin: 30px 0px; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
            col_graf1, col_graf2, col_graf3 = st.columns(3)
            with col_graf1: st.markdown("**Por Cidade**"); st.bar_chart(df_final['cidade'].value_counts())
            with col_graf2: st.markdown("**Por Categoria**"); st.bar_chart(df_final['formato'].value_counts())
            with col_graf3:
                st.markdown("**Gasto por Cidade (R$)**")
                if not df_investimento.empty: st.bar_chart(df_investimento.groupby('cidade')['valor'].sum(), color="#4F46E5") 
else:
    st.markdown("<br><br><h3 style='text-align: center; color: #94a3b8; font-weight:400;'>👆 Selecione uma categoria acima para carregar o painel.</h3><br>", unsafe_allow_html=True)

# ==========================================
# 5. ADICIONAR NOVO REGISTO
# ==========================================
st.markdown("<hr style='margin: 40px 0px 20px 0px; border-top: 1px dashed #cbd5e1;'>", unsafe_allow_html=True)
with st.expander("➕ REGISTAR NOVO PONTO MANUALMENTE"):
    with st.form("novo_cadastro", clear_on_submit=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            f_formato = st.text_input("Categoria (Ex: OUTDOOR, CONDOMINIO)")
            f_parceiro = st.text_input("Nome do Local")
            f_cidade = st.text_input("Cidade")
            f_foto = st.file_uploader("📸 Anexar Foto do Ponto", type=['png', 'jpg', 'jpeg'])
        with col_f2:
            f_responsavel = st.text_input("Responsável")
            f_contato = st.text_input("Telefone")
            f_publicidade = st.text_input("Detalhe da Publicidade (O que foi divulgado?)")
        with col_f3:
            f_vencimento = st.date_input("Vencimento", date.today())
            f_status = st.selectbox("Status", ["Ativo", "Negociação", "ok"])
            f_tipo_inv = st.radio("Pagamento", ["💰 Valor Financeiro", "🎁 Cortesia"])
            
            if "Valor" in f_tipo_inv: f_valor = st.number_input("Investimento (R$)", min_value=0.0); tipo_salvar_novo = "Valor"
            else: f_valor = 0.0; tipo_salvar_novo = "Cortesia"
            
        if st.form_submit_button("Guardar Novo Registo"):
            if f_formato and f_parceiro:
                url_foto_nova = upload_imagem(f_foto)
                supabase.table("campanhas").insert({
                    "formato": f_formato, "parceiro_local": f_parceiro, "cidade": f_cidade, 
                    "contato": f_contato, "responsavel": f_responsavel, "data_fim": str(f_vencimento), 
                    "valor": f_valor, "tipo_investimento": tipo_salvar_novo, "status": f_status, 
                    "publicidade": f_publicidade, "imagem_path": url_foto_nova
                }).execute()
                st.rerun()
