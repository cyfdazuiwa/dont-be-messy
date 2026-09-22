#!/usr/bin/env python3
"""生成交互页面 calm_interactive.html：
  第一页：头顶乱麻胸像动图（与 mess_head_tangle 同构图），乱麻中心慢慢浮现
          红色单词 calm；点击 calm → 立即进入第二幕（小人消失，乱麻与手中
          mess 单词从原位置飞散重排成参考图式多排词阵）。
  第二幕：两幕同尺寸比例（800×1000 逻辑框，高 100vh 居中显示）。底部 ¿ 由玩家
          控制：←→ / A·D 或拖动左右移动，点击 ¿（或空格）向上发射粒子；
          命中 mess 该词变红并停下；命中唯一隐藏的红色 calm 游戏结束。
  调试参数：?t=秒   第一页静帧（calm 直接可见）
           ?scene=2            直接进入第二页
           ?scene=2&win=1      直接进入结束状态
           ?scene=2&sim=秒     加载时同步模拟运行到该游戏时刻
           ?scene=2&selftest=1 自动从中心射击（测试碰撞）
"""
import math, random

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calm_interactive.html")
FONT = "'Comic Sans MS','Marker Felt','Segoe Print',cursive"
CX, CY = 415.0, 330.0

def loop_path(seed, base_r):
    rng = random.Random(seed)
    cx = CX + rng.uniform(-55, 55)
    cy = CY + rng.uniform(-45, 45)
    a = rng.uniform(0, 6.28)
    turns = rng.uniform(0.95, 1.25)
    n = rng.randint(24, 30)
    pts = []
    for _ in range(n):
        r = base_r + 30 * math.sin(a * 2.1 + seed) + rng.uniform(-14, 14)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        a += 6.2832 * turns / n + rng.uniform(-0.06, 0.06)
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    m = len(pts)
    for i in range(m):
        q0 = pts[(i - 1) % m]; q1 = pts[i]; q2 = pts[(i + 1) % m]; q3 = pts[(i + 2) % m]
        c1 = (q1[0] + (q2[0] - q0[0]) / 6.0, q1[1] + (q2[1] - q0[1]) / 6.0)
        c2 = (q2[0] - (q3[0] - q1[0]) / 6.0, q2[1] - (q3[1] - q1[1]) / 6.0)
        d += f" C {c1[0]:.1f} {c1[1]:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {q2[0]:.1f} {q2[1]:.1f}"
    return d + " Z"

loops = [loop_path(40 + i, r) for i, r in enumerate(
    [52, 66, 80, 94, 108, 122, 136, 150, 164, 178, 195, 212])]
defs_loops = "".join(f'<path id="lp{i}" d="{loops[i]}" fill="none"/>' for i in range(12))
inner = "".join(f'<text font-family="{FONT}" font-size="27" fill="#000" letter-spacing="1">'
                f'<textPath xlink:href="#lp{i}" href="#lp{i}">{"mess " * 30}</textPath></text>'
                for i in range(0, 12, 2))
outer = "".join(f'<text font-family="{FONT}" font-size="27" fill="#000" letter-spacing="1">'
                f'<textPath xlink:href="#lp{i}" href="#lp{i}">{"mess " * 30}</textPath></text>'
                for i in range(1, 12, 2))

