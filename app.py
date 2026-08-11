import streamlit as st
import time

# 1. Configuração da página (DEVE ser o primeiro comando)
st.set_page_config(page_title="Login - Gestor de Mídia 360", layout="wide")

# 2. Inicializar variável de controle na sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# 3. Lógica de renderização (Mostra o Login ou o Painel)
if not st.session_state.autenticado:
    
    # --- ESTILO PREMIUM APENAS PARA A TELA DE LOGIN ---
    st.markdown("""
        <style>
        /* Esconder topo e rodapé padrão do Streamlit */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container { padding-top: 3rem !important; }
        
        /* Fundo degradê suave */
        .stApp {
            background-color: #f8fafc;
            background-image: radial-gradient(circle at 50% 0%, #fdfbfb 0%, #e2ebf0 100%);
        }
        
        /* Estilo do Cartão de Login */
        .login-card {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 45px 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.08);
            border: 1px solid #e2e8f0;
            text-align: center;
            margin-top: 5vh;
        }
        
        /* Botão de Entrar */
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #4f46e5;
            color: white;
            border-radius: 10px;
            height: 55px;
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

    # Usamos colunas para criar um "falso centro" no layout wide
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        
        st.markdown("<h1 style='color: #1e293b; font-size: 30px; margin-bottom: 5px; font-weight: 700;'>🖥️ Gestor 360</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size: 15px; margin-bottom: 30px;'>Área restrita. Faça login para continuar.</p>", unsafe_allow_html=True)
        
        with st.form("form_login"):
            usuario = st.text_input("👤 Usuário")
            senha = st.text_input("🔑 Senha", type="password")
            
            if st.form_submit_button("Entrar no Sistema"):
                # Validação usando os Secrets do Streamlit
                try:
                    usuarios_permitidos = st.secrets["usuarios"]
                    
                    if usuario in usuarios_permitidos and usuarios_permitidos[usuario] == senha:
                        st.session_state.autenticado = True
                        st.success("✅ Acesso liberado! Carregando...")
                        time.sleep(1) # Aguarda um segundo para dar o efeito de carregamento
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos.")
                except KeyError:
                    st.error("⚠️ Configuração pendente: Cadastre as credenciais nos Secrets.")
                    
        st.markdown("</div>", unsafe_allow_html=True)
        
else:
    # --- CARREGA O SISTEMA ---
    # Se autenticado, ele lê e roda o seu arquivo do painel na mesma página!
    with open("painel.py", encoding="utf-8") as f:
        exec(f.read())