"""Website-only design layer, applied by build.py on top of the store page.

Each change is a find-and-replace on the store's page code. If the store page
changes so a piece is not found, that piece is skipped (and reported) instead of
breaking the build, so the website always publishes.
"""

FONT_OLD = 'family=Kalam:wght@400;700&display=swap">\n<style id="app-style">'
FONT_NEW = 'family=Kalam:wght@400;700&family=Rozha+One&display=swap">\n<style id="app-style">'

HERO_START = "h+='<section class=\"brand\">"
HERO_END_MARK = "h+='<div class=\"how\""

HERO_JS = r"""var cimg=s.catImg||{},pics=['Sweets','Chocolates','Dry Fruits','Hampers','Namkeens','Cookies'].map(function(c){return cimg[c]}).filter(Boolean).slice(0,4);
    h+='<section class="hero"><div class="lights"></div><div class="hero-txt"><p class="eyebrow">Diwali gifting'+(s.delivery?' · '+esc(s.delivery):'')+'</p><h2>'+esc(s.name)+'</h2>'+(s.tagline?'<p class="tag">'+esc(s.tagline)+'</p>':'')+'<ul class="perks"><li>'+I.star+'Handpicked festive gift packs</li><li>'+I.star+'Order easily on WhatsApp</li></ul><div class="hero-cta"><button class="cta" id="shopNow">Shop gift packs</button>'+(waNumber()?'<button class="cta2" id="chatWa">'+I.wa+'Chat with us</button>':'')+'</div></div>'+(pics.length>=2?'<div class="mosaic" aria-hidden="true">'+pics.map(function(u){return '<img src="'+esc(u)+'" alt="">'}).join('')+'</div>':'')+'</section>';
    """

DIYA_OLD = "drawDiya(document.getElementById('diya'));"
DIYA_NEW = "var dy=document.getElementById('diya');if(dy)drawDiya(dy);"

CLICK_OLD = "case 'shareWa':openLink("
CLICK_NEW = ("case 'chatWa':case 'chatWa2':openLink('https://wa.me/'+waNumber()+'?text='+encodeURIComponent('Hello '+state.store.name+'! I would like to know about your gift packs.'));break;\n"
             "      case 'shareWa':openLink(")

FOOT_OLD = "<div class=\"flourish\">'+flourishSVG(false)+'<span>Wishing you a bright, sweet Diwali</span>'+flourishSVG(true)+'</div></div></main>';"
FOOT_NEW = ("<div class=\"flourish\">'+flourishSVG(false)+'<span>Wishing you a bright, sweet Diwali</span>'+flourishSVG(true)+'</div>"
            "<footer class=\"foot-c\"><div class=\"fc-logo\">'+(s.logo?'<img src=\"'+esc(s.logo)+'\" alt=\"\">':'')+'</div>"
            "<div class=\"fc-txt\"><b>'+esc(s.name)+'</b><span>'+esc(s.delivery||'Gift packs for every occasion')+'</span></div>"
            "'+(waNumber()?'<button class=\"cta2\" id=\"chatWa2\">'+I.wa+'+'+waNumber().slice(0,2)+' '+waNumber().slice(2,7)+' '+waNumber().slice(7)+'</button>':'')+'</footer></div></main>';")

