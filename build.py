"""產生 Hibbeler 9-34 解題頁 index.html（含手繪 SVG 示意圖）。"""
from pathlib import Path

# ---------- 立體示意圖的投影 ----------
OX, OY = 70, 300          # 自由端前下角在畫布上的位置
U = (0.80, -0.60)         # 沿梁軸（朝牆）的畫面方向
W = (1.00, 0.20)          # 沿寬度（朝 A 側）的畫面方向
SA, SC = 0.19, 0.62       # 軸向 px/mm、斷面 px/mm（斷面放大）


def P(s, w, h):
    return (OX + s * SA * U[0] + w * SC * W[0],
            OY + s * SA * U[1] + w * SC * W[1] - h * SC)


def poly(pts, cls):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{d}" class="{cls}"/>'


def line(a, b, cls, extra=""):
    return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" '
            f'y2="{b[1]:.1f}" class="{cls}" {extra}/>')


def text(p, s, cls="lbl", dx=0, dy=0, anchor="start"):
    return (f'<text x="{p[0]+dx:.1f}" y="{p[1]+dy:.1f}" class="{cls}" '
            f'text-anchor="{anchor}">{s}</text>')


def beam_svg():
    L, B_, H = 2000, 120, 150
    o = []
    o.append(poly([P(0, 0, H), P(L, 0, H), P(L, B_, H), P(0, B_, H)], "f-top"))
    o.append(poly([P(0, B_, 0), P(L, B_, 0), P(L, B_, H), P(0, B_, H)], "f-side"))
    o.append(poly([P(0, 0, 0), P(0, B_, 0), P(0, B_, H), P(0, 0, H)], "f-end"))
    # 牆
    wall = [P(L, -40, -40), P(L, B_ + 40, -40), P(L, B_ + 40, H + 40), P(L, -40, H + 40)]
    o.insert(0, poly(wall, "f-wall"))
    # 截面（虛線）
    s = 1200
    o.append(poly([P(s, 0, 0), P(s, B_, 0), P(s, B_, H), P(s, 0, H)], "sec"))
    # A、B
    A = P(s, B_, H - 30)
    Bp = P(s, 40, H)
    o.append(f'<circle cx="{A[0]:.1f}" cy="{A[1]:.1f}" r="4.5" class="pt"/>')
    o.append(f'<circle cx="{Bp[0]:.1f}" cy="{Bp[1]:.1f}" r="4.5" class="pt"/>')
    o.append(text(A, "A", "lbl b", dx=9, dy=6))
    o.append(text(Bp, "B", "lbl b", dx=-6, dy=-10, anchor="end"))
    # 載重：自由端形心，向下 4、朝 A 側 3
    c = P(0, 60, 75)
    k = 20
    end = (c[0] + 3 * k * W[0], c[1] + 3 * k * W[1] + 4 * k)
    o.append(line(c, end, "load", 'marker-end="url(#ahL)"'))
    o.append(line(c, (c[0], c[1] + 4 * k), "comp"))
    o.append(line((c[0], c[1] + 4 * k), end, "comp"))
    o.append(text(end, "15 kN", "lbl load-t", dx=6, dy=14))
    o.append(text((c[0], c[1] + 2 * k), "4", "lbl sm", dx=-10, dy=4, anchor="end"))
    o.append(text(((c[0] + end[0]) / 2, c[1] + 4 * k), "3", "lbl sm", dx=0, dy=22))
    # 尺寸
    m1 = P(0, B_ + 60, 0); m2 = P(s, B_ + 60, 0); m3 = P(L, B_ + 60, 0)
    o.append(line(m1, m2, "dim", 'marker-start="url(#tk)" marker-end="url(#tk)"'))
    o.append(line(m2, m3, "dim", 'marker-end="url(#tk)"'))
    o.append(text(((m1[0]+m2[0])/2, (m1[1]+m2[1])/2), "1200 mm", "lbl sm", dx=10, dy=16))
    o.append(text(((m2[0]+m3[0])/2, (m2[1]+m3[1])/2), "800 mm", "lbl sm", dx=10, dy=16))
    e1 = P(0, 0, H); e2 = P(0, B_, H)
    o.append(text(((e1[0]+e2[0])/2, e1[1]), "120", "lbl sm", dy=-10, anchor="middle"))
    o.append(text(P(0, 0, 75), "150", "lbl sm", dx=-8, dy=4, anchor="end"))
    # 座標軸
    g = (470, 320)
    ax = [((U[0]*55, U[1]*55), "x（朝牆）"), ((0, -55), "y（向上）"),
          ((W[0]*55, W[1]*55), "z（朝 A 側）")]
    for (dx, dy), lab in ax:
        e = (g[0] + dx, g[1] + dy)
        o.append(line(g, e, "axis", 'marker-end="url(#ahA)"'))
        o.append(text(e, lab, "lbl sm axis-t", dx=4, dy=-4 if dy < 0 else 14))
    return o


