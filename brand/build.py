# Brand asset generator: writes SVG logos and HTML sources for PNG/PDF rendering.
import os
NAVY, NAVY2, GOLD, CORAL, PAPER, MIST, SKY = "#0B1640", "#14246B", "#FFC93C", "#FF6B5B", "#F6F4EE", "#B9C3EC", "#E8ECFA"

def mark(page=NAVY, spark=CORAL, bg=None, size=120):
    r = f'<rect width="120" height="120" rx="30" fill="{bg}"/>' if bg else ""
    dy = 4
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 120 120">{r}'
            f'<g transform="translate(0 {dy})">'
            f'<path d="M57 92 C46 85 33 83 20 85 L20 47 C33 45 46 47 57 55 Z" fill="{page}"/>'
            f'<path d="M63 92 C74 85 87 83 100 85 L100 47 C87 45 74 47 63 55 Z" fill="{page}"/>'
            f'<path d="M60 12 C61.6 23 64.6 26.4 76 28 C64.6 29.6 61.6 33 60 44 C58.4 33 55.4 29.6 44 28 C55.4 26.4 58.4 23 60 12Z" fill="{spark}"/>'
            f'</g></svg>')

def spark(color, size):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><path d="M50 0 C53 35 65 47 100 50 C65 53 53 65 50 100 C47 65 35 53 0 50 C35 47 47 35 50 0Z" fill="{color}"/></svg>')

def lockup(dark=False, scale=1.0):
    ink = "#FFFFFF" if dark else NAVY
    sub = GOLD if dark else CORAL
    m = mark(GOLD, CORAL, None) if dark else mark(NAVY, CORAL)
    s = scale
    return (f'<div class="lockup" style="display:inline-flex;align-items:center;gap:{18*s}px">'
            f'<div style="width:{132*s}px;height:{132*s}px;margin:{-10*s}px {-6*s}px {-10*s}px {-14*s}px">{m.replace(chr(39)+"120"+chr(39),"100%")}</div>'
            f'<div style="display:flex;flex-direction:column;line-height:1">'
            f'<div style="font-family:Inter Display;font-weight:900;font-size:{64*s}px;letter-spacing:-.02em;color:{ink}">AI Багш</div>'
            f'<div style="font-family:Inter;font-weight:700;font-size:{19*s}px;letter-spacing:.42em;color:{sub};margin-top:{9*s}px;padding-left:{3*s}px">АКАДЕМИ</div>'
            f'</div></div>')

BASE = """<!doctype html><html lang="mn"><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif;color:%s}
svg{display:block;width:100%%;height:100%%}
.lockup svg{width:100%%;height:100%%}
</style></head><body>""" % NAVY

def write(name, body, w, h, extra_css=""):
    with open(name, "w") as f:
        f.write(BASE.replace("</style>", f"html,body{{width:{w}px;height:{h}px;overflow:hidden}}{extra_css}</style>") + body + "</body></html>")

os.makedirs("src", exist_ok=True)
# --- SVG logo files
open("logo-mark.svg","w").write(mark(NAVY, CORAL))
open("logo-mark-white.svg","w").write(mark("#FFFFFF", CORAL))
open("logo-app-icon.svg","w").write(mark(GOLD, CORAL, NAVY))

# --- Logo PNG sources
write("src/logo-light.html", f'<div style="width:1200px;height:500px;background:{PAPER};display:grid;place-items:center">{lockup(False,1.6)}</div>', 1200, 500)
write("src/logo-dark.html",  f'<div style="width:1200px;height:500px;background:{NAVY};display:grid;place-items:center">{lockup(True,1.6)}</div>', 1200, 500)

# --- Facebook profile (mark only, circle-safe)
write("src/fb-profile.html",
      f'<div style="width:1080px;height:1080px;background:{NAVY};display:grid;place-items:center;position:relative">'
      f'<div style="position:absolute;inset:0;background:radial-gradient(520px 520px at 50% 50%,#1A2C78,transparent 72%)"></div>'
      f'<div style="width:900px;height:900px;position:relative">{mark(GOLD, CORAL)}</div></div>', 1080, 1080)

