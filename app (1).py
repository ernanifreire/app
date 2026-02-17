import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFile, ImageOps
import io
import zipfile
import base64
import os
import requests

ImageFile.LOAD_TRUNCATED_IMAGES = True

st.set_page_config(page_title="Gerador Premium + Preview", page_icon="📱", layout="wide")

# ==============================================================================
# ÍCONE BASE64 (MANTENHA O SEU CÓDIGO GIGANTE AQUI!)
# ==============================================================================
ICONE_PADRAO_BASE64 = """
COLE_AQUI_O_CODIGO_BASE64_DA_MAOZINHA
"""
# ==============================================================================

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configurações")
st.sidebar.subheader("📝 Textos do Banner")
texto_linha1 = st.sidebar.text_input("Frase 1", "Toque na tela")
texto_linha2 = st.sidebar.text_input("Frase 2", "e faça seu pedido!")
st.sidebar.subheader("📐 Ajustes Visuais")
tamanho_logo_pct = st.sidebar.slider("Tamanho da Logo (%)", 50, 120, 85) / 100.0
forcar_fundo_branco = st.sidebar.checkbox("Forçar Fundo Branco", value=False)


# --- FUNÇÕES DE LÓGICA ---
def carregar_fonte_segura():
    font_filename = "Montserrat-Bold.ttf"
    font_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf"
    if not os.path.exists(font_filename):
        try:
            response = requests.get(font_url, timeout=5)
            if response.status_code == 200:
                with open(font_filename, "wb") as f: f.write(response.content)
        except: pass
    
    # --- AQUI: Mudei o tamanho de 70 para 55 (Mais delicado) ---
    try: return ImageFont.truetype(font_filename, 55)
    except: 
        for f in ["Arial.ttf", "DejaVuSans-Bold.ttf", "Roboto-Bold.ttf"]:
            try: return ImageFont.truetype(f, 55)
            except: continue
        return ImageFont.load_default()

def load_icon_from_base64(base64_string):
    if not base64_string or "COLE_AQUI" in base64_string: return None
    try: return Image.open(io.BytesIO(base64.b64decode(base64_string.strip())))
    except: return None

def rgb_to_hex(rgb): return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def calcular_cor_texto(rgb):
    return "#000000" if ((rgb[0]*299 + rgb[1]*587 + rgb[2]*114)/1000) > 160 else "#fff8ef"

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- FUNÇÃO DO MOCKUP (SIMULADOR) ---
def gerar_preview_html(banner_img, primary_color, text_color):
    banner_b64 = image_to_base64(banner_img)
    
    html = f"""
    <div style="
        font-family: 'Segoe UI', sans-serif;
        background-color: #f4f4f4;
        border: 8px solid #333;
        border-radius: 20px;
        overflow: hidden;
        max-width: 400px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin: auto;">
        
        <div style="width: 100%; line-height: 0;">
            <img src="data:image/png;base64,{banner_b64}" style="width: 100%;">
        </div>

        <div style="display: flex; height: 350px;">
            <div style="width: 30%; background: white; padding: 5px; display: flex; flex-direction: column; gap: 5px; border-right: 1px solid #ddd;">
                <div style="border: 1px solid {primary_color}; color: {primary_color}; border-radius: 5px; padding: 8px 2px; text-align: center; font-size: 10px; font-weight: bold;">Combos</div>
                <div style="background-color: {primary_color}; color: {text_color}; border-radius: 5px; padding: 15px 2px; text-align: center; font-size: 10px; font-weight: bold;">Burgers</div>
                <div style="border: 1px solid {primary_color}; color: {primary_color}; border-radius: 5px; padding: 8px 2px; text-align: center; font-size: 10px; font-weight: bold;">Bebidas</div>
            </div>

            <div style="width: 70%; padding: 10px; overflow-y: hidden;">
                <h4 style="margin: 0 0 10px 0; color: #333; font-size: 14px;">Destaques</h4>
                <div style="background: white; border-radius: 8px; padding: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; gap: 8px; margin-bottom: 10px;">
                    <div style="width: 50px; height: 50px; background: #eee; border-radius: 4px;"></div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; font-size: 12px; color: #333;">X-Salada</div>
                        <div style="font-size: 9px; color: #777; margin-bottom: 4px;">Completo</div>
                        <div style="font-weight: bold; color: {primary_color}; font-size: 12px;">R$ 28,00</div>
                    </div>
                </div>
            </div>
        </div>
        <div style="background: #222; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center;">
            <div style="color: white; font-size: 12px;">Total: <b>R$ 0,00</b></div>
            <div style="background: {primary_color}; color: {text_color}; padding: 6px 15px; border-radius: 4px; font-size: 12px; font-weight: bold;">Confirmar</div>
        </div>
    </div>
    """
    return html