CSS_ANCHOR = ".bcard.lg{flex-direction:column;"
CSS = r"""
/* ---- website design v3 ---- */
:root{--disp:"Rozha One",Georgia,"Times New Roman",serif}
.brand,.banner{display:none}
.hero{position:relative;overflow:hidden;border-radius:22px;padding:24px 18px 20px;color:#fff;display:grid;grid-template-columns:1fr;gap:18px;
  background:radial-gradient(110% 80% at 100% 0%,rgba(242,163,58,.85) 0%,rgba(242,163,58,0) 55%),linear-gradient(140deg,#4E0F38 0%,#8C2366 48%,#C2185B 100%);
  box-shadow:0 16px 36px rgba(110,26,80,.30)}
.hero::after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 12% 110%,rgba(255,213,74,.22),transparent 42%)}
.hero .lights{position:absolute;left:0;right:0;top:0;height:10px;background:radial-gradient(circle,#FFD54A 0 3px,transparent 3.5px) 0 2px/22px 10px repeat-x}
@media (prefers-reduced-motion:no-preference){.hero .lights{animation:twinkle 1.4s steps(2) infinite}}
.hero-txt{position:relative;z-index:1;min-width:0}
.eyebrow{margin:4px 0 0;font-size:11.5px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#FFD9A0}
.hero h2{font-family:var(--disp);font-weight:400;font-size:clamp(32px,9vw,50px);line-height:1.02;margin:8px 0 0;text-wrap:balance;text-shadow:0 2px 10px rgba(0,0,0,.18)}
.hero .tag{margin:10px 0 0;font-size:13.5px;line-height:1.45;opacity:.92;white-space:pre-line;max-width:44ch}
.stats{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 0;padding:0}
.stats li{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.24);border-radius:999px;padding:5px 11px;font-size:12.5px;font-weight:600}
.stats b{font-weight:800;color:#FFD54A}
.hero-cta{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.hero .cta{margin:0;padding:11px 16px;font-size:14px;font-weight:800;border:0;border-radius:12px;background:#fff;color:#8C2366;box-shadow:0 6px 16px rgba(0,0,0,.18)}
.cta2{display:inline-flex;align-items:center;gap:7px;border:1.5px solid rgba(255,255,255,.6);background:rgba(255,255,255,.06);color:#fff;font-weight:800;font-size:14px;border-radius:12px;padding:10px 14px}
.cta2 svg{width:18px;height:18px;flex:none}
.mosaic{position:relative;z-index:1;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.mosaic img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:12px;border:2px solid rgba(255,255,255,.8);box-shadow:0 8px 18px rgba(0,0,0,.22);display:block;background:#fff}
.mosaic img:nth-child(odd){transform:rotate(-2.5deg)}.mosaic img:nth-child(even){transform:rotate(2.5deg) translateY(4px)}
@media (min-width:640px){.hero{grid-template-columns:1.3fr 1fr;align-items:center;padding:32px 30px}.mosaic{grid-template-columns:1fr 1fr;gap:12px}.mosaic img{border-radius:16px}}
.how{background:var(--surface);border-radius:16px;padding:8px;box-shadow:0 3px 12px rgba(160,60,40,.08);gap:2px}
.how div{background:transparent;box-shadow:none;border:0;padding:6px 4px}
.how b{background:linear-gradient(135deg,var(--berry),var(--rose));color:#fff}
.sec-t h3{font-family:var(--disp);font-weight:400;font-size:24px;letter-spacing:.005em}
.sec-t h3 svg{width:20px;height:20px}
.off{clip-path:none;border-radius:8px;top:8px;left:8px;padding:4px 6px 4px;box-shadow:0 3px 8px rgba(232,115,26,.35)}
.card .pic{box-shadow:inset 0 0 0 1px rgba(140,35,102,.06)}
.cat span,.cat{font-weight:800}
.foot-c{margin-top:18px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:linear-gradient(135deg,#4E0F38,#8C2366);color:#fff;border-radius:18px;padding:16px}
.fc-logo{width:48px;height:48px;border-radius:50%;background:#fff;display:grid;place-items:center;overflow:hidden;flex:none}
.fc-logo img{width:84%;height:84%;object-fit:contain}
.fc-txt{display:flex;flex-direction:column;flex:1;min-width:150px}
.fc-txt b{font-family:var(--disp);font-weight:400;font-size:19px;line-height:1.15}
.fc-txt span{font-size:12.5px;opacity:.85}

/* ---- palette: royal peacock, gold & marigold ---- */
:root{--bg:#FFF8EC;--surface:#FFFFFF;--ink:#1D2B30;--muted:#5F6E72;--line:#EEDFC4;--soft:#F6EBD6;
  --berry:#0E5A6B;--berry-deep:#08343F;--berry-soft:#E3F1F1;--rose:#127A86;
  --gold:#E9B949;--gold-2:#F6D47A;--marigold:#F08A24;--offer:#C2185B;--tile:#FFF6E6}
body{background-image:radial-gradient(900px 420px at 50% 0,rgba(233,185,73,.20),transparent 70%),var(--pattern,none)}
.hdr{background:linear-gradient(100deg,#08343F,#0E5A6B 55%,#127A86);box-shadow:0 2px 14px rgba(8,52,63,.35)}
.hbtn{border-color:rgba(246,212,122,.55)}
.search input{box-shadow:0 0 0 2px rgba(233,185,73,.55)}
.hero{background:radial-gradient(90% 70% at 100% 0%,rgba(240,138,36,.55) 0%,rgba(240,138,36,0) 60%),radial-gradient(70% 60% at 0% 100%,rgba(233,185,73,.30),transparent 60%),linear-gradient(140deg,#062A33 0%,#0A4654 45%,#0E5A6B 100%);
  box-shadow:0 18px 40px rgba(8,52,63,.35);border:1px solid rgba(233,185,73,.45)}
.hero::before{content:"";position:absolute;inset:8px;border:1px dashed rgba(246,212,122,.35);border-radius:16px;pointer-events:none}
.hero h2{color:var(--gold-2);text-shadow:0 2px 14px rgba(0,0,0,.25)}
.eyebrow{color:#FFC98A}
.perks{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:6px}
.perks li{display:flex;align-items:center;gap:8px;font-size:13.5px;font-weight:600;color:#F3EBDD}
.perks svg{width:16px;height:16px;color:var(--gold);flex:none}
.hero .cta{background:linear-gradient(135deg,var(--gold-2),var(--gold));color:#08343F}
.cta2{border-color:rgba(246,212,122,.7)}
.mosaic img{border-color:var(--gold-2)}
.add,.step,.btn.berry{background:linear-gradient(135deg,var(--gold-2),var(--gold));color:#08343F;box-shadow:0 4px 12px rgba(233,185,73,.45)}
.wopt.on{background:var(--berry);border-color:var(--berry);color:#fff}
.bar-in{background:linear-gradient(100deg,#08343F,#0E5A6B);box-shadow:0 8px 24px rgba(8,52,63,.40)}
.bar-in .go{color:var(--gold-2)}
.price b{color:var(--berry-deep)}
.off{background:var(--offer)}
.best{background:linear-gradient(90deg,#08343F,#127A86)}
.top-wrap{background:linear-gradient(180deg,#FBEBC6,#FFF6E4);box-shadow:inset 0 0 0 1px #EBD29A}
.sec-t h3{color:var(--berry-deep)}
.sec-t h3::after{background:linear-gradient(90deg,var(--gold),var(--marigold))}
.cat .ico,.cat .ico.ph{border-color:#fff;box-shadow:0 0 0 2px var(--gold-2),0 6px 16px rgba(8,52,63,.16)}
.cat.on .ico{box-shadow:0 0 0 3px var(--berry),0 6px 16px rgba(8,52,63,.25)}
.how b{background:linear-gradient(135deg,var(--berry),var(--rose))}
.foot-c{background:linear-gradient(135deg,#062A33,#0E5A6B);border:1px solid rgba(233,185,73,.45)}
.fc-txt b{color:var(--gold-2)}
.share-ic,.zbtn{color:var(--berry)}
.chip.on,.bchip.on{background:var(--berry);border-color:var(--berry);color:#fff}
"""


def apply(body):
    """Return (new_body, skipped) after applying the website design changes."""
    skipped = []

    def rep(old, new, name):
        nonlocal body
        if body.count(old) == 1:
            body = body.replace(old, new)
        else:
            skipped.append(name)

    rep(FONT_OLD, FONT_NEW, 'font')
    a = body.find(HERO_START)
    b = body.find(HERO_END_MARK, a)
    if a >= 0 and b > a:
        body = body[:a] + HERO_JS + body[b:]
    else:
        skipped.append('hero')
    rep(DIYA_OLD, DIYA_NEW, 'diya')
    rep(CLICK_OLD, CLICK_NEW, 'chat button')
    rep(FOOT_OLD, FOOT_NEW, 'footer')
    i = body.find(CSS_ANCHOR)
    j = body.find('</style>', i)
    if i >= 0 and j > i:
        body = body[:j] + CSS + body[j:]
    else:
        skipped.append('css')
    return body, skipped
