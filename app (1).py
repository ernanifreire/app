import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFile
import io
import zipfile
import base64
import os
import requests

# Permite carregar imagens mesmo se tiverem pequenos erros
ImageFile.LOAD_TRUNCATED_IMAGES = True

st.set_page_config(page_title="Gerador de Banner/Skin", page_icon="🎨", layout="wide")

# ==============================================================================
# ÍCONE BASE64 (MANTENHA O SEU CÓDIGO GIGANTE AQUI!)
# ==============================================================================
ICONE_PADRAO_BASE64 = """
COLE_AQUI_O_CODIGO_BASE64_DA_MAOZINHA
"""
# ==============================================================================

# --- CSS PERSONALIZADO PARA BOTÕES VERDES E GRANDES ---
st.markdown("""
<style>
    /* Estiliza todos os botões de download para ficarem verdes e grandes */
    div.stDownloadButton > button {
        background-color: #28a745 !important; /* Verde Sucesso */
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 15px 20px !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important; /* Ocupa a largura da coluna */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        transition: transform 0.2s !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #218838 !important; /* Verde mais escuro no mouse */
        transform: scale(1.02) !important;
        color: white !important;
    }
    /* Centraliza o conteúdo das colunas */
    div[data-testid="stColumn"] {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configurações")

st.sidebar.subheader("📐 Ajustes Visuais")
tamanho_logo_pct = st.sidebar.slider("Tamanho da Logo (%)", 50, 120, 85) / 100.0
forcar_fundo_branco = st.sidebar.checkbox("Forçar Fundo Branco", value=False)

st.sidebar.divider()
st.sidebar.subheader("🎨 Personalizar Cores")
usar_cor_manual = st.sidebar.checkbox("Usar uma cor específica?", value=False)
cor_manual = st.sidebar.color_picker("Escolha a cor do sistema", "#000000")
st.sidebar.caption("Se marcado, esta cor será usada ignorando a cor da logo.")


# --- FUNÇÕES DE LÓGICA ---
def carregar_fonte_segura():
    font_filename = "Montserrat-Bold.ttf"
    font_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf"
    
    if not os.path.exists(font_filename):
        try:
            response = requests.get(font_url, timeout=5)
            if response.status_code == 200:
                with open(font_filename, "wb") as f:
                    f.write(response.content)
        except:
            pass
    
    try:
        return ImageFont.truetype(font_filename, 55)
    except: 
        for f in ["Arial.ttf", "DejaVuSans-Bold.ttf", "Roboto-Bold.ttf"]:
            try:
                return ImageFont.truetype(f, 55)
            except:
                continue
        return ImageFont.load_default()

def load_icon_from_base64(base64_string):
    if not base64_string or "COLE_AQUI" in base64_string:
        return None
    try:
        return Image.open(io.BytesIO(base64.b64decode(base64_string.strip())))
    except:
        return None

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calcular_cor_texto(rgb):
    luminancia = (rgb[0]*299 + rgb[1]*587 + rgb[2]*114)/1000
    if luminancia > 160:
        return "#000000"
    else:
        return "#fff8ef"

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- FUNÇÃO DO MOCKUP (SIMULADOR) ---
def gerar_preview_html(banner_img, primary_color, text_color):
    banner_b64 = image_to_base64(banner_img)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; background: transparent; }}
        .mockup-container {{
            background-color: #f4f4f4;
            border: 8px solid #333;
            border-radius: 20px;
            overflow: hidden;
            max-width: 380px;
            margin: 10px auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        .banner-box {{ width: 100%; line-height: 0; }}
        .banner-box img {{ width: 100%; }}
        .content-box {{ display: flex; height: 350px; }}
        .menu-lat {{ width: 30%; background: white; padding: 5px; display: flex; flex-direction: column; gap: 5px; border-right: 1px solid #ddd; }}
        .menu-item {{ border: 1px solid {primary_color}; color: {primary_color}; border-radius: 5px; padding: 8px 2px; text-align: center; font-size: 10px; font-weight: bold; }}
        .menu-item.active {{ background-color: {primary_color}; color: {text_color}; padding: 15px 2px; }}
        .products-area {{ width: 70%; padding: 10px; overflow-y: auto; }}
        .product-card {{ background: white; border-radius: 8px; padding: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; gap: 8px; margin-bottom: 10px; }}
        .footer {{ background: #222; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; }}
        .btn-confirm {{ background: {primary_color}; color: {text_color}; padding: 6px 15px; border-radius: 4px; font-size: 12px; font-weight: bold; border: none; }}
        ::-webkit-scrollbar {{ width: 5px; }}
        ::-webkit-scrollbar-track {{ background: #f1f1f1; }}
        ::-webkit-scrollbar-thumb {{ background: #888; border-radius: 5px; }}
    </style>
    </head>
    <body>
        <div class="mockup-container">
            <div class="banner-box">
                <img src="data:image/png;base64,{banner_b64}">
            </div>
            <div class="content-box">
                <div class="menu-lat">
                    <div class="menu-item">Combos</div>
                    <div class="menu-item">Burgers</div>
                    <div class="menu-item active">O Brabo</div>
                    <div class="menu-item">Bebidas</div>
                </div>
                <div class="products-area">
                    <h4 style="margin: 0 0 10px 0; color: #333; font-size: 14px;">Destaques</h4>
                    <div class="product-card">
                        <div style="width: 50px; height: 50px; background: #eee; border-radius: 4px;"></div>
                        <div style="flex: 1;">
                            <div style="font-weight: bold; font-size: 12px; color: #333;">X-Salada</div>
                            <div style="font-size: 9px; color: #777; margin-bottom: 4px;">Completo</div>
                            <div style="font-weight: bold; color: {primary_color}; font-size: 12px;">R$ 28,00</div>
                        </div>
                    </div>
                     <div class="product-card">
                        <div style="width: 50px; height: 50px; background: #eee; border-radius: 4px;"></div>
                        <div style="flex: 1;">
                            <div style="font-weight: bold; font-size: 12px; color: #333;">Coca</div>
                            <div style="font-size: 9px; color: #777; margin-bottom: 4px;">Gelada</div>
                            <div style="font-weight: bold; color: {primary_color}; font-size: 12px;">R$ 6,00</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">
                <div style="color: white; font-size: 12px;">Total: <b>R$ 0,00</b></div>
                <button class="btn-confirm">Confirmar</button>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def determinar_cores_finais(logo_img, usar_fundo_branco, usar_manual, cor_manual):
    if usar_manual:
        hex_primary = cor_manual
        rgb_primary = hex_to_rgb(hex_primary)
        hex_text = calcular_cor_texto(rgb_primary)
        return hex_primary, hex_text

    img = logo_img.convert("RGBA")
    detected_bg = img.getpixel((0, 0))

    if detected_bg[3] == 0 or usar_fundo_branco:
        hex_primary = "#04543b"
        hex_text = "#fff8ef"
    else:
        rgb_bg = detected_bg[:3]
        hex_primary = rgb_to_hex(rgb_bg)
        hex_text = calcular_cor_texto(rgb_bg)
    
    return hex_primary, hex_text

def gerar_css_string(hex_primary, hex_text):
    css_content = f"""/* @import "./themes/slim/slim-imports.scss"; */
:root body#custom-theme.theme {{
  --primary-color: {hex_primary};
  --primary-auxiliary-color: {hex_text};
  --secondary-color: {hex_primary};
  --secondary-auxiliary-color: {hex_text};
  /* ... resto das variaveis ... */
}}
"""
    return css_content

def gerar_vertical(logo_img, icon_pil, escala_logo, force_white):
    img = logo_img.convert("RGBA")
    bg_color = img.getpixel((0, 0))
    if bg_color[3] == 0 or force_white:
        bg_color = (255, 255, 255, 255)

    W, H = 1080, 1920
    banner = Image.new('RGBA', (W, H), bg_color)
    draw = ImageDraw.Draw(banner)
    footer_h = 500
    footer_y = H - footer_h
    
    draw.rectangle((0, footer_y, W, H), fill="white")
    draw.ellipse((W//2 - 160, footer_y - 160, W//2 + 160, footer_y + 160), fill="white")

    target_w = int(850 * escala_logo)
    ratio = target_w / img.width
    target_h = int(img.height * ratio)
    if target_h > 1000:
        target_h = 1000
        target_w = int(target_h * (img.width / img.height))
    img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    pos_x = (W - target_w) // 2
    pos_y = (footer_y - target_h) // 2 - 50 
    banner.paste(img_resized, (pos_x, pos_y), img_resized)

    if icon_pil:
        try:
            icon = icon_pil.convert("RGBA")
            icon_h = 150
            icon_w = int(icon.width * (icon_h / icon.height))
            icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
            banner.paste(icon, ((W - icon_w)//2, footer_y - (icon_h//2) - 10), icon)
        except:
            pass

    font = carregar_fonte_segura()
    
    def draw_txt(text, y):
        try:
            bbox = draw.textbbox((0,0), text, font=font)
            w = bbox[2] - bbox[0]
        except:
            w, h = draw.textsize(text, font=font)
        draw.text(((W-w)/2, y), text, font=font, fill="black")

    draw_txt("Toque na tela", footer_y + 120)
    draw_txt("e faça seu pedido!", footer_y + 180)
    
    linha_y = footer_y + 290
    raio_linha = 150
    draw.line((W//2 - raio_linha, linha_y, W//2 + raio_linha, linha_y), fill="black", width=4)
    
    return banner

def gerar_interno(logo_img, force_white):
    img = logo_img.convert("RGBA")
    if img.width < 500:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        img = ImageEnhance.Contrast(img).enhance(1.1)

    bg_color = img.getpixel((0, 0))
    if bg_color[3] == 0 or force_white:
        bg_color = (255, 255, 255, 255)

    W, H = 1080, 350
    banner = Image.new('RGBA', (W, H), bg_color)
    max_h, max_w = 310, 1000
    ratio = min(max_h / img.height, max_w / img.width)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    banner.paste(img, ((W - new_w)//2, (H - new_h)//2), img)
    return banner

# --- INTERFACE PRINCIPAL ---

st.title("📱 Fábrica de Banners/Skin")
st.markdown("Arraste sua logo abaixo para gerar os materiais.")

# MUDANÇA: aceitar apenas 1 arquivo (accept_multiple_files=False)
uploaded_file = st.file_uploader("Upload da Logo", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=False)

if uploaded_file:
    icon_pil = load_icon_from_base64(ICONE_PADRAO_BASE64)
    
    if st.button("🚀 Gerar e Simular"):
        # Processamento direto do arquivo único
        logo_pil = Image.open(uploaded_file)
        nome_base = uploaded_file.name.split('.')[0]
        
        # 1. Determina as cores
        hex_pri, hex_txt = determinar_cores_finais(logo_pil, forcar_fundo_branco, usar_cor_manual, cor_manual)

        # 2. Gera os arquivos
        banner_v = gerar_vertical(logo_pil, icon_pil, tamanho_logo_pct, forcar_fundo_branco)
        banner_h = gerar_interno(logo_pil, forcar_fundo_branco)
        css_texto = gerar_css_string(hex_pri, hex_txt)
        
        # 3. Prepara downloads em memória
        img_v_io = io.BytesIO()
        banner_v.save(img_v_io, format='PNG')
        data_v = img_v_io.getvalue()
        
        img_h_io = io.BytesIO()
        banner_h.save(img_h_io, format='PNG')
        data_h = img_h_io.getvalue()
        
        # --- EXIBIÇÃO EM 3 COLUNAS ---
        st.success("✅ Materiais Gerados com Sucesso!")
        col1, col2, col3 = st.columns([1, 1, 1.2])
        
        # COLUNA 1: VERTICAL
        with col1: 
            st.subheader("Totem")
            st.image(banner_v, use_container_width=True)
            # Botão de Download Verde e Grande
            st.download_button(
                label="⬇️ BAIXAR BANNER VERTICAL",
                data=data_v,
                file_name=f"Vertical_{nome_base}.png",
                mime="image/png"
            )
        
        # COLUNA 2: HORIZONTAL
        with col2:
            st.subheader("Banner Interno")
            st.image(banner_h, use_container_width=True)
            st.info(f"🎨 Primária: `{hex_pri}` | Texto: `{hex_txt}`")
            # Botão de Download Verde e Grande
            st.download_button(
                label="⬇️ BAIXAR BANNER INTERNO",
                data=data_h,
                file_name=f"Interno_{nome_base}.png",
                mime="image/png"
            )

        # COLUNA 3: SIMULAÇÃO + CSS
        with col3:
            st.subheader("📲 Simulação")
            html_preview = gerar_preview_html(banner_h, hex_pri, hex_txt)
            components.html(html_preview, height=600, scrolling=True)
            # Botão de Download Verde e Grande
            st.download_button(
                label="⬇️ BAIXAR ARQUIVO CSS",
                data=css_texto,
                file_name=f"style_{nome_base}.css",
                mime="text/css"
            )