# --- Facebook cover (brand, not promo). Safe centre 1109px for mobile.
cover_pattern = "".join(
    f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:{o}">{spark(c, s)}</div>'
    for x,y,s,c,o in [(1185,70,120,GOLD,1),(1300,250,64,CORAL,1),(1130,330,40,"#FFFFFF",.5),(1420,110,36,"#FFFFFF",.35),(1460,400,90,"#FFFFFF",.14),(70,420,60,"#FFFFFF",.12),(190,80,30,"#FFFFFF",.25)])
write("src/fb-cover.html",
      f'<div style="width:1640px;height:624px;background:{NAVY};position:relative;overflow:hidden">'
      f'<div style="position:absolute;inset:0;background:radial-gradient(700px 520px at 82% 40%,{NAVY2},transparent 70%)"></div>'
      f'<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.10) 1.4px,transparent 1.5px);background-size:30px 30px;'
      f'mask-image:linear-gradient(90deg,transparent 10%,#000 60%);-webkit-mask-image:linear-gradient(90deg,transparent 10%,#000 60%)"></div>'
      f'{cover_pattern}'
      f'<div style="position:absolute;left:300px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center">'
      f'{lockup(True,1.25)}'
      f'<div style="font-family:Inter Display;font-weight:800;font-size:46px;letter-spacing:-.015em;color:#fff;margin-top:44px;line-height:1.12">Ухаалаг багш —<br><span style="color:{GOLD}">ирээдүйн анги.</span></div>'
      f'<div style="font-size:21px;color:{MIST};margin-top:18px">Монгол багш нарт зориулсан AI сургалт</div>'
      f'</div></div>', 1640, 624)

# --- Brand guide (16:9 pages)
W,H = 1600, 900
def page(inner, bg=PAPER, color=NAVY, num=None, title=None):
    head = (f'<div style="position:absolute;left:90px;top:64px;right:90px;display:flex;justify-content:space-between;font-size:15px;font-weight:700;letter-spacing:.14em;opacity:.6">'
            f'<span>AI БАГШ АКАДЕМИ · БРЭНДИЙН ГАРЫН АВЛАГА</span><span>{num or ""}</span></div>') if num else ""
    t = f'<h2 style="font-family:Inter Display;font-weight:900;font-size:56px;letter-spacing:-.02em;margin-bottom:46px">{title}</h2>' if title else ""
    return (f'<section style="width:{W}px;height:{H}px;background:{bg};color:{color};position:relative;overflow:hidden;page-break-after:always">'
            f'{head}<div style="position:absolute;left:90px;right:90px;top:140px;bottom:70px">{t}{inner}</div></section>')

def swatch(name, hexv, role, fg="#fff", border=False):
    b = "border:2px solid #E2E0D8;" if border else ""
    return (f'<div style="flex:1;border-radius:22px;overflow:hidden;background:#fff;box-shadow:0 2px 0 rgba(11,22,64,.06)">'
            f'<div style="height:250px;background:{hexv};{b}border-radius:22px 22px 0 0;padding:22px;color:{fg};font-family:Inter Display;font-weight:900;font-size:30px;display:flex;align-items:flex-end">{name}</div>'
            f'<div style="padding:18px 22px;font-size:17px;line-height:1.5"><b style="font-size:19px">{hexv}</b><br><span style="opacity:.7">{role}</span></div></div>')

pages = []
# 1 Cover
pages.append(page(
    f'<div style="position:absolute;inset:-140px -90px -70px -90px;padding:90px;display:flex;flex-direction:column;justify-content:center">'
    f'{lockup(True,1.6)}'
    f'<div style="font-family:Inter Display;font-weight:900;font-size:84px;letter-spacing:-.025em;color:#fff;margin-top:70px;line-height:1.02">Брэндийн<br><span style="color:{GOLD}">гарын авлага</span></div>'
    f'<div style="font-size:22px;color:{MIST};margin-top:26px">Хувилбар 1.0 · 2026</div></div>'
    f'<div style="position:absolute;right:-20px;top:40px;width:520px;height:520px;opacity:.95">{spark(GOLD,520)}</div>'
    f'<div style="position:absolute;right:400px;top:460px;width:120px;height:120px">{spark(CORAL,120)}</div>',
    bg=NAVY, color="#fff"))
