import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFile
import io
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
iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAACAASURBVHic7d152F1VeffxbyZCAkEChDkgIPMgM7SAgKLIoFWsqLXFqi21tRWrUl59tVWrFrRicdYOioWq8DJIEVAGmRUZJMwEkDALARJCQsj8/rGeSEieJOd5zt77Xnvt7+e67isBBX5nnZOz72ftvdYagdRdawKvBLYCNgHWByYBGwz8fv2B348BRgKvWOafGzfw+wXA7IHfLwFmAs8Bs4DnB/56OvAY8BTwu4Hf/xZ4sa4XJkmrMyI6gFSzEcDWwKuBXYBtSRf8pRf9yD8Dj5MagQeAe4A7B+pBUjMhSbWxAVBJRgI7A38A7AHsBuwKTIgMNQxzgDuAG4FfD9RUbAokVcgGQG02DtgHOBA4APhDYN3QRPWZCVwHXAlcBdwCLIoMJKndbADUNtsBRwJHAAcDY2PjhJlFagYuGqhHQtNIah0bAOVuDHAocDTpov+q2DjZmgL8FDiHNDsgSVLrjCRd9L8NPE269231XvcDJwN7DXXgJUmKsC9wGunp+OiLaCl1F3ASsOkQ3gdJkmq3DvDXwK3EXyxLroWkZwWOAUb39M5IklSDvYDvkDbLib44dq0eJ90i2Hy175IkSRUYCbwN+BXxF0EL5gGnkzZIkiSpcmOB44C7ib/oWYPXtcCbVvYGSpI0FOsAnyLtgR99gbN6q6tI+ytIkjRkY4HjSQffRF/QrOHVtaSlmJIkrdYY0oX/MeIvYFY1dSnpPAVJklYwAngnL51iZ5VVC4BvkI5KliQJSKfuXU38Rcqqv2YCJ+A+ApLUaeuRdu1bSPyFyWq2ppBOX5QkdcgI0s59zxJ/IbLiajHwn5R7/LIkaRlbA5cTf/Gx8qknSNsLS5IKNAo4EXiB+AuOlWf9ENgASVIxdgFuJP4CY+VfjwNvQJLUescBc4i/sFjtqcWkQ57GI0lqnUnABcRfTKz21hRgeyRJrfFa3MnPqqZmkTaIkiRlbCTwOWAR8RcOq6z6KrAGkqTsrAOcT/yFwiq3rgM2QpKUjR2Au4m/QFjl1yPA3kiSwh0LzCb+wmB1p2bjxkFSFkZFB1CYE4D/wHuzatYapMZzLum2gCSpIaOAbxH/k6BlnUZ6+FSSVLMJwMXEf/Fb1tL6ETAGSY0bER1AjdkUuBDYIzqItJzzgXcA86ODSF1iA9ANWwBXANtEB5FW4mLSw4EvRgeRusIGoHxbkY7w3So6iLQaPwPeSnpAUFLNbADKtj3p4r9ZdBCpR1cDR5GWC0qqkQ1AuXYCLgM2iQ4iDdG1wJHA89FBpJLZAJRpZ+BKYIPgHNJwXQMcjrcDpNq4Brc82wA/x4u/2u0g4CxgdHQQqVTuBFiWzYBfkJ76l9puO2Bj0vJVSRWzASjHJNIDf9tFB5EqtBfpiOqro4NIpbEBKMME0sV/t+ggUg0OBR4Gbo0OIpXEBqD9RpHulR4cHUSqyQjgaGAKcG9wFqkYPgTYfl8D3hQdQqrZKOAMYO/oIFIpXAbYbh8BvhwdQmrQI6TnAqZHB5HazgagvY4CfoK3cdQ9VwBvID0cKGmYvHi0086kfdPHRgeRAmxF2h/giuggUpvZALTPBNJGP5tGB5ECHQjcDtwdHURqK28BtMsI4GzgbdFBpAw8D+wL3BMdRGojVwG0y0l48ZeWmkBaAjs+OojURt4CaI9Dge9j0yYtayPSiZcXRAeR2sYGoB0mkh76Wzc6iJShPfB5AGnI/GmyHb4NTI4OIWXs28CG0SGkNrEByN97gWOjQ0iZmwR8NTqE1CbeAsjbVsD5uN5f6sUupNsAd0YHkdrAZYD5GgVcBRwQHURqkadJjcCT0UGk3HkLIF9/ixd/aag2AL4bHUJqA28B5GkL4BxgjeggUgttD9xHWhkgaSW8BZCnC/CIX6kfTwLbAbOig0i5cgYgP+8CPhEdQmq5tUm3OC+LDiLlyhmAvKxHeorZ9cxS/+YBu5JuB0hajg8B5uUzePGXqjIWODU6hJQrZwDysSMwBRgTHUQqzFHARdEhpNzYAOTjIuCI6BD6vReAh4FngGcHfp0NzBn43+eQmrWlKzXWJd13Xn+gNgI2BUY3F1krMZV0K2B+dBApJzYAeTgCf0KJsAR4kLRcbGk9CEwDplfw7x8NbAZsSXoifdeB2o3UJKg5JwL/Gh1CyokNQLzRwG2kWwCq13zgl8B1wPUDv382KMurgD8cqIOAnYJydMWzpK21XRYoKRt/SfpJ1KqnHgK+CbyZNEWfq8mkz8I5pFsN0eNWYn2y53dDkmq2Bmm6OfqLsbR6mPT09/60c5ZrPPDHwI9JzxpEj2cp9QywzhDeB0mqzQeJ/1IspRYClwJvp6wNriYAx5FeW/QYl1DOAkgKtybwKPFfiG2vJ4BP0Y39E/YATidtcBM97m0tZwEkhTuB+C/DNtddwPtIm710zabAF4CZxL8PbSxnASSFGQs8TvwXYRvrXuDduIslpK2jPw88T/z70qZyFkBSmPcR/yXYtnoCeD9urDOYDYDTSMsco9+nttTHhzXSktSHEcAdxH8BtqXmkS5u/sS2etsBZxH/nrWhHsNttyU17I3Ef/m1pS4DthneMHfam4FHiH//cq+3DXeAJWk4LiP+iy/3mgEcTzvX8OdiLeBk0vLI6Pcz17pi2KMrSUO0G/FfernXJcAmwx1greAQ0sZI0e9rjrUY2HnYIytJQ/Bt4r/0cq25wEn4dH8dXgH8N/HvcY71jT7GVZJ6shbwHPFfeDnWA8Duwx9a9eh44EXi3++cahY+YCqpZi79G7wuIq1nVzP2JB15HP2+51R/19eIStJq/JL4L7rc6hSc8o+wIek45Oj3P5e6vb/hlKSV24X4L7mcaiHwN32NqPo1Fvgf4j8LudSu/Q2nJA3uK8R/weVSs0l7ISjeSODLxH8mcqjP9zmWkrSCkaRdx6K/4HKo54FD+xtO1eAk4j8b0fUA7jshqWIHE//llkM9C+zX51iqPh8krYuP/pxE1r59j6IkLeMbxH+xRddMYO9+B1K1+xDxn5XIOrX/IZSkZCQe+zsHOKjfgVRj/pH4z0xUPQ6M6n8IJSnd747+UousF4HX9j2KatqXiP/sRNUh/Q+fJMHXif9Ci6rFwLv7H0IFGAH8mPjPUER9vYLxkyTuJ/4LLao+WcH4Kc6awLXEf46arqlVDJ6kbtuO+C+zqDqjgvFTvEnAQ8R/npquraoYPCl3bsNanyOiAwS5jXTojNpvOvBHpJMau+T10QGkJtgA1KeLDcAM4BjgheggqsytwF9Fh2iYDYCkYRtHughGT2U2XcdWMXjK0pnEf76aqhm4HFDSMB1G/JdY0/VflYyccvUKunWM8P7VDJuUL28B1OOA6AANewA4ITqEavUc8GfAouggDXlDdACpbjYA9ehSA7AE+AvSQT8q27XA16JDNOSw6ACS2mcU6ael6CnMpuq71QybWmI8acYn+nNXd80BRlc0ZpI6Ynfiv7yaqseBdasZNrXIEcR/9pqoXasaMClH3gKo3oHRARp0EumkP3XLxcBPokM0YJ/oAFKdbACq15UvjRtJS8PUTR8D5keHqNle0QGkOtkAVG+36AANWAJ8mHTgj7rpfuC06BA12zs6gKT2GE06Ajf63mXddV5VA6ZWWxd4lvjPY131IrBGZaMlZcYZgGrtCIyNDlGzJcCno0MoCzMpexZgLLBLdAipLi5zqVYXnhr+f8CU6BA12QTYgXQa3ETSkre1gIWkfQ5mAU+Tjoy9D888APgK8CFgveggNdkbuCU6hFQHG4BqdaEB+Fx0gAptDbyRtOvbwQxtSeMS0ta41wBXAr8gHZ3bNbNIswCfiQ5Skx2jA0hqh58Qf9+yzrq0uqEKMwp4E+m1LKba8bmJtCXyRo29mjxMotzDry6ocJwkFew24r+w6qw3VjdUIQ4D7qD+cZoH/ADYvpmXlYVvE//5rKNur3KQJJVrFvFfWHXV3cCI6oaqUZsDl9P8mC0kNQKb1v8Sw+1I9TMqOdQc2vu5l9SQDYj/sqqzPlLdUDXqKNKDe5Fj9xxp/Ep/5uZq4j+nddQmVQ6SpPLsQ/w
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