TEMPLATE = """<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>mess → calm</title>
<style>
  html,body{margin:0;height:100%;background:#fff;overflow:hidden;
            font-family:-apple-system,'PingFang SC',Arial,sans-serif}
  /* 两幕共用同一显示框：高 100vh、宽 0.8 倍、居中（800×1000 比例） */
  #s1{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
      height:100vh;width:auto;transition:opacity .25s ease}
  body.go #s1{opacity:0;pointer-events:none}
  #game{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);display:none;cursor:crosshair}
  body.go #game{display:block}
  #calmG{cursor:pointer;opacity:0;animation:calmIn 4s ease 2.2s forwards}
  @keyframes calmIn{to{opacity:1}}
  #calmT{transform-box:fill-box;transform-origin:center;animation:calmPulse 3s ease-in-out 6.2s infinite alternate}
  @keyframes calmPulse{from{transform:scale(1)}to{transform:scale(1.08)}}
  body.noanim *{animation:none !important}
</style>
</head>
<body>
<svg id="s1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 800 1000" width="800" height="1000">
  <rect width="800" height="1000" fill="#ffffff"/>
  <defs>
    @@DEFS_LOOPS@@
    <path id="strandL" d="M 388 560 C 372 640, 352 720, 342 800 C 338 830, 337 862, 339 892 C 340 912, 342 928, 345 940" fill="none"/>
    <path id="strandR" d="M 452 560 C 478 640, 503 700, 515 750 C 521 772, 524 780, 525 800 C 527 828, 539 856, 557 880" fill="none"/>
  </defs>

  <!-- 线描胸像 -->
  <g id="figure" stroke="#000" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M 357 533
             C 320 572, 287 616, 274 666
             C 261 728, 257 794, 267 851
             C 274 893, 296 918, 327 914
             C 342 911, 347 898, 339 886"/>
    <ellipse cx="401" cy="448" rx="80" ry="97" transform="rotate(-8 401 448)"/>
    <path d="M 453 530
             C 492 570, 523 616, 535 664
             C 549 726, 553 793, 544 850
             C 537 891, 517 914, 494 908
             C 480 904, 476 890, 485 876
             C 495 858, 511 828, 520 799"/>
  </g>

  <!-- 手中垂下的两条 mess 线 -->
  <text font-family="@@FONT@@" font-size="30" fill="#000" letter-spacing="1">
    <textPath id="tpL" xlink:href="#strandL" href="#strandL" startOffset="2">@@MESS14@@</textPath>
  </text>
  <text font-family="@@FONT@@" font-size="30" fill="#000" letter-spacing="1">
    <textPath id="tpR" xlink:href="#strandR" href="#strandR" startOffset="2">@@MESS14@@</textPath>
  </text>

  <!-- 双拳 -->
  <g stroke="#000" stroke-width="7" stroke-linecap="round" fill="#fff">
    <path d="M 320 850 C 336 842, 352 850, 354 870 C 356 890, 344 904, 326 900 C 310 896, 306 878, 312 864 C 314 858, 317 852, 320 850 Z"/>
    <path d="M 318 866 C 326 870, 338 870, 346 864" fill="none"/>
    <path d="M 317 882 C 325 886, 337 886, 345 880" fill="none"/>
    <path d="M 507 754 C 523 746, 539 754, 541 774 C 543 794, 531 808, 513 804 C 497 800, 493 782, 499 768 C 501 762, 504 756, 507 754 Z"/>
    <path d="M 505 770 C 513 774, 525 774, 533 768" fill="none"/>
    <path d="M 504 786 C 512 790, 524 790, 532 784" fill="none"/>
  </g>

  <!-- 乱麻云 -->
  <g id="gCloud">
    <g id="gOuter">@@OUTER@@</g>
    <g id="gInner">@@INNER@@</g>
  </g>

  <!-- 慢慢浮现的红色 calm（可点击） -->
  <g id="calmG">
    <rect x="335" y="288" width="160" height="84" fill="transparent"/>
    <text id="calmT" x="415" y="346" text-anchor="middle" font-family="@@FONT@@"
          font-size="48" fill="#d43a2f" letter-spacing="2">calm</text>
  </g>
</svg>

<canvas id="game"></canvas>
<div id="ver" style="position:fixed;right:6px;bottom:4px;font:11px -apple-system,Arial;color:#c8c8c8;z-index:99;pointer-events:none">v6</div>

<script>
(function(){
"use strict";
var FONT = "@@FONT@@";
var RED = "#d43a2f", INK = "#111";
var svg = document.getElementById("s1");
var gInner = document.getElementById("gInner");
var gOuter = document.getElementById("gOuter");
var gCloud = document.getElementById("gCloud");
var tpL = document.getElementById("tpL"), tpR = document.getElementById("tpR");
var calmG = document.getElementById("calmG");
var cv = document.getElementById("game"), ctx = cv.getContext("2d");
var q = new URLSearchParams(location.search);
var SELFTEST = false;
var scene = 1, t0 = performance.now(), tNow = 0;

/* ---------- 第一页：乱麻动图 ---------- */
function pose1(t){
  gInner.setAttribute("transform", "rotate(" + (-720*t/16) + " 415 330)");
  gOuter.setAttribute("transform", "rotate(" + (360*t/16) + " 415 330)");
  var s = 1 + 0.015*Math.sin(2*Math.PI*t/16);
  gCloud.setAttribute("transform", "translate(415 330) scale(" + s + ") translate(-415 -330)");
  var pL = 92, pR = 92;
  try { pL = tpL.parentNode.getSubStringLength(0,5); } catch(e){}
  try { pR = tpR.parentNode.getSubStringLength(0,5); } catch(e){}
  tpL.setAttribute("startOffset", 2 + ((pL/4*t) % pL));
  tpR.setAttribute("startOffset", 2 + ((pR/4*t) % pR));
}

var calmReady = false;
/* calm 淡出动画 2.2s 开始、4s 完成；2.4s 后即可点击（无需等动画完全结束） */
setTimeout(function(){ calmReady = true; }, 2400);
calmG.addEventListener("click", function(){ if (calmReady && scene === 1) startTransition(); });

/* 点击 calm：第一页立即收起，第二幕原地开始（词从乱麻原位置飞散重排） */
function startTransition(){
  if (scene !== 1) return;
  scene = 2;
  document.body.classList.add("go");
  svg.style.display = "none";
  startGame(415, 330);
}

/* ---------- 第二幕：词阵游戏（逻辑坐标与第一幕同为 800×1000） ---------- */
var GW = 800, GH = 1000;
var words = [], parts = [];
var won = false, wonT = 0, lastShot = -5, gTime0 = 0, lastKick = -9;
var px = GW/2, keys = {left:false, right:false}, aimX = null;

function resize(){
  var d = window.devicePixelRatio || 1;
  var vh = innerHeight, vw = innerWidth;
  var dh = vh, dw = vh*0.8;
  if (dw > vw){ dw = vw; dh = vw/0.8; }
  cv.style.width = dw + "px"; cv.style.height = dh + "px";
  cv.width = Math.round(dw*d); cv.height = Math.round(dh*d);
  ctx.setTransform(cv.width/GW, 0, 0, cv.height/GH, 0, 0);
}
window.addEventListener("resize", resize);

function mkWord(text, row, rowY, x0, sx, sy, id){
  return { text:text, row:row, rowY:rowY, x0:x0, sx:sx, sy:sy,
           cx:sx, cy:sy, dir:(row%2 ? 1 : -1), spd:90+Math.random()*90, cur:0,
           size:(text==="calm" ? 28 : 20+Math.random()*10),
           phase:Math.random()*6.28, bob:3+Math.random()*4, hw:30,
           state:(text==="calm" ? "calm" : "alive"),
           flyStart:id*0.02, flyDur:800, arrived:false, pop:0, alpha:1 };
}

function startGame(sx, sy){
  resize();
  cv.style.display = "block";
  gTime0 = performance.now();
  words = []; parts = []; won = false; lastShot = -5;
  px = GW/2;
  var rows = 7, per = [7,8,9,9,8,7,6];               /* mess 数量增多：54 个 */
  var top = GH*0.10, gap = 34;
  var id = 0;
  for (var r=0; r<rows; r++){
    for (var j=0; j<per[r]; j++){
      words.push(mkWord("mess", r, top + r*gap + (Math.random()*12-6),
                        GW*0.08 + Math.random()*GW*0.84,
                        sx + (Math.random()*160-80), sy + (Math.random()*100-50), id++));
    }
  }
  /* 红色 calm 混进 mess 行中：随机行随机位置，速度约为 mess 的两倍 */
  var calmRow = Math.floor(Math.random()*rows);
  var calmW = mkWord("calm", calmRow, top + calmRow*gap + (Math.random()*12-6),
                     GW*0.08 + Math.random()*GW*0.84,
                     sx + (Math.random()*160-80), sy + (Math.random()*100-50), id++);
  calmW.spd = 340 + Math.random()*140;   /* 约 mess 的 2.5 倍 */
  calmW.bob = 16 + Math.random()*12;     /* 上下窜动幅度加大 */
  calmW.flyStart = 1.4; calmW.flyDur = 1200;
  words.push(calmW);
  for (var i=0;i<words.length;i++){
    ctx.font = words[i].size + "px " + FONT;
    words[i].hw = ctx.measureText(words[i].text).width/2;
  }
  if (q.get("win") === "1"){ won = true; wonT = -10; resolveHit(calmWord()); }
  SELFTEST = (q.get("selftest") === "1");
  var sim = parseFloat(q.get("sim"));
  if (!isNaN(sim)){
    var nSteps = Math.round(sim/0.016);
    for (var s2=0; s2<nSteps; s2++){ tNow += 0.016; stepGame(); }
    gTime0 = performance.now() - tNow*1000;
  }
}

function calmWord(){ for (var i=0;i<words.length;i++) if (words[i].state==="calm") return words[i]; return null; }

function fire(){
  if (won || scene !== 2) return;
  if (tNow - lastShot < 0.24) return;
  parts.push({ x: px, y: GH*0.87 - 80, vy: -1100 });
  lastShot = tNow; lastKick = tNow;
}

function resolveHit(w){
  if (won) return;
  if (w.state === "alive"){ w.state = "red"; w.pop = tNow; }
  else if (w.state === "calm"){ won = true; wonT = tNow; }
}

function stepGame(){
try {
  var t = tNow;
  var dt = Math.max(0, Math.min(0.05, t - (stepGame.last || t)));
  stepGame.last = t;
  ctx.clearRect(0,0,GW,GH);
  /* 玩家控制 ¿ 左右移动 */
  if (keys.left)  px -= 420*dt;
  if (keys.right) px += 420*dt;
  if (aimX !== null) px += (aimX - px)*Math.min(1, dt*12);
  px = Math.max(45, Math.min(GW-45, px));
  var i, w;
  for (i=0;i<words.length;i++){
    w = words[i];
    if (!w.arrived){
      var p = Math.max(0, Math.min(1, (t - w.flyStart)/(w.flyDur/1000)));
      var e = 1 - Math.pow(1-p, 3);
      w.cx = w.sx + (w.x0 - w.sx)*e;
      w.cy = w.sy + (w.rowY - w.sy)*e;
      if (p >= 1){ w.arrived = true; }
    } else if (w.state !== "red"){
      w.cur += (w.spd - w.cur) * Math.min(1, dt*2);
      w.cx += w.dir * w.cur * dt;
      var lo = GW*0.07, hi = GW*0.93;
      if (w.cx > hi) w.cx = lo;
      if (w.cx < lo) w.cx = hi;
      w.cy = w.rowY + w.bob * Math.sin(6.283*(t*0.55 + w.phase));
    }
    var alpha = w.alpha, size = w.size;
    if (won && w.state !== "calm"){
      alpha = Math.max(0, 1 - (t - wonT)/1.2);
      if (alpha <= 0) continue;
    }
    if (won && w.state === "calm"){
      var k = Math.min(1, (t - wonT)/1.4), e2 = 1 - Math.pow(1-k, 3);
      w.cx += (GW*0.5 - w.cx)*e2;
      w.cy += (GH*0.42 - w.cy)*e2;
      size = 28 + 46*e2;
      size *= 1 + 0.03*Math.sin(t*2.2);
    }
    var scale = 1;
    if (w.pop && t - w.pop < 0.25) scale = 1 + 0.25*(1 - (t-w.pop)/0.25);
    ctx.save();
    ctx.translate(w.cx, w.cy); ctx.scale(scale, scale);
    ctx.globalAlpha = alpha;
    ctx.font = w.size + "px " + FONT;
    ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
    ctx.fillStyle = (w.state === "alive") ? INK : RED;
    ctx.fillText(w.text, 0, 0);
    ctx.restore();
  }
  for (i=parts.length-1;i>=0;i--){
    var pp = parts[i];
    var py0 = pp.y;
    pp.y += pp.vy*dt;
    /* 扫掠碰撞：粒子竖直上行，碰到未被击中的词即命中 */
    var hitw = null;
    for (var k=0;k<words.length;k++){
      var ww = words[k];
      if (ww.state === "red") continue;
      if (Math.abs(pp.x - ww.cx) <= (ww.hw||30) + 5 &&
          pp.y <= ww.cy + ww.size*0.35 && py0 >= ww.cy - ww.size*0.95){
        hitw = ww; break;
      }
    }
    if (hitw){ resolveHit(hitw); hitw.pop = tNow; parts.splice(i,1); continue; }
    if (pp.y < -40){ parts.splice(i,1); continue; }
    ctx.fillStyle = INK;
    ctx.beginPath(); ctx.arc(pp.x, pp.y, 4.5, 0, 6.283); ctx.fill();
  }
  /* 底部问号 ¿（玩家控制，点击它发射） */
  var kick = Math.max(0, 1 - (tNow - lastKick)*4);
  ctx.save();
  ctx.translate(px, GH*0.87);
  var ks = 1 + 0.02*Math.sin(tNow*1.7) + 0.12*kick;
  ctx.scale(ks, ks);
  ctx.fillStyle = INK;
  ctx.font = "700 108px -apple-system, 'PingFang SC', Arial, sans-serif";
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillText("\\u00BF", 0, 0);
  ctx.restore();
  /* 操作提示（开局 6 秒后淡出） */
  if (!won && t < 6){
    ctx.globalAlpha = Math.max(0, Math.min(1, 6 - t))*0.75;
    ctx.fillStyle = "#9a9a9a";
    ctx.font = "16px -apple-system, 'PingFang SC', Arial, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("移动到词阵下方，点击 \\u00BF 发射 \\u00B7 也可用 \\u2190\\u2192 或 A/D 移动、空格射击", GW/2, GH*0.965);
    ctx.globalAlpha = 1;
  }
  if (won){
    var rel = tNow - wonT;
    /* 打中 calm：先居中呼吸，随后出现黑色 excellent 提示 */
    if (rel > 1.5){
      ctx.globalAlpha = Math.min(1, (rel - 1.5)/0.5);
      ctx.fillStyle = INK;
      ctx.font = "700 40px -apple-system, 'PingFang SC', Arial, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("excellent", GW/2, GH*0.60);
      ctx.globalAlpha = 1;
    }
    /* 3s 后白场过渡，进入第三幕 */
    if (rel > 3.4){
      var f3 = Math.min(1, (rel - 3.4)/0.7);
      ctx.globalAlpha = f3; ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, GW, GH); ctx.globalAlpha = 1;
      if (f3 >= 1) startScene3();
    }
  }
} catch(err){
  ctx.fillStyle="#b00"; ctx.font="20px monospace"; ctx.textAlign="left";
  ctx.fillText("ERR "+err.message, 20, GH*0.5);
}
}

/* ---------- 输入 ---------- */
function toLogical(e){
  var r = cv.getBoundingClientRect();
  return { x:(e.clientX - r.left)*GW/r.width, y:(e.clientY - r.top)*GH/r.height };
}
cv.addEventListener("pointermove", function(e){
  if (scene === 3){
    if (!s3.dragging) return;
    var l = toLogical(e);
    s3.dotX = Math.max(s3.dotX, Math.max(130, Math.min(670, l.x)));
    return;
  }
  if (scene !== 2 || won) return;
  var l = toLogical(e);
  aimX = Math.max(45, Math.min(GW-45, l.x));
});
cv.addEventListener("pointerdown", function(e){
  if (scene === 3){
    s3.dragging = true;
    var l = toLogical(e);
    s3.dotX = Math.max(s3.dotX, Math.max(130, Math.min(670, l.x)));
    return;
  }
  if (won){ if (tNow - wonT > 1.6) location.reload(); return; }
  if (scene !== 2) return;
  var l = toLogical(e);
  /* 点击 ¿ 本体：发射 */
  if (Math.hypot(l.x - px, l.y - GH*0.87) < 80) fire();
});
window.addEventListener("keydown", function(e){
  if (e.code === "ArrowLeft" || e.code === "KeyA") keys.left = true;
  else if (e.code === "ArrowRight" || e.code === "KeyD") keys.right = true;
  else if (e.code === "Space" || e.code === "ArrowUp" || e.code === "KeyW"){
    if (won){ if (tNow - wonT > 1.6) location.reload(); }
    else fire();
    e.preventDefault();
  }
});
window.addEventListener("keyup", function(e){
  if (e.code === "ArrowLeft" || e.code === "KeyA") keys.left = false;
  if (e.code === "ArrowRight" || e.code === "KeyD") keys.right = false;
});
window.addEventListener("pointerup", function(){ if (s3) s3.dragging = false; });

/* ---------- 第三幕：拖动黑点，把三排乱线拉成直线 ---------- */
var s3 = null;

function makeLine(baseY, a1, f1, a2, f2, loopT, loopR, loopUp){
  var N = 90, pts = [];
  for (var i=0;i<N;i++){
    var t = i/(N-1);
    pts.push({ x: 130 + 540*t + 14*Math.sin(t*6.283 + baseY),
               y: baseY + a1*Math.sin(6.283*t*f1 + baseY*0.013) + a2*Math.sin(6.283*t*f2 + 1.3) });
  }
  /* 在 loopT 处卷一个小圈 */
  var idx = Math.round(loopT*(N-1)), c = pts[idx], lp = [];
  for (var k=0;k<=14;k++){
    var a = -1.2 + k/14*6.283;
    lp.push({ x: c.x + loopR*Math.cos(a), y: c.y - loopUp - loopR*Math.sin(a)*0.85 });
  }
  pts = pts.slice(0, idx).concat(lp, pts.slice(idx));
  var straight = [];
  for (var i2=0;i2<pts.length;i2++) straight.push({ x: 130 + 540*i2/(pts.length-1), y: baseY });
  return { pts: pts, straight: straight };
}

function startScene3(){
  scene = 3;
  aimX = null;            /* 清掉第二幕残留的瞄准坐标，避免黑点被瞬移 */
  s3 = { p:0, dotX:130, alpha:0, lines:[
    makeLine(350, 26, 2.2, 10, 4.6, 0.62, 24, 30),
    makeLine(520, 34, 1.5, 13, 3.4, 0.30, 28, 34),
    makeLine(690, 30, 2.7, 15, 5.8, 0.80, 21, 30)
  ]};
}

function stepScene3(dt){
  s3.alpha += (1 - s3.alpha)*Math.min(1, dt*3);
  /* 按住黑点向右拖（指针或 ←→ 键）：进度只增不减，拉直后保持直线 */
  if (keys.left)  s3.dotX = Math.max(130, s3.dotX - 460*dt);
  if (keys.right) s3.dotX = Math.min(670, s3.dotX + 460*dt);
  if (s3.dragging && aimX !== null) s3.dotX = Math.max(s3.dotX, Math.max(130, Math.min(670, aimX)));
  s3.maxX = Math.max(s3.maxX || 130, s3.dotX);
  s3.p = Math.max(s3.p, Math.max(0, Math.min(1, (s3.maxX - 130)/540)));
  var pe = s3.p*s3.p*(3 - 2*s3.p);

  ctx.clearRect(0,0,GW,GH);
  ctx.globalAlpha = s3.alpha;
  /* 标题 */
  ctx.fillStyle = INK;
  ctx.font = "700 26px -apple-system, 'PingFang SC', Arial, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("How calm are you today?", GW/2, 175);
  ctx.fillStyle = "#9a9a9a";
  ctx.font = "18px -apple-system, Arial, sans-serif";
  ctx.fillText("Drag \u2192", GW/2, 218);
  /* 三条线：起止对齐，从左到右依次被抚平 */
  ctx.strokeStyle = INK; ctx.lineWidth = 8;
  ctx.lineCap = "round"; ctx.lineJoin = "round";
  for (var li=0; li<s3.lines.length; li++){
    var L = s3.lines[li], n = L.pts.length;
    ctx.beginPath();
    for (var i=0;i<n;i++){
      var t_i = i/(n-1);
      var wi = Math.max(0, Math.min(1, (pe*1.15 - t_i)/0.15));
      wi = wi*wi*(3 - 2*wi);
      var x = L.pts[i].x + (L.straight[i].x - L.pts[i].x)*wi;
      var y = L.pts[i].y + (L.straight[i].y - L.pts[i].y)*wi;
      if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
    }
    ctx.stroke();
  }
  /* 黑点吸附在中间线的当前高度上（与线条相连） */
  var Lm = s3.lines[1], nm = Lm.pts.length-1;
  var mi = Math.max(0, Math.min(nm, Math.round((s3.dotX-130)/540*nm)));
  var mw = Math.max(0, Math.min(1, (pe*1.15 - mi/nm)/0.15));
  mw = mw*mw*(3-2*mw);
  var dy = Lm.pts[mi].y + (520 - Lm.pts[mi].y)*mw;
  ctx.fillStyle = INK;
  ctx.beginPath(); ctx.arc(s3.dotX, dy, 15, 0, 6.283); ctx.fill();
  ctx.globalAlpha = 1;
}

/* ---------- 主循环 ---------- */
function frame(now){
  var dt = Math.max(0, Math.min(0.05, (now - (frame.last || now))/1000));
  frame.last = now;
  if (scene < 2) pose1((now - t0)/1000);
  if (scene === 2){
    tNow = (now - gTime0)/1000;
    stepGame();
  }
  if (scene === 3) stepScene3(dt);
  requestAnimationFrame(frame);
}

/* ---------- 启动 ---------- */
var qt = parseFloat(q.get("t"));
if (!isNaN(qt)){
  document.body.classList.add("noanim");
  calmG.style.opacity = 1; calmReady = true;
  pose1(qt);
} else {
  requestAnimationFrame(frame);
}
if (q.get("scene") === "2"){
  scene = 2;
  document.body.classList.add("go");
  svg.style.display = "none";
  startGame(GW*0.5, GH*0.33);
}
if (q.get("scene") === "3"){
  document.body.classList.add("go");
  svg.style.display = "none";
  resize();
  cv.style.display = "block";
  startScene3();
  var dv = parseFloat(q.get("drag"));
  if (!isNaN(dv)){ s3.p = Math.max(0, Math.min(1, dv)); s3.dotX = 130 + 540*s3.p; }
}
})();
</script>
</body>
</html>
"""

MESS14 = "mess " * 14
html = (TEMPLATE
        .replace("@@DEFS_LOOPS@@", defs_loops)
        .replace("@@INNER@@", inner)
        .replace("@@OUTER@@", outer)
        .replace("@@FONT@@", FONT)
        .replace("@@MESS14@@", MESS14))
with open(OUT, "w") as f:
    f.write(html)
print("written", OUT, len(html), "bytes")
