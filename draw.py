#!/usr/bin/env python3
"""news-23 b93 front-page-dense: THE WORLD TODAY, Monday 23 November 2026 (31 stories).
Draws entry.png 1024x1024 with PIL. All facts from the brief; no invented numbers.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(d, text, fnt, maxw):
    """Greedy wrap into lines <= maxw px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(d, text, fnt, maxw, max_lines):
    """Wrap, shrinking font until it fits in max_lines (min size 9)."""
    size = fnt.size
    while size > 9:
        f = font(FB, size)
        ls = wrap(d, text, f, maxw)
        if len(ls) <= max_lines:
            return ls, f
        size -= 1
    return wrap(d, text, font(FB, 9), maxw), font(FB, 9)

def chip(d, x, y, text, fill):
    """Small rounded chip; returns right edge."""
    f = font(FB, 9)
    tw = d.textlength(text, font=f)
    w = int(tw) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=fill)
    d.text((x + 5, y + 2), text, font=f, fill="white")
    return x + w

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 56], fill="black")
d.text((16, 7), "THE WORLD TODAY", font=font(FB, 40), fill="white")
d.text((1008, 19), "MONDAY 23 NOVEMBER 2026", font=font(FB, 17), fill="#e8b800", anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 56, W, 78], fill="#b30000")
d.text((512, 61), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       font=font(FB, 15), fill="white", anchor="ma")

# ---------- number strip: 5 cols x 2 rows ----------
NUMBERS = [
    ("-3.3%", "KOSPI", "#b30000"), ("5.3", "US-CHINA POWER GAP", "#1a2a6b"),
    ("11,762", "EBOLA CASES, DRC", "#1a2a6b"), ("10T won", "SEOUL STABILISATION FUND", "#8a6d00"),
    ("2%", "BILLIONAIRE TAX IN PARIS", "#1a2a6b"),
    ("$450M", "SKUBAL DEAL", "#1a2a6b"), ("165", "RUSSIAN MISSILES/WEEK", "#b30000"),
    ("12,000", "CLEARED IN MANCHESTER", "#1a2a6b"), ("264 kg", "EXPLOSIVES SEIZED", "#1a2a6b"),
    ("$107.3B", "ANTHROPIC IPO", "#1a7a2e"),
]
d.rectangle([0, 78, W, 150], fill="#f4f1e8")
for i, (num, lab, col) in enumerate(NUMBERS):
    cx = (i % 5) * 205 + 8
    ry = 82 if i < 5 else 118
    d.text((cx, ry), num, font=font(FB, 19), fill=col)
    d.text((cx, ry + 20), lab, font=font(FB, 9), fill="#333333")

# ---------- region bar ----------
REGIONS = [("ASIA-PACIFIC 7", 220, "#1a2a6b"), ("AMERICAS 8", 220, "#b30000"),
           ("MIDDLE EAST 6", 190, "#8a6d00"), ("EUROPE 5", 160, "#1a7a6b"),
           ("AFRICA 3", 120, "#6b3a8a"), ("WORLD 2", 114, "#555555")]
x = 0
for name, wdt, col in REGIONS:
    d.rectangle([x, 150, x + wdt, 170], fill=col)
    d.text((x + wdt / 2, 155), name, font=font(FB, 13), fill="white", anchor="ma")
    x += wdt

# ---------- UTC strip ----------
d.rectangle([0, 170, W, 186], fill="#e8e8e8")
d.text((8, 174), "THE DAY IN UTC  \u00b7  ~00:00 Kospi dives  \u00b7  ~06:30 Guterres opens  \u00b7  ~09:00 Power Index  \u00b7  ~12:00 Paris 2% tax  \u00b7  ~15:00 Kyiv missiles",
       font=font(FR, 11), fill="#333333")
d.text((1016, 174), "~ APPROX", font=font(FR, 11), fill="#666666", anchor="ra")

# ---------- hero scenes ----------
HX = [8, 348, 684]          # hero column x
HW = 332                    # hero column width
SY, SH = 186, 96            # scene y / height

# --- scene 1: Kospi skyline + chart ---
sx = HX[0]
d.rectangle([sx, SY, sx + HW, SY + SH], fill="#0d1b3d")
import random
random.seed(93)
bx = sx + 6
while bx < sx + HW - 30:
    bw = random.randint(22, 38)
    bh = random.randint(28, 62)
    d.rectangle([bx, SY + SH - bh, bx + bw, SY + SH], fill="#16294f")
    for wy in range(SY + SH - bh + 5, SY + SH - 4, 9):
        for wx in range(bx + 4, bx + bw - 4, 9):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill="#ffd94d")
    bx += bw + 3
pts = [(sx + 12, SY + 62), (sx + 60, SY + 44), (sx + 110, SY + 55), (sx + 160, SY + 34),
       (sx + 210, SY + 42), (sx + 265, SY + 22), (sx + 318, SY + 30)]