DEFS = """
<defs>
 <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>
 <marker id="ahL" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahL"/></marker>
 <marker id="ahA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahA"/></marker>
 <marker id="ahR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahR"/></marker>
 <marker id="tk" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M5,0 L5,10" class="tkm"/></marker>
</defs>"""


def svg(body, vb, label):
    return (f'<svg viewBox="{vb}" role="img" aria-label="{label}">{DEFS}'
            + "".join(body) + "</svg>")


# ---------- 斷面圖（從自由端看向牆）----------
def section_svg():
    s = 1.6                     # px/mm
    x0, y0 = 120, 40            # 斷面左上角
    w, h = 120 * s, 150 * s
    o = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="f-end"/>']
    # Q_A：A 以上 30 mm
    o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{30*s}" class="qa"/>')
    # Q_B：B 左側 40 mm
    o.append(f'<rect x="{x0}" y="{y0}" width="{40*s}" height="{h}" class="qb"/>')
    cx, cy = x0 + w / 2, y0 + h / 2
    o.append(line((x0 - 15, cy), (x0 + w + 15, cy), "na"))
    o.append(line((cx, y0 - 15), (cx, y0 + h + 15), "na"))
    o.append(text((x0 + w + 18, cy), "z", "lbl sm axis-t", dy=4))
    o.append(text((cx, y0 - 20), "y", "lbl sm axis-t", anchor="middle"))
    A = (x0 + w, y0 + 30 * s); B = (x0 + 40 * s, y0)
    for p, n, dx, dy in ((A, "A", 10, 5), (B, "B", 0, -10)):
        o.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="5" class="pt"/>')
        o.append(text(p, n, "lbl b", dx=dx, dy=dy, anchor="middle" if n == "B" else "start"))
    o.append(text((x0 + 70 * s, y0 + 15 * s + 5), "Q_A：120×30", "lbl sm qa-t", anchor="middle"))
    o.append(text((x0 + 20 * s, y0 + h - 40), "Q_B", "lbl sm qb-t", anchor="middle"))
    o.append(text((x0 + 20 * s, y0 + h - 22), "40×150", "lbl sm qb-t", anchor="middle"))
    # 尺寸
    o.append(text((x0 + w + 10, y0 + 15 * s), "30", "lbl sm", dy=4))
    o.append(text((x0 + 20 * s, y0 - 6), "40", "lbl sm", anchor="middle"))
    o.append(text((x0 + w / 2, y0 + h + 30), "120 mm", "lbl sm", anchor="middle"))
    o.append(text((x0 - 26, cy - 30), "150 mm", "lbl sm", anchor="end"))
    o.append(text((x0 + w + 18, cy + 40), "中性軸", "lbl xs mute"))
    o.append(text((x0 + w / 2, y0 + h + 52), "（從自由端看向牆，x 指入紙面）", "lbl xs mute", anchor="middle"))
    return o