def gerar_css_string(logo_img, usar_fundo_branco):
    img = logo_img.convert("RGBA")
    detected_bg = img.getpixel((0, 0))

    if detected_bg[3] == 0 or usar_fundo_branco:
        hex_primary = "#04543b"
        hex_text = "#fff8ef"
    else:
        rgb_bg = detected_bg[:3]
        hex_primary = rgb_to_hex(rgb_bg)
        hex_text = calcular_cor_texto(rgb_bg)

    css_content = f"""/* @import "./themes/slim/slim-imports.scss"; */
:root body#custom-theme.theme {{
  --primary-color: {hex_primary};
  --primary-auxiliary-color: {hex_text};
  --secondary-color: {hex_primary};
  --secondary-auxiliary-color: {hex_text};
  /* ... resto das variaveis ... */
}}
"""
    return css_content, hex_primary, hex_text

def gerar_vertical(logo_img, icon_pil, txt1, txt2, escala_logo, force_white):
    img = logo_img.convert("RGBA")
    bg_color = img.getpixel((0, 0))
    if bg_color[3] == 0 or force_white: bg_color = (255, 255, 255, 255)

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
        except: pass

    font = carregar_fonte_segura()
    def draw_txt(text, y):
        try:
            bbox = draw.textbbox((0,0), text, font=font)
            w = bbox[2] - bbox[0]
        except: w, h = draw.textsize(text, font=font)
        draw.text(((W-w)/2, y), text, font=font, fill="black")

    # --- AQUI ESTÃO OS AJUSTES DE POSIÇÃO (SUBINDO TUDO) ---
    draw_txt(txt1, footer_y + 100) # Subiu de 140 para 100
    draw_txt(txt2, footer_y + 160) # Subiu de 210 para 160
    
    linha_y = footer_y + 250       # Subiu de 300 para 250
    raio_linha = 110               # Encurtou um pouco para combinar com a fonte menor
    draw.line((W//2 - raio_linha, linha_y, W//2 + raio_linha, linha_y), fill="black", width=4)
    # -------------------------------------------------------

    return banner

def gerar_interno(logo_img, force_white):
    img = logo_img.convert("RGBA")
    if img.width < 500:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        img = ImageEnhance.Contrast(img).enhance(1.1)

    bg_color = img.getpixel((0, 0))
    if bg_color[3] == 0 or force_white: bg_color = (255, 255, 255, 255)

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

st.title("📱 Fábrica de Banners + Simulador")
st.markdown("Veja como seu layout vai ficar na tela do totem!")

uploaded_logos = st.file_uploader("Arraste as logos aqui", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)

if uploaded_logos:
    icon_pil = load_icon_from_base64(ICONE_PADRAO_BASE64)
    
    if st.button("🚀 Gerar e Simular"):
        zip_buffer = io.BytesIO()
        progress_bar = st.progress(0)
        
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            for i, logo_file in enumerate(uploaded_logos):
                nome_base = logo_file.name.split('.')[0]
                logo_pil = Image.open(logo_file)
                
                banner_v = gerar_vertical(logo_pil, icon_pil, texto_linha1, texto_linha2, tamanho_logo_pct, forcar_fundo_branco)
                banner_h = gerar_interno(logo_pil, forcar_fundo_branco)
                css_texto, hex_pri, hex_txt = gerar_css_string(logo_pil, forcar_fundo_branco)
                
                img_v = io.BytesIO()
                banner_v.save(img_v, format='PNG')
                zf.writestr(f"Verticais/Vertical_{nome_base}.png", img_v.getvalue())
                
                img_h = io.BytesIO()
                banner_h.save(img_h, format='PNG')
                zf.writestr(f"Internos/Interno_{nome_base}.png", img_h.getvalue())
                
                zf.writestr(f"CSS/style_{nome_base}.css", css_texto)
                progress_bar.progress((i + 1) / len(uploaded_logos))

                if i == 0:
                    st.success("✅ Preview do Resultado Final:")
                    col1, col2, col3 = st.columns([1, 1, 1.2])
                    
                    with col1: 
                        st.subheader("Totem")
                        st.image(banner_v, use_container_width=True)
                    
                    with col2:
                        st.subheader("Banner Interno")
                        st.image(banner_h, use_container_width=True)
                        st.info(f"🎨 Cor Primária: `{hex_pri}`\n\n🎨 Cor Texto: `{hex_txt}`")

                    with col3:
                        st.subheader("📲 Simulação")
                        html_preview = gerar_preview_html(banner_h, hex_pri, hex_txt)
                        st.markdown(html_preview, unsafe_allow_html=True)

        st.download_button("📦 Baixar ZIP Completo", data=zip_buffer.getvalue(), file_name="kit_completo.zip", mime="application/zip")
