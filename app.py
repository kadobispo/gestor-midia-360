import streamlit as st
import time

# 1. Configuração da página
st.set_page_config(page_title="Login - Gestor de Mídia 360", layout="wide")

# 2. Verifica se o usuário já está logado pela URL
url_token = st.query_params.get("session", "")
try:
    usuarios_permitidos = st.secrets["usuarios"]
except KeyError:
    st.error("⚠️ Configuração pendente: Cadastre as credenciais nos Secrets.")
    st.stop()

# Valida se o token na URL corresponde a um usuário real 
usuario_autenticado = url_token if url_token in usuarios_permitidos else None

# 3. Lógica de renderização
if not usuario_autenticado:
    
    st.markdown("""
        <style>
        /* Esconder topo e rodapé padrão do Streamlit */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container { padding-top: 3rem !important; }
        
        /* Fundo da tela inteira */
        .stApp { 
            background-color: #f8fafc; 
            background-image: radial-gradient(circle at 50% 0%, #fdfbfb 0%, #e2ebf0 100%); 
        }
        
        /* Arredondar os cantos da imagem da logo para um visual moderno */
        img { 
            border-radius: 12px; 
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Transformar o formulário padrão no Cartão de Login branco */
        [data-testid="stForm"] {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
            border: 1px solid #e2e8f0;
        }

        /* Estilizar os campos de input (Usuário e Senha) com bordas bem definidas */
        [data-testid="stTextInput"] > div > div {
            background-color: #f8fafc !important; /* Fundo cinza bem clarinho */
            border: 1px solid #cbd5e1 !important; /* Borda visível */
            border-radius: 8px !important;
            padding: 2px 5px;
        }
        /* Cor da borda ao clicar para digitar */
        [data-testid="stTextInput"] > div > div:focus-within {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 1px #4f46e5 !important;
        }

        /* Botão de Entrar */
        div[data-testid="stFormSubmitButton"] > button { 
            background-color: #4f46e5; 
            color: white; 
            border-radius: 8px; 
            height: 50px; 
            font-weight: bold; 
            font-size: 16px; 
            border: none; 
            transition: all 0.3s; 
            width: 100%; 
            margin-top: 15px; 
        }
        div[data-testid="stFormSubmitButton"] > button:hover { 
            background-color: #4338ca; 
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3); 
            transform: translateY(-2px); 
        }
        </style>
    """, unsafe_allow_html=True)

    # Usa colunas para centralizar tudo na tela
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # A logo agora é renderizada de forma limpa acima do formulário
        try:
            st.image("IMG_2267.jpg", use_container_width=True)
        except:
            st.warning("⚠️ Imagem da logo não encontrada. Verifique se o nome do arquivo no GitHub é exatamente IMG_2267.jpg")
            
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Espaçamento invisível
        
        # O Formulário que agora vai funcionar como a caixa branca
        with st.form("form_login"):
            st.markdown("<h4 style='text-align: center; color: #334155; margin-bottom: 15px; font-weight: 600;'>Acesso Restrito</h4>", unsafe_allow_html=True)
            
            usuario = st.text_input("👤 Usuário")
            senha = st.text_input("🔑 Senha", type="password")
            
            if st.form_submit_button("Entrar no Sistema"):
                if usuario in usuarios_permitidos and usuarios_permitidos[usuario] == senha:
                    st.query_params["session"] = usuario
                    st.success("✅ Acesso liberado! Carregando...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos.")
                    
else:
    # --- CARREGA O SISTEMA ---
    st.session_state.usuario_atual = usuario_autenticado
    
    with open("painel.py", encoding="utf-8") as f:
        exec(f.read())