# ---------- 自由端段的自由體圖 ----------
def fbd_svg():
    o = []
    x0, y0, L, H = 170, 80, 260, 70
    o.append(f'<rect x="{x0}" y="{y0}" width="{L}" height="{H}" class="f-side"/>')
    o.append(text((x0 + L / 2, y0 + H / 2 + 5), "自由端段（長 1.2 m）", "lbl sm mute", anchor="middle"))
    # 外力：左端
    c = (x0, y0 + H / 2)
    o.append(line(c, (c[0], c[1] + 70), "load", 'marker-end="url(#ahL)"'))
    o.append(text((c[0] - 6, c[1] + 70), "12 kN", "lbl sm load-t", anchor="end"))
    o.append(text((c[0] - 6, c[1] + 88), "（朝 A 側另有 9 kN）", "lbl xs load-t", anchor="end"))
    # 截面內力：右端 (+x 面)
    r = (x0 + L, y0 + H / 2)
    o.append(line((r[0], r[1] + 50), (r[0], r[1] - 50), "react", 'marker-end="url(#ahR)"'))
    o.append(text((r[0] + 8, r[1] - 40), "V_y = +12 kN", "lbl sm react-t"))
    o.append(text((r[0] + 8, r[1] - 18), "V_z = −9 kN（背離 A 側）", "lbl sm react-t"))
    o.append(text((r[0] + 8, r[1] + 8), "M_z = 14.4 kN·m", "lbl sm react-t"))
    o.append(text((r[0] + 8, r[1] + 30), "M_y = 10.8 kN·m", "lbl sm react-t"))
    o.append(text((r[0] - 4, y0 - 12), "+x 面（外法線朝牆）", "lbl xs mute", anchor="end"))
    # 小座標
    g = (x0 + 20, y0 + H + 70)
    o.append(line(g, (g[0] + 45, g[1]), "axis", 'marker-end="url(#ahA)"'))
    o.append(line(g, (g[0], g[1] - 45), "axis", 'marker-end="url(#ahA)"'))
    o.append(text((g[0] + 50, g[1] + 4), "x（朝牆）", "lbl xs axis-t"))
    o.append(text((g[0] + 6, g[1] - 40), "y", "lbl xs axis-t"))
    return o


# ---------- 應力元素 ----------
def element_svg(kind):
    o = []
    cx, cy, a = 170, 150, 90
    x0, y0 = cx - a / 2, cy - a / 2
    o.append(f'<rect x="{x0}" y="{y0}" width="{a}" height="{a}" class="elem"/>')
    gap, n = 8, 38
    def arr(p, q, cls="sig", mk="ah"):
        o.append(line(p, q, cls, f'marker-end="url(#{mk})"'))
    if kind == "A":
        # σx = −10.8 壓：左右兩面箭頭指向元素
        arr((x0 - gap - n, cy), (x0 - gap, cy))
        arr((x0 + a + gap + n, cy), (x0 + a + gap, cy))
        o.append(text((x0 + a + gap + n + 4, cy - 8), "10.8 MPa", "lbl sm"))
        # τxy = +0.640：右面向上、左面向下、上面向右、下面向左
        t = 6
        arr((x0 + a + t, cy + 30), (x0 + a + t, cy - 30), "tau", "ahR")
        arr((x0 - t, cy - 30), (x0 - t, cy + 30), "tau", "ahR")
        arr((cx - 30, y0 - t), (cx + 30, y0 - t), "tau", "ahR")
        arr((cx + 30, y0 + a + t), (cx - 30, y0 + a + t), "tau", "ahR")
        o.append(text((cx + 34, y0 - 12), "τ = 0.640 MPa", "lbl sm react-t"))
        h_lab, v_lab = "x（朝牆）", "y（向上）"
        note = "A 在側面：從 A 側（+z）往內看"
    else:
        # σx = 42.0 拉：上下兩面箭頭向外（x 畫成向上）
        arr((cx, y0 - gap), (cx, y0 - gap - n))
        arr((cx, y0 + a + gap), (cx, y0 + a + gap + n))
        o.append(text((cx + 8, y0 - gap - n + 4), "42.0 MPa", "lbl sm"))
        # τxz = −0.667：+x 面（上）朝 −z（左）；−x 面（下）朝右；+z 面（右）朝 −x（下）；−z 面（左）朝上
        t = 6
        arr((cx + 30, y0 - t), (cx - 30, y0 - t), "tau", "ahR")
        arr((cx - 30, y0 + a + t), (cx + 30, y0 + a + t), "tau", "ahR")
        arr((x0 + a + t, cy - 30), (x0 + a + t, cy + 30), "tau", "ahR")
        arr((x0 - t, cy + 30), (x0 - t, cy - 30), "tau", "ahR")
        o.append(text((x0 + a + 14, cy + 4), "τ = 0.667 MPa", "lbl sm react-t"))
        h_lab, v_lab = "z（朝 A 側）", "x（朝牆）"
        note = "B 在頂面：從上方（+y）往下看"
    g = (30, 285)
    o.append(line(g, (g[0] + 40, g[1]), "axis", 'marker-end="url(#ahA)"'))
    o.append(line(g, (g[0], g[1] - 40), "axis", 'marker-end="url(#ahA)"'))
    o.append(text((g[0] + 44, g[1] + 4), h_lab, "lbl xs axis-t"))
    o.append(text((g[0] + 6, g[1] - 36), v_lab, "lbl xs axis-t"))
    o.append(text((170, 22), note, "lbl xs mute", anchor="middle"))
    return o


