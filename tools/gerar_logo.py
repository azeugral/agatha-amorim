"""Logo em tinta café e em branco (a partir do logo transparente dela), favicons com os raios do sol, og.jpg e foto.
Uso: python tools/gerar_logo.py"""
import pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[1]
REF = RAIZ.parent / "_ref"
IMG = RAIZ / "assets" / "img"
CAFE = (52, 40, 32)
AREIA = (244, 237, 228)
TAUPE = (185, 160, 136)
CARAMELO = (185, 122, 76)

def tingir(logo, cor):
    a = logo.getchannel("A")
    out = Image.new("RGBA", logo.size, cor + (0,))
    out.putalpha(a)
    return out

def main():
    logo = Image.open(REF / "cliente" / "4.webp").convert("RGBA")
    logo = logo.crop(logo.getchannel("A").getbbox())
    base = logo.copy(); base.thumbnail((1400, 1400))
    tingir(base, CAFE).save(IMG / "logo.webp", quality=92, method=6)
    tingir(base, (255, 255, 255)).save(IMG / "logo-branco.webp", quality=92, method=6)
    print("logo", base.size)

    # favicon: o "A" do próprio logo (isolado em _ref/cliente/a-logo.png), em caramelo, sem fundo
    letra = tingir(Image.open(REF / "cliente" / "a-logo.png").convert("RGBA"), CARAMELO)
    base_a = Image.open(REF / "cliente" / "a-logo.png").convert("RGBA")
    grossa = base_a.copy(); grossa.putalpha(base_a.getchannel("A").filter(ImageFilter.MaxFilter(13)))
    grossa = tingir(grossa, CARAMELO)  # traço mais grosso para 16-48 px
    def icone(n, fundo=None, margem=.06):
        ic = Image.new("RGBA", (n, n), (fundo + (255,)) if fundo else (0, 0, 0, 0))
        l = (grossa if n <= 64 else letra).copy(); m = int(n * (1 - 2 * margem)); l.thumbnail((m, m), Image.LANCZOS)
        ic.alpha_composite(l, ((n - l.width) // 2, (n - l.height) // 2))
        return ic
    icone(192).save(IMG / "favicon-192.png")
    icone(32, margem=.02).save(IMG / "favicon-32.png")
    icone(48, margem=.02).save(RAIZ / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    icone(180, AREIA, .16).convert("RGB").save(IMG / "apple-touch-icon.png")  # iOS não aceita transparência

    # og 1200x630
    og = Image.new("RGBA", (1200, 630), AREIA + (255,))
    l = tingir(logo, CAFE); l.thumbnail((900, 330))
    og.alpha_composite(l, ((1200 - l.width) // 2, 150))
    d = ImageDraw.Draw(og)
    try: f = ImageFont.truetype("arial.ttf", 26)
    except OSError: f = ImageFont.load_default()
    txt = "FINE LINE  ✦  ORNAMENTAL  ✦  DIADEMA - SP"
    txt = txt.replace("✦", "·")
    w = d.textlength(txt, font=f)
    d.text(((1200 - w) / 2, 520), txt, fill=CAFE, font=f)
    og.convert("RGB").save(IMG / "og.jpg", quality=88)

    # foto dela para a abertura (zip do cliente, 1080x1080) recortada em 3:4
    q = Image.open(REF / "zip" / "Agatha" / "Agatha.jpg").convert("RGB").crop((140, 0, 950, 1080))
    q.save(IMG / "agatha.webp", quality=86, method=6)
    print("ok")

if __name__ == "__main__":
    main()