d.line(pts, fill="#ff7f2a", width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill="white", outline="#ff7f2a", width=2)
d.text((sx + 10, SY + 6), "-3.3%", font=font(FB, 26), fill="white")
d.rectangle([sx, SY + SH - 16, sx + HW, SY + SH], fill="black")
d.text((sx + 8, SY + SH - 14), "KOSPI 4,708.54   \u00b7   -161 PTS", font=font(FB, 10), fill="white")

# --- scene 2: Guterres ---
sx = HX[1]
d.rectangle([sx, SY, sx + HW, SY + SH], fill="#0d6b2f")
d.text((sx + 10, SY + 4), "150 DELEGATES", font=font(FB, 20), fill="#ffd94d")
d.text((sx + 10, SY + 28), "BACK A RISK", font=font(FB, 20), fill="#ffd94d")
d.text((sx + 10, SY + 52), "FRAMEWORK", font=font(FB, 20), fill="#ffd94d")
cx, cy, r = sx + HW - 52, SY + 40, 30
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#bfe3c8", outline="white", width=2)
d.ellipse([cx - 12, cy - r, cx + 12, cy + r], outline="#0d6b2f", width=1)
d.line([cx - r, cy, cx + r, cy], fill="#0d6b2f", width=1)
d.arc([cx - r, cy - 14, cx + r, cy + 14], 0, 360, fill="#0d6b2f", width=1)
d.rectangle([sx, SY + SH - 16, sx + HW, SY + SH], fill="black")
d.text((sx + 8, SY + SH - 14), "UN  \u00b7  BRIDGETOWN", font=font(FB, 10), fill="white")

# --- scene 3: Power Index bars ---
sx = HX[2]
d.rectangle([sx, SY, sx + HW, SY + SH], fill="#f4f1e8")
d.text((sx + 8, SY + 4), "NARROWEST SINCE 2018", font=font(FB, 11), fill="#333333")
d.text((sx + HW - 8, SY + 4), "GAP 5.3", font=font(FB, 11), fill="#b30000", anchor="ra")
bars = [("78.9", "US", 0.789, "#1a2a6b"), ("73.6", "CHINA", 0.736, "#b30000"), ("40.5", "INDIA", 0.405, "#c99300")]
by = SY + 22
for val, name, frac, col in bars:
    bw = int((HW - 16) * frac)
    d.rectangle([sx + 8, by, sx + 8 + bw, by + 13], fill=col)
    vcol = "#333333" if name == "INDIA" else "white"
    d.text((sx + 8 + bw / 2, by + 1), val, font=font(FB, 10), fill=vcol, anchor="ma")
    d.text((sx + 8 + bw + 5, by + 1), name, font=font(FB, 10), fill="#333333")
    by += 17
d.rectangle([sx, SY + SH - 16, sx + HW, SY + SH], fill="black")
d.text((sx + 8, SY + SH - 14), "ASIA POWER INDEX 2026", font=font(FB, 10), fill="white")

# ---------- hero headlines / bodies / sources ----------
HEROES = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (head, body, src) in enumerate(HEROES):
    hx = HX[i]
    lines, hf = fit_lines(d, head, font(FB, 21), HW - 4, 2)
    hy = 290
    for ln in lines:
        d.text((hx, hy), ln, font=hf, fill="black")
        hy += hf.size + 3
    blines = wrap(d, body, font(FR, 12), HW - 4)[:2]
    byy = 352
    for ln in blines:
        d.text((hx, byy), ln, font=font(FR, 12), fill="#222222")
        byy += 15
    d.text((hx, 388), src, font=font(FR, 10), fill="#666666")
    chip(d, hx + HW - 62, 386, "REPORTED", "#1a5fb4")

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 410, W, 432], fill="black")
d.text((8, 415), "MORE OF THE DAY  \u2014  10 STORIES", font=font(FB, 14), fill="white")