# ---------- B 點莫爾圓：τ 正負號只影響方向，不影響主應力 ----------
def mohr_svg():
    o = []
    # 非比例尺：τ 以 8 MPa 繪製（實際 0.667 MPa），圓也依此重算，點才會落在圓上
    ox, oy, sx = 50, 160, 6.0
    te = 8.0
    c_val = 21.0; r_val = (21.0**2 + te**2) ** 0.5
    o.append(line((ox - 10, oy), (ox + 330, oy), "axis", 'marker-end="url(#ahA)"'))
    o.append(line((ox, oy - 150), (ox, oy + 150), "axis", 'marker-end="url(#ahA)"'))
    o.append(text((ox + 332, oy + 16), "σ", "lbl sm axis-t"))
    o.append(text((ox - 6, oy + 150), "τ（向下為正）", "lbl xs axis-t", anchor="end"))
    c = ox + c_val * sx; r = r_val * sx
    o.append(f'<circle cx="{c:.1f}" cy="{oy}" r="{r:.1f}" class="mohr"/>')
    X = (ox + 42 * sx, oy - te * sx)      # τ = −0.667 → 畫在上方
    Xw = (ox + 42 * sx, oy + te * sx)     # 若誤用 +0.667
    Z = (ox, oy + te * sx)
    o.append(line(X, Z, "dim"))
    o.append(f'<circle cx="{c:.1f}" cy="{oy}" r="3" class="pt2"/>')
    o.append(f'<circle cx="{X[0]:.1f}" cy="{X[1]:.1f}" r="5.5" class="pt"/>')
    o.append(text(X, "X（τ = −0.667，正確）", "lbl xs b", dx=8, dy=-6))
    o.append(f'<circle cx="{Xw[0]:.1f}" cy="{Xw[1]:.1f}" r="5" class="ghost"/>')
    o.append(text(Xw, "X′（誤用 +0.667）", "lbl xs mute", dx=8, dy=16))
    for v, lab, anc, dx in ((c_val + r_val, "σ₁ = 42.0 MPa", "start", 6), (c_val - r_val, "σ₂ = −10.6 kPa", "end", -6)):
        px = ox + v * sx
        o.append(f'<circle cx="{px:.1f}" cy="{oy}" r="4" class="pt2"/>')
    o.append(text((ox + (c_val + r_val) * sx, oy), "σ₁", "lbl sm", dx=6, dy=18))
    o.append(text((ox + (c_val - r_val) * sx, oy), "σ₂", "lbl sm", dx=-6, dy=18, anchor="end"))
    o.append(text((c + 40, oy + r + 26), "τ 已放大繪製（非比例尺）；X 與 X′ 落在同一個圓上", "lbl xs mute", anchor="middle"))
    return o


BEAM = svg(beam_svg(), "0 0 640 420", "懸臂梁立體示意圖")
SECT = svg(section_svg(), "0 0 460 360", "斷面與 Q 面積")
FBD = svg(fbd_svg(), "0 0 680 280", "自由端段自由體圖")
ELA = svg(element_svg("A"), "0 0 340 310", "A 點應力元素")
ELB = svg(element_svg("B"), "0 0 340 310", "B 點應力元素")
MOHR = svg(mohr_svg(), "-40 -10 480 360", "B 點莫爾圓")

html = Path(__file__).with_name("template.html").read_text(encoding="utf-8")
for k, v in dict(BEAM=BEAM, SECT=SECT, FBD=FBD, ELA=ELA, ELB=ELB, MOHR=MOHR).items():
    html = html.replace("{{" + k + "}}", v)
Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print("ok")
