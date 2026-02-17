import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import zipfile
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Banners & CSS", page_icon="🎨", layout="wide")

st.title("🏭 Fábrica de Banners & CSS Automático")
st.markdown("Faça upload das logos e baixe tudo pronto. O ícone de touch já está incluído!")

# ==============================================================================
# 1. ÍCONE EMBUTIDO (Cole seu código Base64 aqui dentro das aspas!)
# ==============================================================================
ICONE_PADRAO_BASE64 = """
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
"""
# (O código acima é um exemplo genérico de um quadrado preto. 
#  SUBSTITUA pelo código que você gerou no Passo 1 para ter a sua mãozinha real!)

# --- ÁREA PRINCIPAL (Upload das Logos) ---
uploaded_logos = st.file_uploader("Arraste as logos aqui (pode ser várias)", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)

# --- FUNÇÕES ---

def load_icon_from_base64(base64_string):
    try:
        # Decodifica o texto de volta para imagem
        image_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_data))
    except Exception as e:
        st.error(f"Erro ao carregar ícone padrão: {e}")
        return None

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def calcular_cor_texto(rgb):
    luminancia = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    if luminancia > 160: return "#000000"
    else: return "#fff8ef"

def gerar_css_string(logo_img):
    img = logo_img.convert("RGBA")
    detected_bg = img.getpixel((0, 0))

    if detected_bg[3] == 0:
        hex_primary = "#04543b"
        hex_text = "#fff8ef"
    else:
        rgb_bg = detected_bg[:3]
        hex_primary = rgb_to_hex(rgb_bg)
        hex_text = calcular_cor_texto(rgb_bg)

    css_content = f"""/* @import "./themes/slim/slim-imports.scss"; */
:root body#custom-theme.theme {{
  --black-font: "Montserrat-Black";
  --bold-font: "MontSerrat-Bold";
  --regular-font: "MontSerrat-Regular";
  /* --- CORES INTELIGENTES --- */
  --primary-color: {hex_primary};
  --primary-auxiliary-color: {hex_text};
  --secondary-color: {hex_primary};
  --secondary-auxiliary-color: {hex_text};
  /* -------------------------- */
  --lateral-bar-color: #ffffff;
  --category-border-lateral-bar: #fff8ef;
  --fidelity-bar-font-color: #fff8ef;
  --fidelity-bar-bg-color: #000000;
  --product-card-background-color: #fff8ef;
  --price: var(--primary-color);
  --product-name: var(--dark-color);
  --action-button-bg-color: var(--primary-color);
  --action-button-font-color: var(--primary-auxiliary-color);
  --background: transparent linear-gradient(180deg, #fff 0%, #fff 100%) 0% 0% no-repeat padding-box;
  --classic: flex;
  --slim: none;
}}
"""
    return css_content

def gerar_vertical(logo_img, icon_pil):
    img = logo_img.convert("RGBA")
    bg_color = img.getpixel((0, 0))
    if bg_color[3] == 0: bg_color = (255, 255, 255, 255)

    W, H = 1080, 1920
    banner = Image.new('RGBA', (W, H), bg_color)
    draw = ImageDraw.Draw(banner)

    footer_h = 500
    footer_y = H - footer_h
    draw.rectangle((0, footer_y, W, H), fill="white")
    draw.ellipse((W//2 - 160, footer_y - 160, W//2 + 160, footer_y + 160), fill="white")

    target_w = 850
    ratio = target_w / img.width
    target_h = int(img.height * ratio)
    img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    banner.paste(img_resized, ((W - target_w)//2, (footer_y - target_h)//2 - 50), img_resized)

    # Ícone (Usando o que veio do Base64)
    if icon_pil:
        icon = icon_pil.convert("RGBA")
        icon_h = 150
        icon_w = int(icon.width * (icon_h / icon.height))
        icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
        banner.paste(icon, ((W - icon_w)//2, footer_y - (icon_h//2) - 10), icon)

    # Texto e Fonte (CORREÇÃO AQUI!)
    try:
        # Tenta usar uma fonte TTF se houver
        font = ImageFont.truetype("LiberationSans-Bold.ttf", 70)
    except:
        # Se não houver, usa a padrão MAS com um tamanho grande definido
        # Esta é a correção principal para o texto não ficar pequeno
        font = ImageFont.load_default(size=70) 

    def draw_txt(text, y):
        bbox = draw.textbbox((0,0), text, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((W-w)/2, y), text, font=font, fill="black")

    draw_txt("Toque na tela", footer_y + 180)
    draw_txt("e faça seu pedido!", footer_y + 270)
    
    # Barra (CORREÇÃO AQUI!)
    # Reduzi a espessura de 5 para 3 para ficar mais harmônico
    draw.line((W//2 - 200, footer_y + 380, W//2 + 200, footer_y + 380), fill="black", width=3)
    
    return banner
def gerar_interno(logo_img):
    img = logo_img.convert("RGBA")
    if img.width < 500:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        enhancer_contrast = ImageEnhance.Contrast(img)
        img = enhancer_contrast.enhance(1.1)

    bg_color = img.getpixel((0, 0))
    if bg_color[3] == 0: bg_color = (255, 255, 255, 255)

    W, H = 1080, 350
    banner = Image.new('RGBA', (W, H), bg_color)

    max_h, max_w = 310, 1000
    ratio = min(max_h / img.height, max_w / img.width)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    banner.paste(img, ((W - new_w)//2, (H - new_h)//2), img)
    return banner

# --- BOTÃO DE AÇÃO ---

if uploaded_logos:
    # Carrega o ícone padrão da memória
    icon_pil = load_icon_from_base64(ICONE_PADRAO_BASE64)
    
    if st.button("🚀 Gerar Todos os Banners"):
        
        zip_buffer = io.BytesIO()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            for i, logo_file in enumerate(uploaded_logos):
                nome_base = logo_file.name.split('.')[0]
                status_text.text(f"Processando: {logo_file.name}...")
                
                logo_pil = Image.open(logo_file)
                
                # 1. Gerar Vertical
                banner_v = gerar_vertical(logo_pil, icon_pil)
                img_byte_arr_v = io.BytesIO()
                banner_v.save(img_byte_arr_v, format='PNG')
                zf.writestr(f"Verticais/Vertical_{nome_base}.png", img_byte_arr_v.getvalue())
                
                # 2. Gerar Interno
                banner_h = gerar_interno(logo_pil)
                img_byte_arr_h = io.BytesIO()
                banner_h.save(img_byte_arr_h, format='PNG')
                zf.writestr(f"Internos/Interno_{nome_base}.png", img_byte_arr_h.getvalue())
                
                # 3. Gerar CSS
                css_texto = gerar_css_string(logo_pil)
                zf.writestr(f"CSS/style_{nome_base}.css", css_texto)
                
                progress_bar.progress((i + 1) / len(uploaded_logos))

                if i == 0:
                    st.success("Preview do primeiro resultado:")
                    col1, col2 = st.columns(2)
                    with col1: st.image(banner_v, caption="Vertical", use_container_width=True)
                    with col2: st.image(banner_h, caption="Interno", use_container_width=True)

        status_text.text("✅ Processamento concluído!")
        
        st.download_button(
            label="📦 Baixar Pacote Completo (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="banners_prontos.zip",
            mime="application/zip"
        )