# ---------- cards ----------
CARDS = [
    ("AMERICAS", "#1a2a6b", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", "#444444", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", "#8a6d00", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", "#1a7a6b", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", "#b30000", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", "#b30000", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", "#6b3a8a", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", "#1a5fb4", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", "#1a7a6b", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", "#444444", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
for i, (cat, col, head, body, src, kind) in enumerate(CARDS):
    cx = 8 + (i % 5) * 204
    cy = 438 if i < 5 else 524
    d.rectangle([cx, cy, cx + 196, cy + 78], outline="#cccccc", width=1)
    d.rectangle([cx, cy, cx + 196, cy + 15], fill=col)
    d.text((cx + 5, cy + 2), cat, font=font(FB, 9), fill="white")
    d.text((cx + 191, cy + 2), str(i + 1), font=font(FB, 9), fill="white", anchor="ra")
    hlines, hf = fit_lines(d, head, font(FB, 12), 186, 2)
    hy = cy + 19
    for ln in hlines:
        d.text((cx + 5, hy), ln, font=hf, fill="black")
        hy += hf.size + 2
    d.text((cx + 5, cy + 49), body, font=font(FR, 10), fill="#333333")
    d.text((cx + 5, cy + 64), src, font=font(FR, 9), fill="#666666")
    chip(d, cx + 196 - 62, cy + 63, kind, "#1a5fb4" if kind == "REPORTED" else "#b30000")

# ---------- WHERE IT HAPPENED / ALSO strip ----------
d.rectangle([0, 610, W, 632], fill="black")
d.text((8, 615), "WHERE IT HAPPENED", font=font(FB, 14), fill="white")
d.text((360, 615), "ALSO ON MONDAY", font=font(FB, 14), fill="white")

# ---------- map ----------
MX, MY, MW, MH = 8, 638, 336, 190
d.rectangle([MX, MY, MX + MW, MY + MH], outline="#999999", width=1, fill="#f7f7f2")
d.polygon([(28, 652), (95, 648), (140, 662), (150, 700), (128, 724), (92, 722), (55, 700), (22, 680)],
          fill="#cfe3b8", outline="#9dbb7a")
d.polygon([(70, 726), (118, 726), (128, 758), (108, 800), (82, 812), (62, 782), (58, 748)],
          fill="#cfe3b8", outline="#9dbb7a")
d.polygon([(185, 652), (228, 650), (238, 672), (218, 690), (190, 686), (178, 668)],
          fill="#cfe3b8", outline="#9dbb7a")
d.polygon([(186, 694), (238, 694), (246, 730), (228, 786), (200, 792), (182, 750), (180, 712)],
          fill="#cfe3b8", outline="#9dbb7a")
d.polygon([(252, 652), (330, 652), (336, 700), (312, 748), (272, 756), (248, 716), (246, 676)],
          fill="#cfe3b8", outline="#9dbb7a")
d.polygon([(292, 786), (326, 784), (332, 800), (306, 810), (288, 800)],
          fill="#cfe3b8", outline="#9dbb7a")
PINS = [(312, 700, 1), (104, 720, 2), (296, 676, 3), (66, 682, 4), (92, 666, 5),
        (226, 662, 6), (88, 694, 7), (34, 698, 8), (52, 712, 9), (74, 718, 10),
        (206, 680, 11), (190, 660, 12), (258, 664, 13)]
for px, py, n in PINS:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill="#b30000", outline="white", width=1)
    d.text((px, py - 6), str(n), font=font(FB, 9), fill="white", anchor="ma")
d.rectangle([MX + 2, MY + MH - 34, MX + MW - 2, MY + MH - 2], fill="white")
d.text((MX + 6, MY + MH - 33), "Pins 1\u201313:  1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", font=font(FR, 9), fill="#444444")
d.text((MX + 6, MY + MH - 22), "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", font=font(FR, 9), fill="#444444")
d.text((MX + 6, MY + MH - 11), "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", font=font(FR, 9), fill="#444444")

# ---------- ALSO list: 2 cols x 9 rows ----------
ALSO = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after Antalya pact rejected",
    "18. Benghazi: UN demands probe of port attacks [CLAIM]", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
    "23. Lebanon seizes 264 kg explosives", "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones [CLAIM]", "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns", "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools", "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(ALSO):
    col = 0 if i < 9 else 1
    row = i % 9
    ax = 360 if col == 0 else 692
    ay = 642 + row * 21
    if "[CLAIM]" in item:
        base = item.replace(" [CLAIM]", "")
        d.text((ax, ay), base, font=font(FR, 11), fill="black")
        d.text((ax + d.textlength(base, font=font(FR, 11)) + 3, ay), "[CLAIM]", font=font(FB, 10), fill="#b30000")
    else:
        d.text((ax, ay), item, font=font(FR, 11), fill="black")

# ---------- DATE CHECK ----------
d.rectangle([8, 836, 1016, 902], outline="#b30000", width=2)
d.text((16, 842), "DATE CHECK", font=font(FB, 13), fill="#b30000")
d.text((1008, 843), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=font(FB, 9), fill="#b30000", anchor="ra")
d.text((16, 862), "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
       font=font(FR, 11), fill="black")
d.text((16, 882), "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
       font=font(FR, 11), fill="black")

# ---------- footer ----------
d.text((8, 910), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=font(FR, 10), fill="#555555")
d.text((8, 926), "CHIPS: REPORTED = confirmed by wires.  CLAIM = one side's claim, not independently confirmed.  ONGOING = still developing.",
       font=font(FR, 10), fill="#555555")
d.text((8, 942), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=font(FR, 10), fill="#555555")
d.line([8, 962, 1016, 962], fill="#c99300", width=2)
d.text((512, 972), "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
       font=font(FB, 13), fill="#8a6d00", anchor="ma")

img.save("entry.png")
print("saved entry.png", img.size)
