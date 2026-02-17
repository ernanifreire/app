import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
import io
import zipfile

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Banners & CSS", page_icon="🎨", layout="wide")

st.title("🏭 Fábrica de Banners & CSS Automático")
st.markdown("Faça upload da logo e gere automaticamente: Banner Vertical (Totem), Banner Horizontal (Interno) e o CSS Personalizado.")

# --- BARRA LATERAL (Upload do Ícone Touch) ---
st.sidebar.header("1. Configuração")
uploaded_icon = st.sidebar.file_uploader("Upload do ícone 'Touch' (Mãozinha)", type=["png"])

if not uploaded_icon:
    st.sidebar.warning("⚠️ Por favor, faça upload do ícone da mãozinha (touch) para gerar os banners verticais.")

# --- ÁREA PRINCIPAL (Upload das Logos) ---
st.header("2. Logos dos Clientes")
uploaded_logos = st.file_uploader("Arraste as logos aqui (pode ser várias)", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)

# --- FUNÇÕES DE PROCESSAMENTO (Adaptadas para Memória) ---

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def calcular_cor_texto(rgb):
    # Fórmula de Luminância
    luminancia = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    if luminancia > 160:
        return "#000000" # Fundo Claro -> Letra PRETA
    else:
        return "#fff8ef" # Fundo Escuro -> Letra CLARA

def gerar_css_string(logo_img):
    # Converte para RGBA para garantir leitura correta
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

  /* --- CORES INTELIGENTES GERADAS --- */
  --primary-color: {hex_primary};
  --primary-auxiliary-color: {hex_text};
  --secondary-color: {hex_primary};
  --secondary-auxiliary-color: {hex_text};
  /* ---------------------------------- */

  --lateral-bar-color: #ffffff;
  --category-border-lateral-bar: #fff8ef;
  --fidelity-bar-font-color: #fff8ef;
  --fidelity-bar-bg-color: #000000;
  --product-card-background-color: #fff8ef;
  
  /* VARIAVEIS GERAIS DO SISTEMA */
  --price: var(--primary-color);
  --product-name: var(--dark-color);
  --action-button-bg-color: var(--primary-color);
  --action-button-font-color: var(--primary-auxiliary-color);
  
  --background: transparent linear-gradient(180deg, #fff 0%, #fff 100%) 0% 0% no-repeat padding-box;
  --classic: flex;
  --slim: none;
}}

/* ... (Resto do CSS padrão omitido para economizar espaço, mas a lógica da cor está acima) ... */
"""
    return css_content

def gerar_vertical(logo_img, icon_img):
    img = logo_img.convert("RGBA")
    
    # Detecção de cor
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

    # Ícone
    if icon_img:
        icon = icon_img.convert("RGBA")
        icon_h = 150
        icon_w = int(icon.width * (icon_h / icon.height))
        icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
        banner.paste(icon, ((W - icon_w)//2, footer_y - (icon_h//2) - 10), icon)

    # Texto e Fonte
    try:
        font = ImageFont.truetype("LiberationSans-Bold.ttf", 70)
    except:
        font = ImageFont.load_default()

    def draw_txt(text, y):
        bbox = draw.textbbox((0,0), text, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((W-w)/2, y), text, font=font, fill="black")

    draw_txt("Toque na tela", footer_y + 180)
    draw_txt("e faça seu pedido!", footer_y + 270)
    draw.line((W//2 - 200, footer_y + 380, W//2 + 200, footer_y + 380), fill="black", width=5)
    
    return banner

def gerar_interno(logo_img):
    img = logo_img.convert("RGBA")
    
    # Melhorias
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

if uploaded_logos and uploaded_icon:
    if st.button("🚀 Gerar Todos os Banners"):
        
        # Cria um buffer para o arquivo ZIP final
        zip_buffer = io.BytesIO()
        
        # Abre o ícone uma vez
        icon_pil = Image.open(uploaded_icon)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            
            for i, logo_file in enumerate(uploaded_logos):
                nome_base = logo_file.name.split('.')[0]
                status_text.text(f"Processando: {logo_file.name}...")
                
                # Abre a logo
                logo_pil = Image.open(logo_file)
                
                # 1. Gerar Vertical
                banner_v = gerar_vertical(logo_pil, icon_pil)
                # Salva na memória
                img_byte_arr_v = io.BytesIO()
                banner_v.save(img_byte_arr_v, format='PNG')
                # Adiciona ao ZIP
                zf.writestr(f"Verticais/Vertical_{nome_base}.png", img_byte_arr_v.getvalue())
                
                # 2. Gerar Interno
                banner_h = gerar_interno(logo_pil)
                img_byte_arr_h = io.BytesIO()
                banner_h.save(img_byte_arr_h, format='PNG')
                zf.writestr(f"Internos/Interno_{nome_base}.png", img_byte_arr_h.getvalue())
                
                # 3. Gerar CSS
                css_texto = gerar_css_string(logo_pil)
                zf.writestr(f"CSS/style_{nome_base}.css", css_texto)
                
                # Atualiza barra
                progress_bar.progress((i + 1) / len(uploaded_logos))

                # Mostra preview do primeiro apenas para não poluir
                if i == 0:
                    st.success("Preview do primeiro resultado:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(banner_v, caption="Exemplo Vertical", use_container_width=True)
                    with col2:
                        st.image(banner_h, caption="Exemplo Interno", use_container_width=True)

        status_text.text("✅ Processamento concluído!")
        
        # Botão de Download do ZIP
        st.download_button(
            label="📦 Baixar Pacote Completo (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="banners_prontos.zip",
            mime="application/zip"
        )

elif not uploaded_logos:
    st.info("👈 Faça upload do ícone na barra lateral e das logos acima para começar.")