# 2 Brand idea
pages.append(page(
    f'<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:70px;align-items:start">'
    f'<div><div style="font-family:Inter Display;font-weight:900;font-size:64px;line-height:1.05;letter-spacing:-.02em">Ухаалаг багш —<br><span style="color:{CORAL}">ирээдүйн анги.</span></div>'
    f'<p style="font-size:24px;line-height:1.55;margin-top:34px;opacity:.85">AI Багш Академи нь Монгол багш нарт AI-г өдөр тутмын ажилдаа зөв, ёс зүйтэй, үр дүнтэй ашиглахад тусалдаг. Технологи бол хэрэгсэл — гол нь багш хэвээр.</p></div>'
    f'<div style="display:flex;flex-direction:column;gap:18px">'
    + "".join(f'<div style="background:#fff;border-radius:20px;padding:24px 28px"><div style="font-family:Inter Display;font-weight:900;font-size:26px;color:{c}">{h}</div><div style="font-size:19px;margin-top:6px;opacity:.8;line-height:1.45">{d}</div></div>'
              for h,d,c in [("Эрхэм зорилго","Багш бүрийг AI-г итгэлтэй ашигладаг болгох.",NAVY),
                            ("Амлалт","Цагаа хэмнэ. Хичээлээ сайжруул.",CORAL),
                            ("Үнэт зүйл","Практик · Хүртээмжтэй · Ёс зүйтэй · Монгол хэл дээр",NAVY)])
    + '</div></div>', num="01", title="Брэндийн санаа"))
# 3 Logo
pages.append(page(
    f'<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:40px">'
    f'<div style="background:#fff;border-radius:26px;height:330px;display:grid;place-items:center">{lockup(False,1.3)}</div>'
    f'<div style="background:{NAVY};border-radius:26px;height:330px;display:grid;place-items:center">{lockup(True,1.0)}</div>'
    f'</div>'
    f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1.6fr;gap:40px;margin-top:40px;align-items:center">'
    f'<div style="background:#fff;border-radius:26px;height:210px;display:grid;place-items:center"><div style="width:140px;height:140px">{mark(NAVY,CORAL)}</div></div>'
    f'<div style="background:{GOLD};border-radius:26px;height:210px;display:grid;place-items:center"><div style="width:140px;height:140px">{mark(NAVY,"#FFFFFF")}</div></div>'
    f'<div style="border-radius:26px;height:210px;display:grid;place-items:center"><div style="width:180px;height:180px">{mark(GOLD,CORAL,NAVY)}</div></div>'
    f'<div style="font-size:20px;line-height:1.55"><b style="font-family:Inter Display;font-size:26px">Тэмдгийн утга</b><br>'
    f'<b>Нээлттэй ном</b> — мэдлэг, багшийн мэргэжил.<br><b>Од (spark)</b> — AI, шинэ санаа, гэрэлтэх агшин.<br>Хамтдаа: <i>AI-аар гэрэлтсэн мэдлэг.</i></div>'
    f'</div>', num="02", title="Лого"))
# 4 Logo rules
def dont(label, inner):
    return (f'<div><div style="background:#fff;border-radius:20px;height:190px;display:grid;place-items:center;position:relative;overflow:hidden">{inner}'
            f'<div style="position:absolute;top:14px;right:14px;width:34px;height:34px;border-radius:50%;background:{CORAL};color:#fff;display:grid;place-items:center;font-weight:900;font-size:22px">✕</div></div>'
            f'<div style="font-size:17px;margin-top:12px;font-weight:600">{label}</div></div>')