uploaded_file = st.file_uploader("Upload da Logo", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=False)

# LÓGICA DE CACHE PARA PERSISTÊNCIA APÓS DOWNLOAD
# Se o usuário mudar o arquivo, limpa a memória
if 'last_uploaded_file' not in st.session_state or st.session_state['last_uploaded_file'] != uploaded_file:
    st.session_state['generated_data'] = None
    st.session_state['last_uploaded_file'] = uploaded_file

if uploaded_file:
    icon_pil = load_icon_from_base64(ICONE_PADRAO_BASE64)
    
    # Botão "Gerar"
    if st.button("🚀 Gerar e Simular"):
        # Processamento
        logo_pil = Image.open(uploaded_file)
        nome_base = uploaded_file.name.split('.')[0]
        
        hex_pri, hex_txt = determinar_cores_finais(logo_pil, forcar_fundo_branco, usar_cor_manual, cor_manual)
        
        banner_v = gerar_vertical(logo_pil, icon_pil, tamanho_logo_pct, forcar_fundo_branco)
        banner_h = gerar_interno(logo_pil, forcar_fundo_branco)
        css_texto = gerar_css_string(hex_pri, hex_txt)
        html_preview = gerar_preview_html(banner_h, hex_pri, hex_txt)
        
        # Converte para bytes para download
        img_v_io = io.BytesIO()
        banner_v.save(img_v_io, format='PNG')
        
        img_h_io = io.BytesIO()
        banner_h.save(img_h_io, format='PNG')
        
        # SALVA TUDO NA SESSÃO DO STREAMLIT
        st.session_state['generated_data'] = {
            'banner_v': banner_v,
            'banner_h': banner_h,
            'data_v': img_v_io.getvalue(),
            'data_h': img_h_io.getvalue(),
            'css_texto': css_texto,
            'html_preview': html_preview,
            'hex_pri': hex_pri,
            'hex_txt': hex_txt,
            'nome_base': nome_base
        }

    # VERIFICAÇÃO: Se existem dados na sessão (seja porque clicou em Gerar agora ou antes do download)
    if st.session_state['generated_data']:
        data = st.session_state['generated_data']
        
        st.success("✅ Materiais Prontos!")
        col1, col2, col3 = st.columns([1, 1, 1.2])
        
        with col1: 
            st.subheader("Totem")
            st.image(data['banner_v'], use_container_width=True)
            st.download_button(
                label="⬇️ BAIXAR BANNER VERTICAL",
                data=data['data_v'],
                file_name=f"Vertical_{data['nome_base']}.png",
                mime="image/png",
                key="btn_v"
            )
        
        with col2:
            st.subheader("Banner Interno")
            st.image(data['banner_h'], use_container_width=True)
            st.info(f"🎨 Primária: `{data['hex_pri']}` | Texto: `{data['hex_txt']}`")
            st.download_button(
                label="⬇️ BAIXAR BANNER INTERNO",
                data=data['data_h'],
                file_name=f"Interno_{data['nome_base']}.png",
                mime="image/png",
                key="btn_h"
            )

        with col3:
            st.subheader("📲 Simulação")
            components.html(data['html_preview'], height=600, scrolling=True)
            st.download_button(
                label="⬇️ BAIXAR ARQUIVO CSS",
                data=data['css_texto'],
                file_name=f"style_{data['nome_base']}.css",
                mime="text/css",
                key="btn_css"
            )
