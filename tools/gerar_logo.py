"""Logo em tinta café e em branco (a partir do logo transparente dela), favicons com os raios do sol, og.jpg e foto.
Uso: python tools/gerar_logo.py"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[1]
REF = RAIZ.parent / "_ref"
IMG = RAIZ / "assets" / "img"
CAFE = (52, 40, 32)
AREIA = (244, 237, 228)
TAUPE = (185, 160, 136)

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

    # raios do sol (canto direito do logo) como ícone
    W, H = logo.size
    so_raios = logo.copy()
    ImageDraw.Draw(so_raios).rectangle((0, int(H * .5), int(W * .836), H), fill=(0, 0, 0, 0))
    raios = so_raios.crop((int(W * .74), 0, W, int(H * .80)))
    raios = raios.crop(raios.getchannel("A").getbbox())
    for n, fundo in [(512, TAUPE)]:
        ic = Image.new("RGBA", (n, n), fundo + (255,))
        r = tingir(raios, (255, 255, 255)); r.thumbnail((int(n * .62), int(n * .62)))
        ic.alpha_composite(r, ((n - r.width) // 2 + n // 20, (n - r.height) // 2 + n // 20))
        ic = ic.convert("RGB")
        ic.resize((192, 192), Image.LANCZOS).save(IMG / "favicon-192.png")
        ic.resize((180, 180), Image.LANCZOS).save(IMG / "apple-touch-icon.png")
        ic.resize((32, 32), Image.LANCZOS).save(IMG / "favicon-32.png")
        ic.save(RAIZ / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

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

    # foto dela, recortada do post "Quem sou eu" (provisória, CONFIRMAR uma foto boa)
    q = Image.open(REF / "ig" / "quem-sou.jpg").convert("RGB").crop((236, 250, 444, 510))
    q.resize((416, 520), Image.LANCZOS).save(IMG / "agatha.webp", quality=86)
    print("ok")

if __name__ == "__main__":
    main()