pages.append(page(
    f'<div style="display:grid;grid-template-columns:1fr 1.4fr;gap:60px">'
    f'<div><div style="background:#fff;border-radius:26px;height:300px;display:grid;place-items:center;position:relative">'
    f'<div style="outline:2px dashed {CORAL};outline-offset:34px">{lockup(False,0.9)}</div></div>'
    f'<p style="font-size:19px;line-height:1.55;margin-top:22px"><b>Хамгаалалтын зай:</b> логоны эргэн тойронд тэмдгийн өндрийн ⅓-ээс багагүй хоосон зай үлдээнэ.<br>'
    f'<b>Хамгийн бага хэмжээ:</b> хэвтээ лого 120px / 30мм, тэмдэг 24px / 8мм.</p></div>'
    f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px">'
    + dont("Сунгаж, хавчихгүй", f'<div style="transform:scaleX(1.5)">{lockup(False,0.5)}</div>')
    + dont("Өнгийг өөрчлөхгүй", f'<div style="filter:hue-rotate(140deg)">{lockup(False,0.5)}</div>')
    + dont("Эргүүлэхгүй", f'<div style="transform:rotate(-14deg)">{lockup(False,0.5)}</div>')
    + dont("Сүүдэр, эффект нэмэхгүй", f'<div style="filter:drop-shadow(6px 6px 0 #999)">{lockup(False,0.5)}</div>')
    + dont("Бараан бүдэг дэвсгэр дээр бараан лого", f'<div style="background:#2A3366;padding:24px 20px;border-radius:12px">{lockup(False,0.5)}</div>')
    + dont("Бүрэлдэхүүнийг салгаж зөөхгүй", f'<div style="display:flex;align-items:flex-end;gap:40px"><div style="width:44px;height:44px">{mark()}</div><div style="font-family:Inter Display;font-weight:900;font-size:30px">AI Багш</div></div>')
    + '</div></div>', num="03", title="Логоны хэрэглээ"))
# 5 Colours
pages.append(page(
    f'<div style="display:flex;gap:24px">'
    + swatch("Шөнийн хөх", NAVY, "Үндсэн өнгө · дэвсгэр, текст · 60%")
    + swatch("Алтан шар", GOLD, "Онцлох өнгө · гол үг, товч · 20%", fg=NAVY)
    + swatch("Шүрэн улаан", CORAL, "Эрч хүч · од, шошго · 10%")
    + swatch("Цаасан цагаан", PAPER, "Цайвар дэвсгэр · 10%", fg=NAVY, border=True)
    + swatch("Манан хөх", MIST, "Туслах текст бараан дэвсгэр дээр", fg=NAVY)
    + '</div>'
    f'<p style="font-size:19px;margin-top:34px;line-height:1.55;opacity:.85">Хослол: Шөнийн хөх дэвсгэр + цагаан текст + алтан шар онцлол — бүх сошиал контентын үндсэн хэв маяг. Шүрэн улааныг зөвхөн жижиг онцлолд хэрэглэнэ.</p>',
    num="04", title="Өнгө"))
# 6 Typography
pages.append(page(
    f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:60px">'
    f'<div style="background:#fff;border-radius:26px;padding:40px">'
    f'<div style="font-size:17px;font-weight:700;letter-spacing:.12em;color:{CORAL}">ГАРЧИГ</div>'
    f'<div style="font-family:Inter Display;font-weight:900;font-size:120px;letter-spacing:-.03em;line-height:1">Аа Өө Үү</div>'
    f'<div style="font-size:22px;margin-top:18px"><b>Inter Display</b> — Black 900 / ExtraBold 800</div>'
    f'<div style="font-size:18px;opacity:.7;margin-top:8px;line-height:1.5">Монгол кирилл (Ө, Ү) бүрэн дэмждэг, үнэгүй (Google Fonts).</div></div>'
    f'<div style="background:#fff;border-radius:26px;padding:40px">'
    f'<div style="font-size:17px;font-weight:700;letter-spacing:.12em;color:{CORAL}">ҮНДСЭН ТЕКСТ</div>'
    f'<div style="font-weight:500;font-size:120px;letter-spacing:-.02em;line-height:1">Аа Өө Үү</div>'
    f'<div style="font-size:22px;margin-top:18px"><b>Inter</b> — Regular 400 / SemiBold 600 / Bold 700</div>'
    f'<div style="font-size:18px;opacity:.7;margin-top:8px;line-height:1.5">Мөр хоорондын зай 1.4–1.6. Гарчиг текстийн 2.5–4 дахин том.</div></div>'
    f'</div>'
    f'<div style="display:flex;gap:40px;align-items:baseline;margin-top:40px">'
    f'<span style="font-family:Inter Display;font-weight:900;font-size:56px;letter-spacing:-.02em">Хичээлээ 20 минутад бэлтгэе!</span>'
    f'<span style="font-size:20px;opacity:.7">H1 · 56–90px</span></div>',
    num="05", title="Үсгийн хэв"))
# 7 Graphic elements & voice
pages.append(page(
    f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:60px">'
    f'<div><div style="background:{NAVY};border-radius:26px;height:330px;position:relative;overflow:hidden">'
    f'<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.14) 1.6px,transparent 1.7px);background-size:28px 28px"></div>'
    f'<div style="position:absolute;left:60px;top:60px;width:150px;height:150px">{spark(GOLD,150)}</div>'
    f'<div style="position:absolute;left:250px;top:170px;width:70px;height:70px">{spark(CORAL,70)}</div>'
    f'<div style="position:absolute;left:380px;top:80px;width:44px;height:44px;opacity:.6">{spark("#fff",44)}</div>'
    f'<div style="position:absolute;right:40px;bottom:40px;background:#fff;color:{NAVY};border-radius:18px 18px 18px 6px;padding:14px 18px;font-size:18px;font-weight:600">Чат хэлбэрийн карт</div>'
    f'<div style="position:absolute;right:40px;top:40px;background:{GOLD};color:{NAVY};border-radius:999px;padding:10px 18px;font-size:17px;font-weight:800">Дугуй шошго</div></div>'
    f'<p style="font-size:19px;line-height:1.55;margin-top:20px"><b>Од</b> — AI-гийн бэлгэдэл, онцлох газарт. <b>Цэгэн тор</b> — бараан дэвсгэрийн бүтэц. <b>Чатын карт</b> — AI-тай харилцааг харуулах. Булангийн радиус 20–28px.</p></div>'
    f'<div><div style="font-family:Inter Display;font-weight:900;font-size:30px;margin-bottom:18px">Брэндийн дуу хоолой</div>'
    + "".join(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px"><div style="background:#E6F6EE;border-radius:16px;padding:16px 18px;font-size:18px;line-height:1.4"><b style="color:#0E7A49">✓</b> {a}</div><div style="background:#FDECEA;border-radius:16px;padding:16px 18px;font-size:18px;line-height:1.4"><b style="color:{CORAL}">✕</b> {b}</div></div>'
              for a,b in [("Найрсаг, хүндэтгэлтэй: “Багшаа, хамтдаа туршъя.”","Албан хатуу: “Та заавал бүртгүүлэх шаардлагатай.”"),
                          ("Жишээгээр: “Энэ prompt-оор 5 минутад тест гаргана.”","Хийсвэр: “AI нь боловсролын хувьсгал юм.”"),
                          ("Энгийн үг: “AI туслах”","Мэргэжлийн хэллэг: “LLM-д суурилсан систем”"),
                          ("Багшийг гол дүр болгох","AI-г багшийг орлоно гэж хэлэх")])
    + '</div></div>', num="06", title="График элемент ба дуу хоолой"))
write("src/brand-guide.html", "".join(pages), W, H*len(pages), "@page{size:1600px 900px;margin:0}html,body{height:auto!important;overflow:visible!important}")
print("pages", len(pages))
