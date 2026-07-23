import json
import datetime

BUILD_TIME = datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

# Cloudflare Worker URL that relays "Update Data" submissions to GitHub for a full site rebuild.
WORKER_URL = 'https://jaxstate-dashboard-relay.r-henry0623.workers.dev/'

with open('roster_data2.json') as f:
    data = json.load(f)

DATA_JSON = json.dumps(data)

with open('logo_b64.txt') as f:
    LOGO_B64 = f.read().strip()
LOGO_DATA_URI = 'data:image/png;base64,' + LOGO_B64

with open('photos_data.json') as f:
    photos_data = json.load(f)
PHOTOS_JSON = json.dumps(photos_data)

with open('headshots_data.json') as f:
    headshots_data = json.load(f)
HEADSHOTS_JSON = json.dumps(headshots_data)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="__LOGO_URI__">
<title>Jax State MBB · Performance Dashboard</title>
<style>
  :root {
    --red: #A6192E; --red-dark: #7d1123; --black: #0d0e10;
    --panel: #17181b; --panel2: #1f2023; --line: #2c2e33;
    --text: #f2f1ee; --muted: #93969d; --good: #3ecf6e; --bad: #e5484d; --neutral: #8a8d94;
    --tier-green: #3ecf6e; --tier-yellow: #e8b73d; --tier-red: #e5484d; --tier-gray: #55575c;
  }
  * { box-sizing: border-box; }
  body { margin:0; background: var(--black); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  header { background: linear-gradient(135deg, var(--red-dark), var(--red)); padding: 20px 28px 0;
    box-shadow: 0 2px 12px rgba(0,0,0,.4); position: sticky; top:0; z-index: 30; }
  .header-top { display:flex; align-items:center; justify-content:space-between; padding-bottom:16px; }
  .header-brand { display:flex; align-items:center; gap:14px; }
  .logo-badge { background:#fff; border-radius:10px; padding:6px 8px; display:flex; align-items:center; justify-content:center;
    box-shadow: 0 2px 6px rgba(0,0,0,.3); flex-shrink:0; }
  .header-logo { height:40px; width:auto; display:block; }
  .print-logo { height:46px; width:auto; display:block; }
  header h1 { margin:0; font-size: 19px; letter-spacing:.05em; text-transform:uppercase; font-weight:800; }
  header .sub { font-size:12px; color: rgba(255,255,255,.75); margin-top:2px; }
  #backBtn { display:none; background: rgba(255,255,255,.14); color:#fff; border:1px solid rgba(255,255,255,.3);
    padding:8px 14px; border-radius:8px; cursor:pointer; font-size:13px; font-weight:600; }
  #backBtn:hover { background: rgba(255,255,255,.25); }
  nav.tabs { display:flex; gap:4px; overflow-x:auto; padding: 0 2px; }
  nav.tabs button { background:transparent; border:none; color: rgba(255,255,255,.65); font-size:13px; font-weight:700;
    padding: 11px 15px; cursor:pointer; border-bottom:3px solid transparent; white-space:nowrap; letter-spacing:.02em;
    transition: color .12s ease, border-color .12s ease; }
  nav.tabs button:hover { color:#fff; }
  nav.tabs button.active { color:#fff; border-bottom-color:#fff; }
  main { max-width: 1320px; margin:0 auto; padding: 24px 28px 60px; }
  .view { display:none; } .view.active { display:block; }
  .kpi-row { display:grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap:10px; margin-bottom:16px; }
  .kpi-card { background: var(--panel); border:1px solid var(--line); border-radius:10px; padding:12px 14px; }
  .kpi-card .label { font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; font-weight:700; }
  .kpi-card .value { font-size:24px; font-weight:800; margin-top:4px; line-height:1.1; }
  .kpi-card .caption { font-size:10.5px; color: var(--muted); margin-top:3px; }
  .panels-2 { display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:14px; align-items:start; }
  @media (max-width: 920px) { .panels-2 { grid-template-columns: 1fr; } }
  .panel { background: var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px 16px; margin-bottom:12px; }
  .panel h3 { margin:0 0 10px; font-size:12.5px; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); font-weight:700; }
  .metric-block { margin-bottom: 18px; }
  .metric-head { display:flex; align-items:baseline; justify-content:space-between; margin: 14px 0 7px; }
  .metric-head h2 { font-size:14px; margin:0; text-transform:uppercase; letter-spacing:.07em; color: var(--red); font-weight:800; }
  .metric-head .unit-note { font-size:10.5px; color:var(--muted); }
  .metric-desc { font-size:12px; color:var(--muted); margin: -3px 0 10px; line-height:1.4; max-width:720px; }
  .metric-desc-sm { font-size:10.5px; color:var(--muted); line-height:1.35; margin:-3px 0 8px; }
  .info-dot { position:relative; display:inline-flex; align-items:center; justify-content:center;
    width:17px; height:17px; border-radius:50%; background:rgba(255,255,255,.12); color:var(--text);
    font-size:12px; font-style:normal; cursor:help; vertical-align:middle; }
  .info-dot:hover, .info-dot:focus { background:rgba(255,255,255,.22); outline:none; }
  .info-dot .tooltip-box { display:none; position:absolute; bottom:calc(100% + 8px); left:50%;
    transform:translateX(-50%); background:#1c1d20; border:1px solid var(--line); color:var(--text);
    font-size:13px; font-weight:400; line-height:1.4; text-transform:none; letter-spacing:normal;
    padding:10px 12px; border-radius:8px; width:240px; box-shadow:0 6px 20px rgba(0,0,0,.4); z-index:50; }
  .info-dot:hover .tooltip-box, .info-dot:focus .tooltip-box { display:block; }
  .table-wrap { overflow-x:auto; }
  table.data { width:100%; border-collapse:collapse; background: var(--panel); border-radius:12px; overflow:hidden; }
  table.data th, table.data td { padding:8px 12px; text-align:left; font-size:12.6px; border-bottom:1px solid var(--line); white-space:nowrap; }
  table.data th { color: var(--muted); font-weight:700; font-size:10.6px; text-transform:uppercase; letter-spacing:.03em; cursor:pointer; user-select:none; }
  table.data th:hover { color: var(--text); }
  table.data th.sorted { color: var(--red); }
  table.data th .arrow { font-size:9px; margin-left:3px; }
  table.data tr:last-child td { border-bottom:none; }
  table.data tr:hover td { background: rgba(255,255,255,.03); }
  table.data td.num, table.data th.num { text-align:right; }
  table.data td.num { font-variant-numeric: tabular-nums; }
  table.data td.name { font-weight:700; }
  table.data td.trend svg { display:block; }
  a.player-link { color: var(--text); text-decoration:none; font-weight:700; cursor:pointer; }
  a.player-link:hover { color: var(--red); text-decoration:underline; }
  .vs-good { color: var(--good); font-weight:700; } .vs-bad { color: var(--bad); font-weight:700; } .vs-neutral { color: var(--neutral); }
  .na { color: var(--muted); font-style:italic; }
  .bar-row { display:flex; align-items:center; gap:10px; margin-bottom:7px; }
  .bar-name { width:140px; flex-shrink:0; font-size:14px; font-weight:600; text-align:right; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; cursor:pointer; }
  .bar-name:hover { color: var(--red); }
  .bar-track { flex:1; background: var(--panel2); border-radius:2px; height:3px; position:relative; overflow:visible; }
  .bar-fill { height:100%; border-radius:2px; }
  .bar-fill.tier-green { background: var(--tier-green); box-shadow: 0 0 6px 0 rgba(62,207,110,0.85); }
  .bar-fill.tier-yellow { background: var(--tier-yellow); box-shadow: 0 0 6px 0 rgba(232,183,61,0.85); }
  .bar-fill.tier-red { background: var(--tier-red); box-shadow: 0 0 6px 0 rgba(229,72,77,0.85); }
  .bar-fill.tier-gray { background: var(--tier-gray); box-shadow: 0 0 4px 0 rgba(85,87,92,0.7); }
  .bar-val { width:60px; flex-shrink:0; font-size:11.5px; font-variant-numeric: tabular-nums; font-weight:700; }
  .bar-legend { display:flex; gap:16px; margin-bottom:12px; font-size:11px; color:var(--muted); }
  .bar-legend span { display:inline-flex; align-items:center; gap:5px; }
  .bar-legend i { width:9px; height:9px; border-radius:2px; display:inline-block; }
  .combo-legend { display:flex; gap:16px; margin-bottom:14px; font-size:11.5px; color:var(--muted); flex-wrap:wrap; }
  .combo-legend span { display:inline-flex; align-items:center; gap:6px; }
  .combo-legend i { width:8px; height:8px; border-radius:50%; display:inline-block; }
  .combo-row { display:flex; align-items:center; gap:12px; margin-bottom:11px; }
  .combo-name { width:130px; flex-shrink:0; font-size:13px; font-weight:600; text-align:right; cursor:pointer;
    overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .combo-name:hover { color: var(--red); }
  .combo-bars { flex:1; display:flex; flex-direction:column; gap:4px; }
  .combo-bar-line { display:flex; align-items:center; gap:8px; }
  .combo-bar-line .dot { width:6px; height:6px; border-radius:50%; flex-shrink:0; }
  .combo-bar-line .track { flex:1; background: var(--panel2); border-radius:2px; height:3px; overflow:visible; }
  .combo-bar-line .fill { height:100%; border-radius:2px; }
  .combo-bar-line .val { width:60px; flex-shrink:0; font-size:10.5px; color:var(--muted); text-align:left;
    font-variant-numeric: tabular-nums; }
  .toolbar { display:flex; gap:12px; flex-wrap:wrap; align-items:center; margin-bottom:14px; }
  .toolbar input, .toolbar select { background: var(--panel); border:1px solid var(--line); color: var(--text);
    padding:9px 12px; border-radius:8px; font-size:13px; }
  .toolbar input { flex:1; min-width:200px; }
  #printAllBtn { background: rgba(255,255,255,.1); border:1px solid var(--line); color:var(--text);
    padding:9px 14px; border-radius:8px; cursor:pointer; font-size:13px; white-space:nowrap; }
  #printAllBtn:hover { background: rgba(255,255,255,.18); }
  #printAllBtn:disabled { opacity:.5; cursor:wait; }
  .print-sheet-page + .print-sheet-page { page-break-before: always; break-before: page; }
  .grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(230px,1fr)); gap:14px; }
  .card { background: var(--panel); border:1px solid var(--line); border-radius:12px; padding:16px; cursor:pointer;
    transition: transform .12s ease, border-color .12s ease, background .12s ease; }
  .card:hover { transform: translateY(-2px); border-color: var(--red); background: var(--panel2); }
  .card-top { display:flex; align-items:center; gap:12px; }
  .avatar { width:46px; height:46px; border-radius:50%; background: var(--red); display:flex; align-items:center;
    justify-content:center; font-weight:700; font-size:15px; flex-shrink:0; overflow:hidden; }
  .avatar img, .detail-avatar img { width:100%; height:100%; object-fit:cover; border-radius:50%; }
  .card-name { font-weight:700; font-size:15px; line-height:1.25; }
  .card-pos { font-size:11.5px; color:var(--muted); }
  .card-body { margin-top:12px; display:flex; justify-content:space-between; font-size:12.5px; color:var(--muted); }
  .card-body .metric b { color: var(--text); font-size:14px; display:block; }
  .trend-up { color: var(--good); } .trend-down { color: var(--bad); }
  .detail-header { display:flex; gap:16px; align-items:flex-start; flex-wrap:wrap; margin-bottom:16px; }
  .detail-avatar { width:76px; height:76px; border-radius:50%; background: var(--red); flex-shrink:0;
    display:flex; align-items:center; justify-content:center; font-weight:800; font-size:26px; overflow:hidden; }
  .detail-title h2 { margin:0 0 4px; font-size:22px; }
  .detail-title .pos-pill { display:inline-block; background: var(--red); color:#fff; font-size:11px; font-weight:700;
    padding:3px 10px; border-radius:100px; margin-right:8px; letter-spacing:.03em; }
  .bio-row { display:flex; gap:20px; margin-top:8px; flex-wrap:wrap; }
  .bio-item .label { font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:.05em; }
  .bio-item .value { font-size:15px; font-weight:700; }
  .chart-wrap svg { width:100%; height:auto; display:block; }
  .chart-wrap svg circle.pt-hit { cursor:pointer; }
  .chart-tooltip { position:fixed; display:none; background:#1c1d20; border:1px solid var(--line); color:var(--text);
    font-size:12.5px; font-weight:600; padding:6px 10px; border-radius:7px; pointer-events:none; z-index:9999;
    white-space:nowrap; box-shadow:0 6px 18px rgba(0,0,0,.4); }
  @media print { .chart-tooltip { display:none !important; } }
  .metric-hero { display:flex; align-items:baseline; gap:6px; flex-wrap:wrap; margin-bottom:2px; }
  .metric-hero .hero-value { font-size:30px; font-weight:800; color:var(--text); line-height:1; }
  .metric-hero .hero-unit { font-size:13px; font-weight:600; color:var(--muted); }
  .metric-hero .hero-badge { margin-left:auto; font-size:11.5px; font-weight:700; padding:3px 10px; border-radius:100px; }
  .metric-hero .hero-badge.good { background: rgba(62,207,110,0.15); color: var(--good); }
  .metric-hero .hero-badge.bad { background: rgba(229,72,77,0.15); color: var(--bad); }
  .metric-hero .hero-badge.neutral { background: rgba(138,141,148,0.15); color: var(--neutral); }

  .metric-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(215px,1fr)); gap:10px; margin-bottom:14px; }
  .metric-grid .panel { padding:11px 13px; margin-bottom:0; }
  .metric-grid .panel h3 { margin:0 0 6px; font-size:11px; }
  .metric-grid .metric-hero .hero-value { font-size:21px; }
  .metric-grid .metric-hero .hero-unit { font-size:10.5px; }
  .metric-grid .metric-hero .hero-badge { font-size:9.5px; padding:2px 7px; }
  .metric-grid .stat-line { gap:12px; margin-bottom:6px; }
  .metric-grid .stat-line .si { font-size:10px; }
  .metric-grid .stat-line .si b { font-size:11px; }
  .metric-grid .pb-badge { font-size:9px; padding:1px 6px; }
  .stat-line { display:flex; gap:16px; margin-bottom:10px; flex-wrap:wrap; align-items:center; }
  .stat-line .si { font-size:11px; color:var(--muted); }
  .stat-line .si b { color: var(--text); font-size:12.5px; font-weight:700; margin-left:4px; }
  .trait-defs { display:flex; flex-direction:column; gap:7px; }
  .trait-def { font-size:11.5px; color:var(--muted); line-height:1.5; }
  .trait-def b { color:var(--text); font-weight:700; }
  .pb-badge { background: rgba(166,25,46,0.18); color: var(--red); font-size:10px; font-weight:800;
    padding:2px 8px; border-radius:100px; text-transform:uppercase; letter-spacing:.04em; }
  .print-btn { background: rgba(255,255,255,.1); border:1px solid var(--line); color:var(--text);
    padding:8px 14px; border-radius:8px; cursor:pointer; font-size:13px; margin-left:auto; }
  .print-btn:hover { background: rgba(255,255,255,.18); }
  @page { size: letter; margin: 0.35in; }
  @media print {
    header, .toolbar, .print-btn, #backBtn, nav.tabs, .modal-overlay { display:none !important; }
    body { background:#fff; color:#000; font-size:9px; }
    main { padding:0 !important; max-width:none !important; }
    .panel, table.data, .card, .kpi-card { background:#fff; border-color:#bbb; box-shadow:none; }
    body:not(.printing-all) #playerDetail { display:block !important; }
    /* "Print All Player Sheets" mode: show the pre-built multi-player container instead of
       whichever single player happened to be on screen, and hide the roster grid / single
       player view so nothing duplicates or leaks into the printout. */
    body.printing-all #playerDetail, body.printing-all #playersRoster { display:none !important; }
    body.printing-all #printAllContent { display:block !important; }

    /* ---- Header / bio: compact single row ---- */
    .detail-header { margin-bottom:6px; gap:10px; align-items:center; }
    .detail-avatar { width:52px; height:52px; font-size:17px; }
    .detail-title h2 { font-size:16px; margin:0 0 2px; }
    .pos-pill { font-size:8.5px; padding:1px 7px; }
    .bio-row { gap:10px; margin-top:4px; }
    .bio-item .label { font-size:7.5px; }
    .bio-item .value { font-size:11px; }
    .print-logo { height:32px; }

    /* ---- Progress Photos: shrink + tighten so all 4 line up neatly ---- */
    .photo-grid4 { gap:14px; margin-bottom:2px; }
    .pg-cell { width:auto; }
    .pg-cell img, .pg-placeholder { width:62px; height:83px; }
    .pg-placeholder { font-size:6px; padding:4px; }
    .pg-header { font-size:8px; margin-bottom:3px; }
    .pg-tag { font-size:6.5px; margin-bottom:2px; }
    .pg-date { font-size:6.5px; margin-top:3px; }
    .photo-note { display:none; }
    #photoContent { page-break-inside: avoid; }

    /* ---- Character Eval + Weight Trend chart panels: side by side, shrunk charts ---- */
    .panels-2 { gap:8px; margin-bottom:6px; page-break-inside: avoid; }
    .panels-2 .panel { padding:7px 9px; }
    .panels-2 .panel h3 { font-size:9.5px; margin:0 0 3px; }
    .panels-2 .chart-wrap { max-width:230px; margin:0 auto; }
    .trait-defs { font-size:6.5px; margin-top:5px !important; line-height:1.35; }

    /* ---- All 12 test metrics: dense 4-across grid, small charts ---- */
    .metric-head { margin: 6px 0 3px; }
    .metric-head h2 { font-size:10px; }
    /* Start STRENGTH cleanly on its own page rather than letting the heading get orphaned
       at the bottom of the SPEED/BOUNCE page with its grid stranded below the break. */
    .metric-head[data-cat="STRENGTH"] { page-break-before: always; break-before: page; margin-top:0; }
    .metric-grid { display:grid; grid-template-columns: repeat(4, 1fr); gap:6px; margin-bottom:6px; }
    .metric-grid .panel { padding:5px 6px; page-break-inside: avoid; }
    .metric-grid .panel h3 { font-size:8px; margin:0 0 2px; }
    .info-dot { display:none; } /* tooltips are meaningless on paper */
    .metric-desc-sm { display:none; } /* keeps the print sheet within its 1-2 page budget */
    .metric-grid .metric-hero { margin-bottom:0; gap:3px; }
    .metric-grid .metric-hero .hero-value { font-size:15px; }
    .metric-grid .metric-hero .hero-unit { font-size:6.5px; }
    .metric-grid .metric-hero .hero-badge { font-size:6.5px; padding:1px 5px; }
    .metric-grid .stat-line { gap:7px; margin-bottom:2px; }
    .metric-grid .stat-line .si { font-size:6.5px; }
    .metric-grid .stat-line .si b { font-size:7.5px; }
    .metric-grid .pb-badge { font-size:6px; padding:0 4px; }
    .metric-grid .chart-wrap { max-width:100%; }
  }
  .modal-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,.6); z-index:100;
    align-items:center; justify-content:center; padding:20px; }
  .modal-overlay.open { display:flex; }
  .modal-box { background: var(--panel); border:1px solid var(--line); border-radius:14px; padding:24px;
    max-width:440px; width:100%; }
  .modal-box h3 { margin:0 0 8px; font-size:16px; }
  .modal-box p { margin:0 0 16px; font-size:12.5px; color:var(--muted); line-height:1.5; }
  .modal-pw-input { width:100%; background:#151517; border:1px solid var(--line); color:var(--text);
    border-radius:8px; padding:10px 12px; font-size:13px; margin-bottom:14px; box-sizing:border-box; }
  .drop-zone { border:2px dashed var(--line); border-radius:10px; padding:32px 16px; text-align:center;
    font-size:13px; color:var(--muted); cursor:pointer; transition: border-color .12s ease, background .12s ease; }
  .drop-zone.drag-over { border-color: var(--red); background: rgba(166,25,46,0.08); color:var(--text); }
  .drop-zone.disabled { opacity:.45; cursor:not-allowed; }
  .upload-status { font-size:12px; color:var(--muted); margin-top:12px; min-height:16px; }
  .upload-status.pending { color: var(--muted); }
  .upload-status.error { color: var(--bad); }
  .upload-status.success { color: var(--good); }
  .modal-actions { display:flex; justify-content:flex-end; gap:8px; margin-top:16px; }
  .modal-close { background: rgba(255,255,255,.08); border:1px solid var(--line); color:var(--text);
    padding:8px 14px; border-radius:8px; cursor:pointer; font-size:13px; }
  .modal-close:hover { background: rgba(255,255,255,.15); }
  #uploadBtn { background: rgba(255,255,255,.14); color:#fff; border:1px solid rgba(255,255,255,.3);
    padding:8px 14px; border-radius:8px; cursor:pointer; font-size:13px; font-weight:600; }
  #uploadBtn:hover { background: rgba(255,255,255,.25); }
  .data-meta { font-size:10.5px; color: rgba(255,255,255,.55); margin-top:2px; }
  .modal-box.wide { max-width:640px; }
  .review-list { max-height:320px; overflow-y:auto; margin-top:14px; display:flex; flex-direction:column; gap:8px; }
  .review-row { display:flex; align-items:center; gap:10px; background:rgba(255,255,255,.04); border:1px solid var(--line); border-radius:8px; padding:8px 10px; }
  .review-row img { width:44px; height:44px; object-fit:cover; border-radius:6px; flex-shrink:0; }
  .review-row .rf { display:flex; flex-direction:column; gap:4px; flex:1; min-width:0; }
  .review-row .rf-name { font-size:11px; color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .review-row select, .review-row input[type=date] { background:#151517; border:1px solid var(--line); color:var(--text);
    border-radius:6px; padding:5px 7px; font-size:12px; }
  .review-row .rf-fields { display:flex; gap:6px; flex-wrap:wrap; }
  .photo-empty { font-size:12.5px; color:var(--muted); padding:10px 0; }
  .photo-compare { display:flex; gap:16px; flex-wrap:wrap; align-items:flex-start; }
  .photo-compare .pc-item { flex:1; min-width:160px; text-align:center; }
  .photo-compare .pc-item img { width:100%; max-width:280px; border-radius:10px; border:1px solid var(--line); }
  .photo-compare .pc-item .pc-label { font-size:11px; color:var(--red); font-weight:700; text-transform:uppercase; letter-spacing:.06em; margin-bottom:6px; }
  .photo-compare .pc-item .pc-date { font-size:11px; color:var(--muted); margin-top:6px; }
  .photo-note { font-size:10.5px; color:var(--muted); margin-top:10px; text-align:center; }
  .photo-grid4 { display:flex; gap:36px; flex-wrap:wrap; align-items:flex-start; justify-content:center; text-align:center; }
  .pg-group { display:flex; flex-direction:column; align-items:center; }
  .pg-header { font-size:11.5px; color:var(--red); font-weight:800; text-transform:uppercase; letter-spacing:.07em; margin-bottom:7px; text-align:center; }
  .pg-row { display:flex; gap:12px; }
  .pg-cell { display:flex; flex-direction:column; align-items:center; width:210px; }
  .pg-cell img { width:210px; height:280px; object-fit:cover; border-radius:10px; border:1px solid var(--line); }
  .pg-tag { font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.05em; margin-bottom:5px; }
  .pg-date { font-size:11.5px; color:var(--muted); margin-top:6px; }
  .pg-placeholder { width:210px; height:280px; border:1px dashed var(--line); border-radius:10px;
    display:flex; align-items:center; justify-content:center; text-align:center; font-size:11.5px; line-height:1.3; color:var(--muted); padding:10px; }
  .lock-overlay { position:fixed; inset:0; background:#0a0a0b; z-index:500; display:flex; align-items:center; justify-content:center; padding:20px; }
  .lock-box { background: var(--panel); border:1px solid var(--line); border-radius:14px; padding:32px 28px; max-width:340px; width:100%; text-align:center; }
  .lock-box img { width:64px; height:64px; object-fit:contain; margin-bottom:14px; }
  .lock-box h3 { margin:0 0 6px; font-size:17px; }
  .lock-box p { margin:0 0 18px; font-size:12.5px; color:var(--muted); line-height:1.5; }
  .lock-box input[type=password] { width:100%; background:#151517; border:1px solid var(--line); color:var(--text);
    border-radius:8px; padding:10px 12px; font-size:14px; text-align:center; box-sizing:border-box; }
  .lock-box button { width:100%; margin-top:12px; background:var(--red); border:1px solid var(--red); color:#fff;
    padding:10px 12px; border-radius:8px; cursor:pointer; font-size:13.5px; font-weight:700; }
  .lock-box button:hover { background:#8c1526; }
  .lock-error { color:var(--bad); font-size:12px; margin-top:10px; min-height:14px; }
</style>
</head>
<body>

<div class="lock-overlay" id="lockOverlay">
  <div class="lock-box">
    <img src="__LOGO_URI__" alt="Jax State Gamecocks logo">
    <h3>Jax State MBB Dashboard</h3>
    <p>Enter the password to view this dashboard.</p>
    <input type="password" id="lockPassword" placeholder="Password" autocomplete="off">
    <button onclick="tryUnlock()">Unlock</button>
    <div class="lock-error" id="lockError"></div>
  </div>
</div>

<div id="appContent" style="display:none;">
<header>
  <div class="header-top">
    <div class="header-brand">
      <div class="logo-badge"><img class="header-logo" src="__LOGO_URI__" alt="Jax State Gamecocks logo"></div>
      <div>
        <h1>Jax State MBB</h1>
        <div class="sub" id="headerSub">Performance Dashboard · 2026–27</div>
        <div class="data-meta" id="dataMeta"></div>
      </div>
    </div>
    <div style="display:flex; gap:8px;">
      <button id="uploadBtn" onclick="openUploadModal()">Update Data</button>
      <button id="backBtn" onclick="showRoster()">&larr; Back to Roster</button>
    </div>
  </div>
  <nav class="tabs" id="tabNav">
    <button data-tab="dashboard" class="active">Dashboard</button>
    <button data-tab="speed">Speed</button>
    <button data-tab="bounce">Bounce</button>
    <button data-tab="strength">Strength</button>
    <button data-tab="fitness">Fitness</button>
    <button data-tab="character">Character</button>
    <button data-tab="players">Players</button>
  </nav>
</header>

<main>
  <div class="view active" id="view-dashboard">
    <div class="kpi-row" id="kpiDashboard"></div>
    <div class="panels-2">
      <div class="panel"><h3>CMJ — Ranked (cm)</h3><div id="bar-vert"></div></div>
      <div class="panel"><h3>3 Step MPH — Ranked</h3><div id="bar-3stepmph"></div></div>
      <div class="panel"><h3>TBDL — Ranked (lb)</h3><div id="bar-tbdl"></div></div>
      <div class="panel"><h3>Weight Change — Ranked (lb)</h3><div id="bar-weightchange"></div></div>
      <div class="panel"><h3>Body Fat — Most Recent (%)</h3><div id="bar-bodyfat"></div></div>
      <div class="panel"><h3>Lean Mass — Most Recent (lb)</h3><div id="bar-leanmass"></div></div>
    </div>
    <div class="metric-head"><h2>Team Roster — click a name for the full player dashboard</h2></div>
    <div class="table-wrap"><table class="data" id="table-roster"></table></div>
  </div>

  <div class="view" id="view-speed"><div class="kpi-row" id="kpiSpeed"></div><div id="sections-speed"></div></div>
  <div class="view" id="view-bounce"><div class="kpi-row" id="kpiBounce"></div><div id="sections-bounce"></div></div>
  <div class="view" id="view-strength"><div class="kpi-row" id="kpiStrength"></div><div id="sections-strength"></div></div>
  <div class="view" id="view-fitness"><div class="kpi-row" id="kpiFitness"></div><div id="sections-fitness"></div></div>

  <div class="view" id="view-character">
    <div class="kpi-row" id="kpiCharacter"></div>
    <div class="panel"><h3>What each trait means (1–5 scale)</h3><div class="trait-defs" id="traitDefsMain"></div></div>
    <div class="table-wrap"><table class="data" id="table-character"></table></div>
  </div>

  <div class="view" id="view-players">
    <div id="playersRoster">
      <div class="toolbar">
        <input id="search" type="text" placeholder="Search player name..." oninput="renderGrid()">
        <select id="posFilter" onchange="renderGrid()">
          <option value="">All Positions</option><option value="G">Guards</option><option value="F">Forwards</option>
        </select>
        <select id="sortBy" onchange="renderGrid()">
          <option value="name">Sort: Name</option><option value="weight">Sort: Current Weight</option>
          <option value="vert">Sort: CMJ</option><option value="bench">Sort: Bench 1RM</option>
          <option value="workEthic">Sort: Work Ethic</option>
        </select>
        <button id="printAllBtn" onclick="printAllPlayers()">Print All Player Sheets</button>
      </div>
      <div class="grid" id="grid"></div>
    </div>
    <div id="playerDetail" style="display:none;">
      <div class="detail-header">
        <div class="detail-avatar" id="dAvatar"></div>
        <div class="detail-title">
          <h2 id="dName"></h2>
          <div><span class="pos-pill" id="dPos"></span></div>
          <div class="bio-row">
            <div class="bio-item"><div class="label">Height</div><div class="value" id="dHeight"></div></div>
            <div class="bio-item"><div class="label">Starting Weight</div><div class="value" id="dStartWeight"></div></div>
            <div class="bio-item"><div class="label">Current Weight</div><div class="value" id="dCurWeight"></div></div>
            <div class="bio-item"><div class="label">Weight Change</div><div class="value" id="dWeightChange"></div></div>
          </div>
        </div>
        <img class="print-logo" src="__LOGO_URI__" alt="Jax State Gamecocks logo">
        <button class="print-btn" onclick="window.print()">Print Player Sheet</button>
      </div>
      <div class="panel"><h3>Progress Photos</h3><div id="photoContent"></div></div>
      <div class="panels-2">
        <div class="panel"><h3>Character Evaluation (1–5)</h3><div class="chart-wrap" id="charChart"></div>
          <div class="trait-defs" id="traitDefsPlayer" style="margin-top:12px;"></div>
        </div>
        <div class="panel"><h3>Body Weight Trend (lb)</h3><div class="chart-wrap" id="weightChart"></div></div>
      </div>
      <div id="metricSections"></div>
    </div>
    <div id="printAllContent" style="display:none;"></div>
  </div>
</main>

<div class="modal-overlay" id="uploadModal">
  <div class="modal-box">
    <h3>Update dashboard data</h3>
    <p>Enter the dashboard password, then drop your JAX ST MBB DATA spreadsheet (.xlsx) below. This updates what you see immediately, and publishes the update for everyone else within about a minute.</p>
    <input type="password" id="publishPassword" class="modal-pw-input" placeholder="Dashboard password" autocomplete="off">
    <div class="drop-zone" id="dropZone">Drag &amp; drop the .xlsx file here<br>or click to browse</div>
    <input type="file" id="fileInput" accept=".xlsx" style="display:none;">
    <div class="upload-status" id="uploadStatus"></div>
    <div class="modal-actions">
      <button class="modal-close" onclick="closeUploadModal()">Close</button>
    </div>
  </div>
</div>

<div class="modal-overlay" id="photoModal">
  <div class="modal-box wide">
    <h3>Upload progress photos</h3>
    <p>Drag in a batch of player photos — front &amp; back, before &amp; after. Name each file like <b>LastName_FirstName_front_YYYY-MM-DD.jpg</b> (e.g. "Cunningham_Naas_front_2026-07-01.jpg", "...back_2026-07-01.jpg") and the player, angle &amp; date will be guessed automatically — just double-check the guesses below before saving. Photos are stored only in this browser.</p>
    <div class="drop-zone" id="photoDropZone">Drag &amp; drop photos here<br>or click to browse</div>
    <input type="file" id="photoFileInput" accept="image/*" multiple style="display:none;">
    <div class="review-list" id="photoReviewList"></div>
    <div class="upload-status" id="photoStatus"></div>
    <div class="modal-actions">
      <button class="modal-close" onclick="closePhotoModal()">Close</button>
      <button id="savePhotosBtn" class="modal-close" style="display:none; background:var(--red); border-color:var(--red);" onclick="commitPhotoReview()">Save Photos</button>
    </div>
  </div>
</div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<script>
const PW_HASH = '88e06b2fe6f9a4a2dbe33ff8e656a0ff55d7289fba533c6c8d6a24deeb1dce54';
let __dashboardInitialized = false;

// Pure-JS SHA-256 (no Web Crypto / crypto.subtle dependency). crypto.subtle only works in a
// "secure context", and file:// pages opened directly (as this dashboard is, when emailed or
// AirDropped) don't reliably count as secure in every browser - Safari in particular can leave
// crypto.subtle undefined there, silently breaking the password screen for whoever you shared
// this with. This standalone implementation works identically in any browser, any context.
function sha256Hex(str){
  function rightRotate(v, n) { return (v >>> n) | (v << (32 - n)); }
  const maxWord = Math.pow(2, 32);
  const words = [];
  const asciiBitLength = str.length * 8;
  let hash = [], k = [];
  let primeCounter = 0;
  const isComposite = {};
  for (let candidate = 2; primeCounter < 64; candidate++) {
    if (!isComposite[candidate]) {
      for (let i = 0; i < 313; i += candidate) isComposite[i] = candidate;
      hash[primeCounter] = (Math.pow(candidate, 0.5) * maxWord) | 0;
      k[primeCounter++] = (Math.pow(candidate, 1 / 3) * maxWord) | 0;
    }
  }
  str += '\x80';
  while (str.length % 64 - 56) str += '\x00';
  for (let i = 0; i < str.length; i++) {
    const j = str.charCodeAt(i);
    words[i >> 2] |= j << ((3 - i) % 4) * 8;
  }
  words[words.length] = (asciiBitLength / maxWord) | 0;
  words[words.length] = asciiBitLength;
  for (let j = 0; j < words.length;) {
    const w = words.slice(j, j += 16);
    const oldHash = hash.slice(0);
    hash = hash.slice(0, 8);
    for (let i = 0; i < 64; i++) {
      const w15 = w[i - 15], w2 = w[i - 2];
      const a = hash[0], e = hash[4];
      const temp1 = hash[7] +
        (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) +
        ((e & hash[5]) ^ (~e & hash[6])) +
        k[i] +
        (w[i] = (i < 16) ? w[i] : (
          w[i - 16] +
          (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3)) +
          w[i - 7] +
          (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))
        ) | 0);
      const temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) +
        ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
      hash = [(temp1 + temp2) | 0].concat(hash);
      hash[4] = (hash[4] + temp1) | 0;
    }
    for (let i = 0; i < 8; i++) hash[i] = (hash[i] + oldHash[i]) | 0;
  }
  let result = '';
  for (let i = 0; i < 8; i++) result += ((hash[i] >>> 0) + 0x100000000).toString(16).substr(1);
  return result;
}

async function tryUnlock(){
  const input = document.getElementById('lockPassword');
  const errEl = document.getElementById('lockError');
  const pw = input.value || '';
  let hash = '';
  try {
    hash = await sha256Hex(pw);
  } catch(e) {
    errEl.textContent = 'Unable to verify password in this browser.';
    return;
  }
  if (hash === PW_HASH) {
    document.getElementById('lockOverlay').style.display = 'none';
    document.getElementById('appContent').style.display = '';
    initDashboard();
  } else {
    errEl.textContent = 'Incorrect password. Try again.';
    input.value = '';
    input.focus();
  }
}

(function wireLockScreenInput(){
  const pwInput = document.getElementById('lockPassword');
  if (pwInput) {
    pwInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') tryUnlock(); });
    pwInput.focus();
  }
})();

const STORAGE_KEY = 'jaxst_mbb_dashboard_data_v1';
const BUILD_TIME = '__BUILD_TIME__'; // ISO timestamp of when THIS file was generated
const EMBEDDED_DATA = __DATA_JSON__;
let DATA = EMBEDDED_DATA;
let dataSavedAt = null;
let savedDataWasIncompatible = false;
let savedDataWasStale = false;
try {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    const parsed = JSON.parse(saved);
    if (parsed && parsed.data && parsed.data.order && parsed.data.players) {
      // Guard against a schema mismatch: if a metric was renamed/added since this browser last
      // saved data (e.g. Vertical Jump -> CMJ, or a new Peak Power test), the saved snapshot won't
      // have those metric keys and every lookup against them would throw, silently blanking the
      // whole page. Only trust the saved snapshot if it has every metric the current template expects.
      const expectedMetrics = Object.keys(EMBEDDED_DATA.metricMeta || {});
      const savedMetrics = new Set(Object.keys((parsed.data.metricMeta) || {}));
      const compatible = expectedMetrics.every(m => savedMetrics.has(m));
      // Guard against staleness: every time this dashboard file is regenerated with corrected/updated
      // numbers, it carries a fresh BUILD_TIME. A browser's saved snapshot should only win over the
      // freshly-embedded data if the USER re-uploaded a spreadsheet in this browser AFTER that point
      // (i.e. savedAt is later than this build). Otherwise the snapshot is old news and the newly
      // shipped built-in data should be shown instead - this is what silently caused "missing"/dash
      // values for players whose data was corrected after the browser's cached copy was saved.
      const isFresh = !!(parsed.savedAt && parsed.savedAt > BUILD_TIME);
      if (compatible && isFresh) {
        DATA = parsed.data;
        dataSavedAt = parsed.savedAt || null;
      } else {
        if (!compatible) savedDataWasIncompatible = true;
        else if (!isFresh) savedDataWasStale = true;
      }
    }
  }
} catch(e) {}
let players = DATA.players;
let order = DATA.order;
let metricMeta = DATA.metricMeta;
const RED = '#A6192E';

const PHOTOS_KEY = 'jaxst_mbb_dashboard_photos_v1';
const EMBEDDED_PHOTOS = __PHOTOS_JSON__;
let PHOTOS = EMBEDDED_PHOTOS;
try {
  const savedPhotos = localStorage.getItem(PHOTOS_KEY);
  if (savedPhotos) PHOTOS = JSON.parse(savedPhotos) || {};
} catch(e) {}
let photoReviewQueue = [];
let photoIdCounter = 0;

const HEADSHOTS = __HEADSHOTS_JSON__;
function avatarHtml(name){
  const src = HEADSHOTS[name];
  if (src) return `<img src="${src}" alt="${name}">`;
  return initials(name);
}

const METRIC_ORDER = {
  SPEED: ['10 Yard Sprint','Peak Power','MPH by Step 3'],
  BOUNCE: ['CMJ','RSI','Approach Jump'],
  STRENGTH: ['TBDL 1RM (.4m/s)','Bench 1RM','Chin Up Max Reps'],
  FITNESS: ['Body Fat','Lean Mass','Celtic Test'],
};

const COMBO_WEIGHTS = {};

const TRAIT_DEFS = [
  { key:'workEthic', label:'Work Ethic', def:'Gives great effort. Gives more than expected.' },
  { key:'consistency', label:'Consistency', def:'Reliable in their performance, effort, and mindset.' },
  { key:'coachability', label:'Coachability', def:'Receptive to feedback, craves instruction.' },
  { key:'attitude', label:'Attitude', def:'Contagious enthusiasm. Willing to rise to any challenge. Body language is excited and present.' },
  { key:'toughness', label:'Toughness', def:'Never complains. Does not make excuses, seeks challenge.' },
];

function renderTraitDefs(containerId){
  document.getElementById(containerId).innerHTML = TRAIT_DEFS.map(t =>
    `<div class="trait-def"><b>${t.label}</b> — ${t.def}</div>`
  ).join('');
}

function initials(name){ const [last,first]=name.split(',').map(s=>s.trim()); return (first?first[0]:'')+(last?last[0]:''); }
function shortName(name){ const [last,first]=name.split(',').map(s=>s.trim()); return (first?first[0]+'. ':'')+last; }
function lastVal(arr){ for(let i=arr.length-1;i>=0;i--) if(arr[i]!=null) return arr[i]; return null; }
function fmtNum(v, unit, decimals){
  if (v===null||v===undefined) return null;
  let d = decimals!==undefined ? decimals : (unit==='%'?1:2);
  let out = unit==='%' ? (v*100).toFixed(1)+'%' : (Number.isInteger(v)?String(v):v.toFixed(d));
  if (unit && unit!=='%') out += ' '+unit;
  return out;
}
// Like fmtNum but never appends a unit suffix (used where the unit is shown separately, e.g. hero-value + hero-unit)
function fmtNumBare(v, unit, decimals){
  if (v===null||v===undefined) return null;
  let d = decimals!==undefined ? decimals : (unit==='%'?1:2);
  return unit==='%' ? (v*100).toFixed(1) : (Number.isInteger(v)?String(v):v.toFixed(d));
}
function avg(arr){ const a=arr.filter(v=>v!=null); return a.length? a.reduce((x,y)=>x+y,0)/a.length : null; }
function curWeight(p){ return lastVal(p.weights); }
function weightChange(p){ const c=curWeight(p); return (c!=null && p.startWeight!=null) ? c-p.startWeight : null; }
function compositeChar(p){ if(!p.character) return null; const vals=Object.values(p.character).filter(v=>v!=null); return vals.length? vals.reduce((a,b)=>a+b,0)/vals.length : null; }
function kpiCard(label, value, caption){ return `<div class="kpi-card"><div class="label">${label}</div><div class="value">${value}</div><div class="caption">${caption||''}</div></div>`; }

function goToPlayer(name){
  document.querySelectorAll('nav.tabs button').forEach(b=>b.classList.remove('active'));
  document.querySelector('nav.tabs button[data-tab="players"]').classList.add('active');
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.getElementById('view-players').classList.add('active');
  showDetail(name);
}

/* ---------- ranked horizontal bar chart ----------
   By default tiers by quartile (top 25% green / middle 50% yellow / bottom 25% red).
   Pass a `thresholdFn` (value => 'tier-green'|'tier-yellow'|'tier-red') to use fixed
   cutoffs instead (e.g. weight change: >=5 green, 0-4.9 yellow, <0 red). */
function renderRankedBar(containerId, rows, unit, decimals, direction, thresholdFn){
  direction = direction || 'high';
  const withVal = rows.filter(r=>r.value!=null);
  const withoutVal = rows.filter(r=>r.value==null);
  withVal.sort((a,b) => direction==='low' ? a.value-b.value : b.value-a.value);
  const n = withVal.length;
  const topCount = Math.ceil(n * 0.25);
  const botCount = Math.ceil(n * 0.25);
  const maxV = Math.max(...rows.map(r=>Math.abs(r.value||0)), 0.0001);

  const barRow = (r, tierClass) => {
    const pct = Math.max(2, (Math.abs(r.value||0)/maxV)*100);
    const valStr = r.value==null ? '—' : fmtNum(r.value, unit, decimals);
    return `<div class="bar-row">
      <div class="bar-name" onclick="goToPlayer('${r.name.replace(/'/g,"\\'")}')">${shortName(r.name)}</div>
      <div class="bar-track"><div class="bar-fill ${tierClass}" style="width:${pct}%"></div></div>
      <div class="bar-val">${valStr}</div>
    </div>`;
  };

  const rowsHtml = withVal.map((r, idx) => {
    let tierClass;
    if (thresholdFn) {
      tierClass = thresholdFn(r.value);
    } else if (idx < topCount) tierClass = 'tier-green';
    else if (idx >= n - botCount) tierClass = 'tier-red';
    else tierClass = 'tier-yellow';
    return barRow(r, tierClass);
  }).join('') + withoutVal.map(r => barRow(r, 'tier-gray')).join('');

  document.getElementById(containerId).innerHTML = rowsHtml;
}

/* ---------- sparkline (compact inline SVG) ---------- */
function sparkline(values, unit){
  const nums = values.map((v,i)=>({v,i})).filter(o=>o.v!=null);
  if (nums.length === 0) return '<span class="na">—</span>';
  if (nums.length === 1) {
    return `<svg width="70" height="26" viewBox="0 0 70 26"><circle cx="35" cy="13" r="3" fill="${RED}"/></svg>`;
  }
  const w=70,h=26,pad=4;
  let minV=Math.min(...nums.map(o=>o.v)), maxV=Math.max(...nums.map(o=>o.v));
  if (minV===maxV){ minV-=1; maxV+=1; }
  const xFor = i => pad + (i/(values.length-1))*(w-2*pad);
  const yFor = v => pad + (h-2*pad) - ((v-minV)/(maxV-minV))*(h-2*pad);
  const d = nums.map((o,idx)=> (idx===0?'M':'L') + xFor(o.i).toFixed(1)+','+yFor(o.v).toFixed(1)).join(' ');
  const last = nums[nums.length-1];
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
    <path d="${d}" fill="none" stroke="${RED}" stroke-width="2"/>
    <circle cx="${xFor(last.i).toFixed(1)}" cy="${yFor(last.v).toFixed(1)}" r="2.6" fill="${RED}"/>
  </svg>`;
}

/* ---------- generic sortable table ---------- */
let tblCounter = 0;
function buildTable(containerId, columns, rows, defaultKey, defaultDir){
  const fnName = '__tblSort_' + (containerId.replace(/[^a-zA-Z0-9]/g,'_')) + '_' + (tblCounter++);
  let state = { key: defaultKey, dir: defaultDir || 'desc' };
  function renderHead(){
    return '<tr>' + columns.map(c=>{
      const sorted = c.key===state.key;
      const arrow = sorted ? (state.dir==='asc' ? '&uarr;' : '&darr;') : '';
      const cls = [sorted?'sorted':'', c.numeric?'num':''].filter(Boolean).join(' ');
      return c.sortable===false
        ? `<th class="${cls}">${c.label}</th>`
        : `<th class="${cls}" onclick="${fnName}('${c.key}')">${c.label}<span class="arrow">${arrow}</span></th>`;
    }).join('') + '</tr>';
  }
  function renderBody(){
    const sorted = [...rows].sort((a,b)=>{
      let va=a[state.key], vb=b[state.key];
      if (va==null && vb==null) return 0;
      if (va==null) return 1; if (vb==null) return -1;
      if (typeof va === 'string') return state.dir==='asc' ? va.localeCompare(vb) : vb.localeCompare(va);
      return state.dir==='asc' ? va-vb : vb-va;
    });
    return sorted.map(r=>'<tr>' + columns.map(c=>{
      const raw = r[c.key];
      const display = c.format ? c.format(raw, r) : (raw==null ? '<span class="na">—</span>' : raw);
      return `<td class="${c.numeric?'num':''} ${c.key==='name'?'name':''} ${c.trend?'trend':''}">${display}</td>`;
    }).join('') + '</tr>').join('');
  }
  function render(){ document.getElementById(containerId).innerHTML = `<thead>${renderHead()}</thead><tbody>${renderBody()}</tbody>`; }
  window[fnName] = function(key){
    if (state.key===key) state.dir = state.dir==='asc' ? 'desc':'asc';
    else { state.key=key; state.dir='desc'; }
    render();
  };
  render();
}

function vsAvgHtml(current, teamAvg, direction, unit){
  if (current==null || teamAvg==null) return '<span class="na">n/a</span>';
  const diff = current - teamAvg;
  const better = direction==='low' ? diff<0 : diff>0;
  const cls = Math.abs(diff)<1e-9 ? 'vs-neutral' : (better?'vs-good':'vs-bad');
  let shown = unit==='%' ? (diff*100).toFixed(1)+'pt' : diff.toFixed(2);
  const sign = diff>0 ? '+' : '';
  return `<span class="${cls}">${sign}${shown}</span>`;
}

function vsAvgBadge(current, teamAvg, direction, unit){
  if (current==null || teamAvg==null) return '<span class="hero-badge neutral">no team avg yet</span>';
  const diff = current - teamAvg;
  const better = direction==='low' ? diff<0 : diff>0;
  const cls = Math.abs(diff)<1e-9 ? 'neutral' : (better?'good':'bad');
  const arrow = Math.abs(diff)<1e-9 ? '' : (diff>0?'&uarr; ':'&darr; ');
  let shown = unit==='%' ? Math.abs(diff*100).toFixed(1)+'pt' : Math.abs(diff).toFixed(2);
  return `<span class="hero-badge ${cls}">${arrow}${shown} vs team avg</span>`;
}

/* ---------- generic team metric section (used by Speed/Bounce/Strength/Fitness tabs) ---------- */
function renderMetricSection(containerId, metricLabel){
  const meta = metricMeta[metricLabel];
  const dates = meta.dates;
  const container = document.getElementById(containerId);
  const block = document.createElement('div');
  block.className = 'metric-block';

  const firsts = order.map(n=>players[n].metrics[metricLabel].first).filter(v=>v!=null);
  const bests = order.map(n=>players[n].metrics[metricLabel].best).filter(v=>v!=null);

  let statsHtml = `<div class="metric-head"><h2>${metricLabel}</h2><span class="unit-note">${dates.length} test date${dates.length===1?'':'s'} recorded${dates.length?': '+dates.join(', '):''}</span></div>`;
  if (meta.description) statsHtml += `<div class="metric-desc">${meta.description}</div>`;
  statsHtml += `<div class="kpi-row">
    ${kpiCard('Avg First', firsts.length?fmtNum(avg(firsts),meta.unit):'—','earliest test')}
    ${kpiCard('Avg Best', bests.length?fmtNum(avg(bests),meta.unit):'—','best recorded')}
  </div>`;

  const tableId = containerId + '-table-' + metricLabel.replace(/[^a-zA-Z0-9]/g,'');
  statsHtml += `<div class="table-wrap"><table class="data" id="${tableId}"></table></div>`;

  block.innerHTML = statsHtml;
  container.appendChild(block);

  const rows = order.map(n=>{
    const p = players[n], m = p.metrics[metricLabel];
    const row = { name: p.name, pos: p.pos, best: m.best, _series: m.series };
    dates.forEach((d,i)=>{ row['d'+i] = m.series[i]; });
    return row;
  });
  const columns = [
    { key:'name', label:'Athlete', format:(v,r)=>`<a class="player-link" onclick="goToPlayer('${r.name.replace(/'/g,"\\'")}')">${v}</a>` },
    { key:'pos', label:'Pos' },
  ];
  dates.forEach((d,i)=>{
    columns.push({ key:'d'+i, label:d, numeric:true, format:v=>v!=null?fmtNum(v,meta.unit):'<span class="na">—</span>' });
  });
  columns.push({ key:'best', label:'Best', numeric:true, format:v=>v!=null?fmtNum(v,meta.unit):'<span class="na">—</span>' });
  columns.push({ key:'trend', label:'Trend', sortable:false, trend:true, format:(v,r)=>sparkline(r._series) });
  buildTable(tableId, columns, rows, dates.length ? 'd'+(dates.length-1) : 'best', 'desc');
}

/* ---------- one combined ranked chart per tab, comparing all metrics in that category ---------- */
const COMBO_COLORS = ['#A6192E', '#4C8BF5', '#A855F7'];

function renderCombinedRankedChart(containerId, metricsInCat, weightsMap){
  const stats = metricsInCat.map(m => {
    const meta = metricMeta[m];
    const vals = order.map(n=>players[n].metrics[m].best).filter(v=>v!=null);
    const teamMin = vals.length ? Math.min(...vals) : 0;
    const teamMax = vals.length ? Math.max(...vals) : 1;
    const weight = (weightsMap && weightsMap[m]) ? weightsMap[m] : 1;
    return { label:m, unit:meta.unit, direction:meta.direction, teamMin, teamMax, weight };
  });

  function normFor(stat, value){
    if (value==null) return null;
    const range = stat.teamMax - stat.teamMin;
    if (range === 0) return 100;
    return stat.direction==='low' ? ((stat.teamMax-value)/range)*100 : ((value-stat.teamMin)/range)*100;
  }

  const rows = order.map(n => {
    const p = players[n];
    const parts = stats.map(stat => {
      const raw = p.metrics[stat.label].best;
      return { label: stat.label, raw, norm: normFor(stat, raw), weight: stat.weight };
    });
    const validParts = parts.filter(x=>x.norm!=null);
    const weightSum = validParts.reduce((a,x)=>a+x.weight,0);
    const composite = weightSum ? validParts.reduce((a,x)=>a+x.norm*x.weight,0)/weightSum : null;
    return { name:n, parts, composite };
  });
  rows.sort((a,b) => (b.composite ?? -1) - (a.composite ?? -1));

  const legend = `<div class="combo-legend">${stats.map((s,i)=>`<span><i style="background:${COMBO_COLORS[i]}"></i>${s.label} (best)${s.weight!==1?' &middot; &times;'+s.weight+' weight':''}</span>`).join('')}</div>`;

  const rowsHtml = rows.map(r => {
    const lines = r.parts.map((part,i) => {
      const pct = part.norm==null ? 0 : Math.max(2, part.norm);
      const valStr = part.raw==null ? '—' : fmtNum(part.raw, stats[i].unit);
      return `<div class="combo-bar-line">
        <i class="dot" style="background:${COMBO_COLORS[i]}"></i>
        <div class="track"><div class="fill" style="width:${pct}%; background:${COMBO_COLORS[i]}"></div></div>
        <span class="val">${valStr}</span>
      </div>`;
    }).join('');
    return `<div class="combo-row">
      <div class="combo-name" onclick="goToPlayer('${r.name.replace(/'/g,"\\'")}')">${shortName(r.name)}</div>
      <div class="combo-bars">${lines}</div>
    </div>`;
  }).join('');

  document.getElementById(containerId).innerHTML = legend + rowsHtml;
}

function renderTeamTab(containerId, kpiId, category){
  document.getElementById(containerId).innerHTML = '';
  const metricsInCat = METRIC_ORDER[category];
  // top-level kpi row: avg current for each metric in category (falls back to best if no recent test logged yet)
  document.getElementById(kpiId).innerHTML = metricsInCat.map(m=>{
    const meta = metricMeta[m];
    const currents = order.map(n=>players[n].metrics[m].current ?? players[n].metrics[m].best).filter(v=>v!=null);
    return kpiCard('Avg ' + m, currents.length? fmtNum(avg(currents), meta.unit) : '—', meta.direction==='low' ? 'lower is better' : 'higher is better');
  }).join('');

  const comboId = containerId + '-combo';
  document.getElementById(containerId).innerHTML = `<div class="panel"><h3>${category} — Combined Ranking (best recorded)</h3><div id="${comboId}"></div></div>`;
  renderCombinedRankedChart(comboId, metricsInCat, COMBO_WEIGHTS[category]);

  metricsInCat.forEach(m => renderMetricSection(containerId, m));
}

/* ================= DASHBOARD TAB ================= */
function renderDashboard(){
  // Fall back to the last real result when a player missed only the very latest test date,
  // rather than showing a dash/skewing the average (same fix applied to the roster card and
  // individual player hero values).
  const curOrLast = m => (m.current!=null ? m.current : lastVal(m.series));

  const verts = order.map(n=>curOrLast(players[n].metrics['CMJ'])).filter(v=>v!=null);
  const mph3 = order.map(n=>curOrLast(players[n].metrics['MPH by Step 3'])).filter(v=>v!=null);
  const weights = order.map(n=>curWeight(players[n])).filter(v=>v!=null);
  const weightChanges = order.map(n=>weightChange(players[n])).filter(v=>v!=null);
  const tbdl = order.map(n=>players[n].metrics['TBDL 1RM (.4m/s)'].best).filter(v=>v!=null);
  const bodyFat = order.map(n=>curOrLast(players[n].metrics['Body Fat'])).filter(v=>v!=null);
  const leanMass = order.map(n=>curOrLast(players[n].metrics['Lean Mass'])).filter(v=>v!=null);

  document.getElementById('kpiDashboard').innerHTML = [
    kpiCard('Avg CMJ', verts.length?avg(verts).toFixed(1)+' cm':'—', 'most recent test'),
    kpiCard('Avg 3 Step MPH', mph3.length?avg(mph3).toFixed(1)+' mph':'—', 'most recent test'),
    kpiCard('Avg TBDL', tbdl.length?avg(tbdl).toFixed(0)+' lb':'—', '.4 m/s velocity based'),
    kpiCard('Avg Weight Change', weightChanges.length?(avg(weightChanges)>=0?'+':'')+avg(weightChanges).toFixed(1)+' lb':'—', 'since start weight'),
    kpiCard('Avg Body Fat', bodyFat.length?(avg(bodyFat)*100).toFixed(1)+'%':'—', 'most recent test'),
    kpiCard('Avg Lean Mass', leanMass.length?avg(leanMass).toFixed(1)+' lb':'—', 'most recent test'),
  ].join('');

  renderRankedBar('bar-vert', order.map(n=>({name:n,value:players[n].metrics['CMJ'].best})), 'cm', undefined, 'high');
  renderRankedBar('bar-3stepmph', order.map(n=>({name:n,value:players[n].metrics['MPH by Step 3'].best})), 'mph', 1, 'high');
  renderRankedBar('bar-tbdl', order.map(n=>({name:n,value:players[n].metrics['TBDL 1RM (.4m/s)'].best})), 'lb', 0, 'high', function(v){
    if (v >= 500) return 'tier-green';
    if (v >= 400) return 'tier-yellow';
    return 'tier-red';
  });
  renderRankedBar('bar-weightchange', order.map(n=>({name:n,value:weightChange(players[n])})), 'lb', 1, 'high', function(v){
    if (v >= 5) return 'tier-green';
    if (v >= 0) return 'tier-yellow';
    return 'tier-red';
  });
  renderRankedBar('bar-bodyfat', order.map(n=>({name:n,value:curOrLast(players[n].metrics['Body Fat'])})), '%', 1, 'low');
  renderRankedBar('bar-leanmass', order.map(n=>({name:n,value:curOrLast(players[n].metrics['Lean Mass'])})), 'lb', 0, 'high');

  const rows = order.map(n=>{
    const p = players[n];
    return { name:p.name, pos:p.pos, height:p.height, weight: curWeight(p),
      vert: p.metrics['CMJ'].current, bench: p.metrics['Bench 1RM'].best };
  });
  buildTable('table-roster', [
    { key:'name', label:'Athlete', format:(v,r)=>`<a class="player-link" onclick="goToPlayer('${r.name.replace(/'/g,"\\'")}')">${v}</a>` },
    { key:'pos', label:'Pos' },
    { key:'height', label:'Height' },
    { key:'weight', label:'Weight', numeric:true, format:v=>v!=null?v.toFixed(1)+' lb':'<span class="na">—</span>' },
    { key:'vert', label:'CMJ', numeric:true, format:v=>v!=null?v.toFixed(1)+' cm':'<span class="na">—</span>' },
    { key:'bench', label:'Bench 1RM', numeric:true, format:v=>v!=null?v.toFixed(0)+' lb':'<span class="na">—</span>' },
  ], rows, 'name', 'asc');
}

/* ================= CHARACTER TAB ================= */
function renderCharacter(){
  const traits = ['workEthic','consistency','coachability','attitude','toughness'];
  const traitAvg = t => avg(order.map(n=>players[n].character ? players[n].character[t] : null));
  document.getElementById('kpiCharacter').innerHTML = [
    kpiCard('Avg Work Ethic', traitAvg('workEthic').toFixed(1)+' / 5', ''),
    kpiCard('Avg Consistency', traitAvg('consistency').toFixed(1)+' / 5', ''),
    kpiCard('Avg Coachability', traitAvg('coachability').toFixed(1)+' / 5', ''),
    kpiCard('Avg Attitude', traitAvg('attitude').toFixed(1)+' / 5', ''),
    kpiCard('Avg Toughness', traitAvg('toughness').toFixed(1)+' / 5', ''),
  ].join('');
  renderTraitDefs('traitDefsMain');
  const rows = order.map(n=>{
    const p = players[n], c = p.character || {};
    return { name:p.name, pos:p.pos, workEthic:c.workEthic, consistency:c.consistency, coachability:c.coachability,
      attitude:c.attitude, toughness:c.toughness, composite: compositeChar(p) };
  });
  const fInt = v => v!=null ? v : '<span class="na">—</span>';
  buildTable('table-character', [
    { key:'name', label:'Athlete', format:(v,r)=>`<a class="player-link" onclick="goToPlayer('${r.name.replace(/'/g,"\\'")}')">${v}</a>` },
    { key:'pos', label:'Pos' },
    { key:'workEthic', label:'Work Ethic', numeric:true, format:fInt },
    { key:'consistency', label:'Consistency', numeric:true, format:fInt },
    { key:'coachability', label:'Coachability', numeric:true, format:fInt },
    { key:'attitude', label:'Attitude', numeric:true, format:fInt },
    { key:'toughness', label:'Toughness', numeric:true, format:fInt },
    { key:'composite', label:'Composite', numeric:true, format:v=>v!=null?v.toFixed(1):'<span class="na">—</span>' },
  ], rows, 'composite', 'desc');
}

/* ================= PLAYERS TAB ================= */
function renderGrid(){
  const q = document.getElementById('search').value.toLowerCase();
  const pos = document.getElementById('posFilter').value;
  const sortBy = document.getElementById('sortBy').value;
  let list = order.map(n=>players[n]).filter(p=>{
    if (pos && p.pos!==pos) return false;
    if (q && !p.name.toLowerCase().includes(q)) return false;
    return true;
  });
  const val = (p,key)=>{
    if (key==='name') return p.name;
    if (key==='weight') return curWeight(p) ?? -Infinity;
    if (key==='vert') return lastVal(p.metrics['CMJ'].series) ?? -Infinity;
    if (key==='bench') return p.metrics['Bench 1RM'].best ?? -Infinity;
    if (key==='workEthic') return p.character.workEthic ?? -Infinity;
  };
  list.sort((a,b)=>{ const va=val(a,sortBy), vb=val(b,sortBy); if (sortBy==='name') return va.localeCompare(vb); return vb-va; });
  document.getElementById('grid').innerHTML = list.map(p=>{
    const cw = curWeight(p); const change = weightChange(p);
    const changeHtml = change==null ? '<span class="na">—</span>' : (change>=0?`<span class="trend-up">+${change.toFixed(1)} lb</span>`:`<span class="trend-down">${change.toFixed(1)} lb</span>`);
    const vert = lastVal(p.metrics['CMJ'].series);
    return `<div class="card" onclick="showDetailFromRoster('${p.name.replace(/'/g,"\\'")}')">
      <div class="card-top"><div class="avatar">${avatarHtml(p.name)}</div>
        <div><div class="card-name">${p.name}</div><div class="card-pos">${p.pos==='G'?'Guard':'Forward'} &middot; ${p.height ?? '—'}</div></div>
      </div>
      <div class="card-body">
        <div class="metric">Weight<b>${cw!=null?cw.toFixed(1):'—'} lb</b></div>
        <div class="metric">CMJ<b>${vert!=null?vert.toFixed(1):'—'} cm</b></div>
        <div class="metric" title="Weight change since season start">Wt. Change<b>${changeHtml}</b></div>
      </div></div>`;
  }).join('');
}

function renderRadarChart(containerId, labels, values, avgValues, maxValue){
  const w=460, h=400, cx=w/2, cy=190, radius=85, n=labels.length;
  const angleFor = i => (Math.PI*2*i/n) - Math.PI/2;
  function pointAt(i,val,r){ const rr=((val||0)/maxValue)*(r!=null?r:radius); const a=angleFor(i); return [cx+rr*Math.cos(a), cy+rr*Math.sin(a)]; }
  let gridRings=''; for (let level=1; level<=maxValue; level++){ const pts=labels.map((_,i)=>pointAt(i,level).join(',')).join(' '); gridRings+=`<polygon points="${pts}" fill="none" stroke="#2c2e33" stroke-width="1"/>`; }
  let axisLines='', labelEls='';
  labels.forEach((lab,i)=>{
    const [x,y]=pointAt(i,maxValue);
    axisLines+=`<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="#2c2e33" stroke-width="1"/>`;
    const [lx,ly]=pointAt(i,maxValue*1.3);
    const anchor = Math.abs(lx-cx)<8 ? 'middle' : (lx>cx?'start':'end');
    labelEls+=`<text x="${lx}" y="${ly}" fill="#f2f1ee" font-size="12.5" text-anchor="${anchor}" dominant-baseline="middle">${lab}</text>`;
  });
  const radarNum = v => v==null ? '—' : (Number.isInteger(v) ? String(v) : v.toFixed(1));
  const avgPts = (avgValues||[]).map((v,i)=>pointAt(i, v).join(',')).join(' ');
  const avgPoints = (avgValues||[]).map((v,i)=>{ const [x,y]=pointAt(i, v);
    const tip = `${labels[i]} (Team Avg): ${radarNum(v)}`;
    return `<circle cx="${x}" cy="${y}" r="3" fill="#93969d"/><circle class="pt-hit" data-tip="${tip.replace(/"/g,'&quot;')}" cx="${x}" cy="${y}" r="9" fill="transparent"/>`; }).join('');
  const dataPts = values.map((v,i)=>pointAt(i, v).join(',')).join(' ');
  const dataPoints = values.map((v,i)=>{ const [x,y]=pointAt(i, v);
    const tip = `${labels[i]}: ${radarNum(v)}`;
    return `<circle cx="${x}" cy="${y}" r="3.5" fill="${RED}"/><circle class="pt-hit" data-tip="${tip.replace(/"/g,'&quot;')}" cx="${x}" cy="${y}" r="9" fill="transparent"/>`; }).join('');
  const legendY = h - 14;
  const legend = avgValues ? `
    <line x1="${cx-115}" y1="${legendY}" x2="${cx-95}" y2="${legendY}" stroke="${RED}" stroke-width="2.5"/>
    <text x="${cx-90}" y="${legendY+4}" fill="#f2f1ee" font-size="11.5">This Player</text>
    <line x1="${cx+5}" y1="${legendY}" x2="${cx+25}" y2="${legendY}" stroke="#93969d" stroke-width="2.5" stroke-dasharray="4,3"/>
    <text x="${cx+30}" y="${legendY+4}" fill="#93969d" font-size="11.5">Team Average</text>` : '';
  document.getElementById(containerId).innerHTML = `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">
    ${gridRings}${axisLines}
    ${avgValues ? `<polygon points="${avgPts}" fill="rgba(147,150,157,0.12)" stroke="#93969d" stroke-width="2" stroke-dasharray="5,4"/>` : ''}
    <polygon points="${dataPts}" fill="rgba(166,25,46,0.35)" stroke="${RED}" stroke-width="2.5"/>
    ${avgPoints}${dataPoints}${labelEls}${legend}</svg>`;
}

function axisNum(v, unit){
  if (v==null) return '';
  if (unit === '%') return (v*100).toFixed(1);
  return Number.isInteger(v) ? String(v) : v.toFixed(v >= 100 ? 0 : 1);
}

// Builds a smooth SVG path (Catmull-Rom converted to cubic beziers) through a list of [x,y]
// points, instead of straight line segments. Falls back gracefully for 0/1 points.
function smoothPathD(points){
  if (points.length === 0) return '';
  if (points.length === 1) return `M${points[0][0].toFixed(1)},${points[0][1].toFixed(1)}`;
  let d = `M${points[0][0].toFixed(1)},${points[0][1].toFixed(1)} `;
  for (let i=0;i<points.length-1;i++){
    const p0 = points[i-1] || points[i];
    const p1 = points[i];
    const p2 = points[i+1];
    const p3 = points[i+2] || p2;
    const cp1x = p1[0] + (p2[0]-p0[0])/6;
    const cp1y = p1[1] + (p2[1]-p0[1])/6;
    const cp2x = p2[0] - (p3[0]-p1[0])/6;
    const cp2y = p2[1] - (p3[1]-p1[1])/6;
    d += `C${cp1x.toFixed(1)},${cp1y.toFixed(1)} ${cp2x.toFixed(1)},${cp2y.toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)} `;
  }
  return d.trim();
}

function renderLineChart(containerId, labels, values, unit, compact){
  const w = compact ? 260 : 500, h = compact ? 118 : 270;
  const padL = compact ? 34 : 48, padR = compact ? 10 : 22, padT = compact ? 12 : 20, padB = compact ? 20 : 34;
  const plotW=w-padL-padR, plotH=h-padT-padB;
  const gridSteps = compact ? 3 : 4;
  const fsAxis = compact ? 8 : 10, fsXLab = compact ? 8 : 10, fsDot = compact ? 2.2 : 3.2, fsStroke = compact ? 1.8 : 2.5;
  const nums = values.filter(v=>v!=null);
  if (nums.length === 0){
    document.getElementById(containerId).innerHTML = `<svg viewBox="0 0 ${w} ${h}"><text x="${w/2}" y="${h/2}" fill="#93969d" font-size="${compact?10:12}" text-anchor="middle">No test data yet</text></svg>`;
    return;
  }
  if (nums.length === 1){
    document.getElementById(containerId).innerHTML = `<svg viewBox="0 0 ${w} ${h}"><circle cx="${w/2}" cy="${h/2}" r="${compact?3:4}" fill="${RED}"/>
      <text x="${w/2}" y="${h/2-(compact?12:18)}" fill="#f2f1ee" font-size="${compact?11:13}" text-anchor="middle">${fmtNum(nums[0], unit)}</text>
      <text x="${w/2}" y="${h/2+(compact?18:26)}" fill="#93969d" font-size="${compact?9:11}" text-anchor="middle">${compact?'1 test recorded':'only one test recorded so far'}</text></svg>`;
    return;
  }
  let minV=Math.min(...nums), maxV=Math.max(...nums);
  if (minV===maxV){ minV-=5; maxV+=5; }
  const pad=(maxV-minV)*0.18; minV-=pad; maxV+=pad;
  const xFor = i => padL + (i/(labels.length-1))*plotW;
  const yFor = v => padT + plotH - ((v-minV)/(maxV-minV))*plotH;
  let gridLines='';
  for (let s=0;s<=gridSteps;s++){ const v=minV+(maxV-minV)*s/gridSteps; const y=yFor(v);
    gridLines += `<line x1="${padL}" y1="${y}" x2="${w-padR}" y2="${y}" stroke="#1f2023" stroke-width="1"/>`;
    if (!compact || s%2===0) gridLines += `<text x="${padL-6}" y="${y+3}" fill="#93969d" font-size="${fsAxis}" text-anchor="end">${axisNum(v,unit)}</text>`; }
  let xLabels=''; labels.forEach((lab,i)=>{ if (compact && labels.length>4 && i%2!==0 && i!==labels.length-1) return; xLabels += `<text x="${xFor(i)}" y="${h-(compact?6:10)}" fill="#93969d" font-size="${fsXLab}" text-anchor="middle">${lab}</text>`; });
  // Skip missed tests (null values) entirely rather than breaking the line into disconnected
  // segments — connect straight from the last real reading to the next one, so a missed test
  // doesn't leave a visual gap in the trend line.
  let points=[];
  values.forEach((v,i)=>{ if (v!=null) points.push([xFor(i), yFor(v), v, i]); });
  const d = smoothPathD(points.map(p=>[p[0],p[1]]));
  const paths = `<path d="${d}" fill="none" stroke="${RED}" stroke-width="${fsStroke}"/>`;
  const areaD = d + ` L${points[points.length-1][0].toFixed(1)},${(padT+plotH).toFixed(1)} L${points[0][0].toFixed(1)},${(padT+plotH).toFixed(1)} Z`;
  const areas = `<path d="${areaD}" fill="rgba(166,25,46,0.15)"/>`;
  const hitR = compact ? 8 : 11;
  const dots = points.map(p=>{
    const tip = `${labels[p[3]]}: ${fmtNum(p[2], unit)}`.replace(/"/g,'&quot;');
    return `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="${fsDot}" fill="${RED}"/><circle class="pt-hit" data-tip="${tip}" cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="${hitR}" fill="transparent"/>`;
  }).join('');
  document.getElementById(containerId).innerHTML = `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">${gridLines}${areas}${paths}${dots}${xLabels}</svg>`;
}

/* ---------- shared chart hover tooltip ----------
   Charts (weight trend, metric trend, character-eval radar) are re-rendered via innerHTML, which
   destroys and recreates their <circle> elements each time. Rather than re-attaching listeners on
   every redraw, we delegate from `document` (which never gets replaced) and read the value/label
   straight off each point's data-tip attribute. */
function ensureChartTooltipEl(){
  let t = document.getElementById('chartTooltip');
  if (!t) {
    t = document.createElement('div');
    t.id = 'chartTooltip';
    t.className = 'chart-tooltip';
    document.body.appendChild(t);
  }
  return t;
}
function chartTipPosition(evt, t){
  const pad = 14;
  let x = evt.clientX + pad, y = evt.clientY + pad;
  const vw = window.innerWidth || 1200, vh = window.innerHeight || 800;
  if (x > vw - 160) x = evt.clientX - pad - 140;
  if (y > vh - 40) y = evt.clientY - pad - 30;
  t.style.left = x + 'px';
  t.style.top = y + 'px';
}
document.addEventListener('mouseover', function(evt){
  const el = evt.target;
  if (!el || !el.dataset || !el.dataset.tip) return;
  const t = ensureChartTooltipEl();
  t.textContent = el.dataset.tip;
  t.style.display = 'block';
  chartTipPosition(evt, t);
});
document.addEventListener('mousemove', function(evt){
  const t = document.getElementById('chartTooltip');
  if (t && t.style.display === 'block') chartTipPosition(evt, t);
});
document.addEventListener('mouseout', function(evt){
  const el = evt.target;
  if (!el || !el.dataset || !el.dataset.tip) return;
  const t = document.getElementById('chartTooltip');
  if (t) t.style.display = 'none';
});

function showDetailFromRoster(name){ showDetail(name); }

function showDetail(name){
  const p = players[name];
  document.getElementById('playersRoster').style.display = 'none';
  document.getElementById('playerDetail').style.display = 'block';
  document.getElementById('backBtn').style.display = 'inline-block';
  document.getElementById('backBtn').onclick = function(){
    document.getElementById('playersRoster').style.display='block';
    document.getElementById('playerDetail').style.display='none';
    document.getElementById('backBtn').style.display='none';
    document.getElementById('headerSub').textContent = 'Performance Dashboard · 2026–27';
  };
  document.getElementById('headerSub').textContent = name + ' — Player Sheet';

  document.getElementById('dAvatar').innerHTML = avatarHtml(p.name);
  document.getElementById('dName').textContent = p.name;
  document.getElementById('dPos').textContent = p.pos==='G' ? 'GUARD' : 'FORWARD';
  document.getElementById('dHeight').textContent = p.height ?? '—';
  document.getElementById('dStartWeight').textContent = p.startWeight!=null ? p.startWeight.toFixed(1)+' lb' : '—';
  const cw = curWeight(p);
  document.getElementById('dCurWeight').textContent = cw!=null ? cw.toFixed(1)+' lb' : '—';
  const change = weightChange(p);
  document.getElementById('dWeightChange').innerHTML = change==null ? '—' : (change>=0?`<span class="trend-up">+${change.toFixed(1)} lb</span>`:`<span class="trend-down">${change.toFixed(1)} lb</span>`);

  const traits = ['workEthic','consistency','coachability','attitude','toughness'];
  const traitLabels = ['Work Ethic','Consistency','Coachability','Attitude','Toughness'];
  const teamTraitAvg = traits.map(t => avg(order.map(nm=>players[nm].character ? players[nm].character[t] : null)));
  renderRadarChart('charChart', traitLabels, traits.map(t=>p.character?p.character[t]:0), teamTraitAvg, 5);
  renderTraitDefs('traitDefsPlayer');
  renderLineChart('weightChart', ['Start', ...p.weightDates], [p.startWeight, ...p.weights], 'lb');
  renderPlayerPhotos(p.name);

  let html = '';
  for (const cat of Object.keys(METRIC_ORDER)){
    html += `<div class="metric-head" data-cat="${cat}"><h2>${cat}</h2></div><div class="metric-grid">`;
    for (const m of METRIC_ORDER[cat]){
      const d = p.metrics[m];
      const meta = metricMeta[m];
      const chartId = 'pchart_' + m.replace(/[^a-zA-Z0-9]/g,'');
      // If the most recent test date was missed (current==null) but the player has been tested
      // before, fall back to their last actual result instead of showing a dash.
      const effCurrent = d.current!=null ? d.current : lastVal(d.series);
      const isPB = effCurrent!=null && d.best!=null && d.first!=null && Math.abs(effCurrent-d.best)<1e-9 && Math.abs(d.best-d.first)>1e-9;
      const heroVal = effCurrent!=null ? fmtNumBare(effCurrent, meta.unit) : '—';
      const heroLabel = d.current!=null ? 'current' : (effCurrent!=null ? 'most recent' : 'current');
      const infoDot = meta.description
        ? ` <span class="info-dot" tabindex="0">ⓘ<span class="tooltip-box">${meta.description.replace(/"/g,'&quot;')}</span></span>`
        : '';
      html += `<div class="panel">
        <h3>${m}${infoDot}</h3>
        ${meta.description ? `<div class="metric-desc-sm">${meta.description}</div>` : ''}
        <div class="metric-hero">
          <span class="hero-value">${heroVal}</span><span class="hero-unit">${meta.unit||''} · ${heroLabel}</span>
          ${vsAvgBadge(effCurrent, d.teamAvgCurrent, meta.direction, meta.unit)}
        </div>
        <div class="stat-line">
          <div class="si">First<b>${d.first!=null?fmtNum(d.first,meta.unit):'—'}</b></div>
          <div class="si">Best<b>${d.best!=null?fmtNum(d.best,meta.unit):'—'}</b></div>
          ${isPB ? '<span class="pb-badge">New PB</span>' : ''}
        </div>
        <div class="chart-wrap" id="${chartId}"></div>
      </div>`;
    }
    html += `</div>`;
  }
  document.getElementById('metricSections').innerHTML = html;
  for (const cat of Object.keys(METRIC_ORDER)){
    for (const m of METRIC_ORDER[cat]){
      const d = p.metrics[m]; const meta = metricMeta[m];
      const chartId = 'pchart_' + m.replace(/[^a-zA-Z0-9]/g,'');
      renderLineChart(chartId, meta.dates, d.series, meta.unit, true);
    }
  }
  window.scrollTo(0,0);
}

function showRoster(){
  document.getElementById('playersRoster').style.display = 'block';
  document.getElementById('playerDetail').style.display = 'none';
  document.getElementById('backBtn').style.display = 'none';
  document.getElementById('headerSub').textContent = 'Performance Dashboard · 2026–27';
}

/* Builds one print-ready sheet per player (reusing the exact same showDetail() rendering as the
   single-player "Print Player Sheet" button, so every print-CSS rule already tuned for that page
   just applies here too) and triggers a single print job covering the whole roster. */
function printAllPlayers(){
  const btn = document.getElementById('printAllBtn');
  if (btn) { btn.disabled = true; btn.textContent = 'Preparing…'; }

  // Remember what was on screen so it can be put back once printing is done.
  const wasShowingDetail = document.getElementById('playerDetail').style.display === 'block';
  const previousPlayerName = wasShowingDetail ? document.getElementById('dName').textContent : null;

  const target = document.getElementById('printAllContent');
  let allHtml = '';
  order.forEach(name => {
    showDetail(name);
    // Note: this intentionally duplicates element ids (dAvatar, charChart, pchart_* etc.) once per
    // player inside this container. That's invalid HTML strictly speaking, but harmless here since
    // nothing queries back into these captured copies - only the live #playerDetail (rendered fresh
    // per click) is ever looked up by id during normal use.
    allHtml += `<div class="print-sheet-page">${document.getElementById('playerDetail').innerHTML}</div>`;
  });
  target.innerHTML = allHtml;
  document.body.classList.add('printing-all');

  let restored = false;
  function restore(){
    if (restored) return;
    restored = true;
    document.body.classList.remove('printing-all');
    target.innerHTML = '';
    if (previousPlayerName) { showDetail(previousPlayerName); } else { showRoster(); }
    if (btn) { btn.disabled = false; btn.textContent = 'Print All Player Sheets'; }
    window.onafterprint = null;
  }
  window.onafterprint = restore;
  setTimeout(function(){ window.print(); }, 50); // let the freshly-built DOM settle before printing
  setTimeout(restore, 5000); // safety net in case this browser never fires onafterprint
}

document.getElementById('tabNav').addEventListener('click', (e)=>{
  const btn = e.target.closest('button[data-tab]'); if (!btn) return;
  document.querySelectorAll('nav.tabs button').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.getElementById('view-'+btn.dataset.tab).classList.add('active');
  if (btn.dataset.tab !== 'players'){
    document.getElementById('backBtn').style.display='none';
    document.getElementById('headerSub').textContent = 'Performance Dashboard · 2026–27';
  } else { showRoster(); }
});

/* ================= LIVE DATA UPLOAD (drag & drop .xlsx) ================= */
const METRIC_SHEETS = [
  ['10YD','10 Yard Sprint','SPEED','low','sec'],
  ['PEAK POWER','Peak Power','SPEED','high','W/kg'],
  ['3 STEP MPH','MPH by Step 3','SPEED','high','mph'],
  ['CMJ','CMJ','BOUNCE','high','cm'],
  ['APPROACH','Approach Jump','BOUNCE','high','in'],
  ['RSI','RSI','BOUNCE','high',''],
  ['TRAP DEAD','TBDL 1RM (.4m/s)','STRENGTH','high','lb'],
  ['BENCH','Bench 1RM','STRENGTH','high','lb'],
  ['CHIN UP','Chin Up Max Reps','STRENGTH','high','reps'],
  ['BODY FAT','Body Fat','FITNESS','low','%'],
  ['LEAN MASS','Lean Mass','FITNESS','high','lb'],
  ['CELTIC','Celtic Test','FITNESS','high',''],
];
// Sheets whose own BEST cell formula is unreliable (a stray non-test column got swept into it,
// or it uses MIN() where MAX() was intended) — recompute BEST from the real dated columns instead.
const RECOMPUTE_BEST_FROM_SERIES = ['TRAP DEAD','BENCH','PEAK POWER'];

function cleanNum(v){
  if (v==null || v==='') return null;
  if (typeof v === 'number') return v;
  if (typeof v === 'string'){
    const s = v.trim();
    // Guard against Excel mangling a typed decimal like "33.7" into a fraction-like string "33/7"
    const slashMatch = s.match(/^(\d+)\/(\d+)$/);
    if (slashMatch) return parseFloat(slashMatch[1] + '.' + slashMatch[2]);
    const f = parseFloat(s); return isNaN(f) ? null : f;
  }
  return null;
}
function fmtDateCell(d){ return (d instanceof Date) ? (d.getMonth()+1) + '/' + d.getDate() : null; }
function sheetRows(wb, name){
  const ws = wb.Sheets[name];
  if (!ws) return null;
  return XLSX.utils.sheet_to_json(ws, {header:1, raw:true, defval:null});
}

function parseWorkbook(wb){
  const rosterRows = sheetRows(wb, 'ROSTER');
  if (!rosterRows) throw new Error('No "ROSTER" sheet found in this file.');
  const rHeader = rosterRows[0];
  const weightDateIdx = [];
  for (let i=5;i<rHeader.length;i++){ if (rHeader[i] instanceof Date) weightDateIdx.push(i); }
  const weightDates = weightDateIdx.map(i=>fmtDateCell(rHeader[i]));

  const players = {}; const order = [];
  for (let r=1; r<rosterRows.length; r++){
    const row = rosterRows[r]; if (!row) continue;
    const name = row[0];
    if (!name || typeof name !== 'string' || !name.trim()) continue;
    order.push(name);
    const weights = weightDateIdx.map(i => cleanNum(row[i]));
    let height = row[2];
    if (typeof height === 'string') height = height.replace(/ /g,'').trim();
    players[name] = { name, pos: row[1], height: height || null,
      startWeight: cleanNum(row[4]), weightDates, weights, character: null, metrics: {} };
  }
  if (!order.length) throw new Error('No player rows found under ROSTER — check the file matches the usual template.');

  const charRows = sheetRows(wb, 'CHARACTER EVAL');
  if (charRows){
    for (let r=1;r<charRows.length;r++){
      const row = charRows[r]; if(!row) continue;
      const name = row[0];
      if (players[name]){
        players[name].character = { workEthic: cleanNum(row[1]), consistency: cleanNum(row[2]),
          coachability: cleanNum(row[3]), attitude: cleanNum(row[4]), toughness: cleanNum(row[5]) };
      }
    }
  }
  order.forEach(n => { if (!players[n].character) players[n].character = {}; });

  const teamMetricAvg = {}; const newMetricMeta = {};
  METRIC_SHEETS.forEach(([sheetName, label, cat, direction, unit]) => {
    const rows = sheetRows(wb, sheetName);
    if (!rows){ newMetricMeta[label] = {category:cat, direction, unit, dates:[], description:null}; return; }
    const hdr = rows[0];
    // Row 20 holds a coach-written description of what the test measures
    // (A20="Description:", B20=text) - surfaced on the dashboard so coaches know what each test is.
    let description = null;
    const descRow = rows[19];
    if (descRow && typeof descRow[0] === 'string' && descRow[0].replace(/:\s*$/,'').trim().toUpperCase() === 'DESCRIPTION'){
      const descVal = descRow[1];
      if (typeof descVal === 'string' && descVal.trim()) description = descVal.trim();
    }
    let avgIdx=null, bestIdx=null; const dateIdx = [];
    for (let i=0;i<hdr.length;i++){
      const h = hdr[i];
      if (h === 'AVERAGE') avgIdx = i;
      else if (h === 'BEST') bestIdx = i;
      else if (i>0 && h instanceof Date) dateIdx.push(i);
    }
    const dateLabels = dateIdx.map(i=>fmtDateCell(hdr[i]));
    const firstDateIdx = dateIdx.length ? dateIdx[0] : null;
    const lastDateIdx = dateIdx.length ? dateIdx[dateIdx.length-1] : null;

    let avgRow = null;
    for (let r=1;r<rows.length;r++){
      const row = rows[r]; if(!row) continue;
      if (row[0] && String(row[0]).toUpperCase().includes('AVERAGE')) avgRow = row;
    }
    const teamCurrentAvg = (avgRow && lastDateIdx!=null) ? cleanNum(avgRow[lastDateIdx]) : null;
    teamMetricAvg[label] = teamCurrentAvg;
    newMetricMeta[label] = { category:cat, direction, unit, dates: dateLabels, description };

    const recomputeBest = RECOMPUTE_BEST_FROM_SERIES.includes(sheetName);
    for (let r=1;r<rows.length;r++){
      const row = rows[r]; if(!row) continue;
      const name = row[0];
      if (!players[name]) continue;
      const series = dateIdx.map(i => cleanNum(row[i]));
      const firstV = series.length ? series[0] : null;
      const currentV = series.length ? series[series.length-1] : null;
      let bestV;
      if (recomputeBest){
        const clean = series.filter(v=>v!=null);
        bestV = clean.length ? (direction==='high' ? Math.max(...clean) : Math.min(...clean)) : null;
      } else {
        bestV = bestIdx!=null ? cleanNum(row[bestIdx]) : null;
      }
      if (bestV === 0) bestV = null;
      players[name].metrics[label] = { series, first: firstV, current: currentV, best: bestV, teamAvgCurrent: teamCurrentAvg };
    }
  });
  order.forEach(n => {
    METRIC_SHEETS.forEach(([,label]) => {
      if (!players[n].metrics[label]) players[n].metrics[label] = { series:[], first:null, current:null, best:null, teamAvgCurrent: teamMetricAvg[label] };
    });
  });

  return { order, players, teamMetricAvg, metricMeta: newMetricMeta };
}

function updateDataMeta(){
  const el = document.getElementById('dataMeta');
  if (!el) return;
  if (savedDataWasIncompatible) {
    el.textContent = 'Showing built-in data (your previously saved upload was from an older template — use "Update Data" to re-upload it)';
    return;
  }
  if (savedDataWasStale) {
    el.textContent = 'Showing built-in data (a newer version was sent since your last upload — use "Update Data" if you have more recent numbers to add)';
    return;
  }
  el.textContent = dataSavedAt ? ('Data updated ' + new Date(dataSavedAt).toLocaleString()) : 'Showing built-in data';
}

function refreshAllViews(){
  renderDashboard();
  renderTeamTab('sections-speed','kpiSpeed','SPEED');
  renderTeamTab('sections-bounce','kpiBounce','BOUNCE');
  renderTeamTab('sections-strength','kpiStrength','STRENGTH');
  renderTeamTab('sections-fitness','kpiFitness','FITNESS');
  renderCharacter();
  renderGrid();
  showRoster();
  updateDataMeta();
}

function applyNewData(newData){
  DATA = newData;
  players = DATA.players;
  order = DATA.order;
  metricMeta = DATA.metricMeta;
  dataSavedAt = new Date().toISOString();
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ data: DATA, savedAt: dataSavedAt })); } catch(e) {}
  refreshAllViews();
}

function openUploadModal(){ document.getElementById('uploadModal').classList.add('open'); }
function closeUploadModal(){
  document.getElementById('uploadModal').classList.remove('open');
  const s = document.getElementById('uploadStatus');
  s.textContent = ''; s.className = 'upload-status';
  const pwEl = document.getElementById('publishPassword');
  if (pwEl) pwEl.value = '';
}

// Cloudflare Worker that safely relays a new spreadsheet to GitHub (which then rebuilds and
// republishes the live site for everyone). The worker checks the password server-side and never
// exposes any write credentials to the browser. Left blank, "Update Data" only updates this browser.
const UPDATE_WORKER_URL = '__WORKER_URL__';

// Uint8Array -> base64, chunked to avoid call-stack limits on large files.
function bytesToBase64(bytes){
  let binary = '';
  const chunkSize = 0x8000;
  for (let i = 0; i < bytes.length; i += chunkSize) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunkSize));
  }
  return btoa(binary);
}

async function publishToEveryone(bytes, filename, password, status){
  if (!UPDATE_WORKER_URL || UPDATE_WORKER_URL.indexOf('__WORKER_URL__') !== -1) {
    return; // relay not configured yet - local-only save already happened
  }
  status.className = 'upload-status pending';
  status.textContent = 'Saved in this browser. Publishing for everyone...';
  try {
    const res = await fetch(UPDATE_WORKER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: password, filename: filename, fileBase64: bytesToBase64(bytes) })
    });
    const body = await res.json().catch(() => ({}));
    if (res.ok && body.ok) {
      status.className = 'upload-status success';
      status.textContent = 'Saved here, and published for everyone — the live site will refresh within about a minute.';
    } else if (res.status === 401) {
      status.className = 'upload-status error';
      status.textContent = 'Saved in this browser, but publishing failed: incorrect password.';
    } else {
      status.className = 'upload-status error';
      status.textContent = 'Saved in this browser, but publishing failed: ' + (body.error || res.statusText || 'unknown error');
    }
  } catch(err){
    status.className = 'upload-status error';
    status.textContent = 'Saved in this browser, but could not reach the publish service: ' + err.message;
  }
}

function handleWorkbookFile(file){
  const status = document.getElementById('uploadStatus');
  const pwEl = document.getElementById('publishPassword');
  const password = pwEl ? pwEl.value : '';
  status.className = 'upload-status';
  status.textContent = 'Reading ' + file.name + '...';
  if (typeof XLSX === 'undefined'){
    status.className = 'upload-status error';
    status.textContent = 'Could not load the spreadsheet reader — this page needs an internet connection the first time you update data.';
    return;
  }
  const reader = new FileReader();
  reader.onload = function(e){
    try {
      const bytes = new Uint8Array(e.target.result);
      const wb = XLSX.read(bytes, {type:'array', cellDates:true});
      const newData = parseWorkbook(wb);
      applyNewData(newData);
      status.className = 'upload-status success';
      status.textContent = 'Loaded ' + newData.order.length + ' players from ' + file.name + '. Saved in this browser for next time.';
      publishToEveryone(bytes, file.name, password, status);
    } catch(err){
      status.className = 'upload-status error';
      status.textContent = 'Could not read that file: ' + err.message;
    }
  };
  reader.onerror = function(){
    status.className = 'upload-status error';
    status.textContent = 'Could not read that file.';
  };
  reader.readAsArrayBuffer(file);
}

const dropZoneEl = document.getElementById('dropZone');
const fileInputEl = document.getElementById('fileInput');
dropZoneEl.addEventListener('click', () => fileInputEl.click());
dropZoneEl.addEventListener('dragover', e => { e.preventDefault(); dropZoneEl.classList.add('drag-over'); });
dropZoneEl.addEventListener('dragleave', () => dropZoneEl.classList.remove('drag-over'));
dropZoneEl.addEventListener('drop', e => {
  e.preventDefault(); dropZoneEl.classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file) handleWorkbookFile(file);
});
fileInputEl.addEventListener('change', e => {
  const file = e.target.files[0];
  if (file) handleWorkbookFile(file);
});

/* ================= PROGRESS PHOTOS (bulk drag & drop) ================= */
function savePhotos(){
  try { localStorage.setItem(PHOTOS_KEY, JSON.stringify(PHOTOS)); }
  catch(e){
    const status = document.getElementById('photoStatus');
    if (status){ status.className='upload-status error'; status.textContent = 'Could not save photos — browser storage may be full. Try fewer or smaller images.'; }
  }
}

function parsePhotoFilename(filename){
  let base = filename.replace(/\.[^.]+$/, '');
  let dateGuess = null, m;
  m = base.match(/(\d{4})[-_.](\d{1,2})[-_.](\d{1,2})/);
  if (m){
    const y=+m[1], mo=+m[2], da=+m[3];
    if (mo>=1&&mo<=12&&da>=1&&da<=31){ dateGuess = y+'-'+String(mo).padStart(2,'0')+'-'+String(da).padStart(2,'0'); base = base.replace(m[0], ' '); }
  }
  if (!dateGuess){
    m = base.match(/(\d{1,2})[-_.](\d{1,2})[-_.](\d{4})/);
    if (m){
      const mo=+m[1], da=+m[2], y=+m[3];
      if (mo>=1&&mo<=12&&da>=1&&da<=31){ dateGuess = y+'-'+String(mo).padStart(2,'0')+'-'+String(da).padStart(2,'0'); base = base.replace(m[0], ' '); }
    }
  }
  const normBase = base.replace(/[_\-.]+/g, ' ');
  let angleGuess = null;
  if (/(^|\s)back(\s|$)/i.test(normBase)) angleGuess = 'back';
  else if (/(^|\s)front(\s|$)/i.test(normBase)) angleGuess = 'front';
  base = normBase.replace(/(^|\s)(front|back)(\s|$)/gi, ' ');
  const tokens = base.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const fuzzy = (tok, name) => tok===name || (name.length>2 && (name.includes(tok) || tok.includes(name)));
  const matches = order.filter(nm=>{
    const parts = nm.split(',').map(s=>s.trim().toLowerCase());
    const last = parts[0]||'', first = parts[1]||'';
    const hasLast = tokens.some(t=>fuzzy(t,last));
    const hasFirst = tokens.some(t=>fuzzy(t,first));
    return hasLast && hasFirst;
  });
  return { playerGuess: matches.length===1 ? matches[0] : null, dateGuess, angleGuess };
}

function compressImage(file){
  return new Promise((resolve, reject)=>{
    const reader = new FileReader();
    reader.onload = e=>{
      const img = new Image();
      img.onload = ()=>{
        const maxDim = 900;
        let w = img.width, h = img.height;
        if (w>maxDim || h>maxDim){
          if (w>h){ h = Math.round(h*maxDim/w); w=maxDim; } else { w = Math.round(w*maxDim/h); h=maxDim; }
        }
        const canvas = document.createElement('canvas');
        canvas.width=w; canvas.height=h;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img,0,0,w,h);
        resolve(canvas.toDataURL('image/jpeg', 0.82));
      };
      img.onerror = reject;
      img.src = e.target.result;
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function updateReviewField(id, field, value){
  const item = photoReviewQueue.find(it=>it.id===id);
  if (item) item[field] = value;
}

function renderPhotoReviewList(){
  const el = document.getElementById('photoReviewList');
  const btn = document.getElementById('savePhotosBtn');
  if (!el) return;
  if (!photoReviewQueue.length){ el.innerHTML=''; if(btn) btn.style.display='none'; return; }
  if (btn) btn.style.display='inline-block';
  el.innerHTML = photoReviewQueue.map(item=>{
    const opts = order.map(nm=>`<option value="${nm}" ${item.player===nm?'selected':''}>${nm}</option>`).join('');
    return `<div class="review-row" data-id="${item.id}">
      <img src="${item.dataUrl}" alt="">
      <div class="rf">
        <div class="rf-name">${item.filename}</div>
        <div class="rf-fields">
          <select onchange="updateReviewField('${item.id}','player',this.value)"><option value="">Choose player&hellip;</option>${opts}</select>
          <select onchange="updateReviewField('${item.id}','angle',this.value)">
            <option value="">Angle&hellip;</option>
            <option value="front" ${item.angle==='front'?'selected':''}>Front</option>
            <option value="back" ${item.angle==='back'?'selected':''}>Back</option>
          </select>
          <input type="date" value="${item.date||''}" onchange="updateReviewField('${item.id}','date',this.value)">
        </div>
      </div>
    </div>`;
  }).join('');
}

async function handlePhotoFiles(fileList){
  const status = document.getElementById('photoStatus');
  status.className='upload-status';
  status.textContent = 'Reading ' + fileList.length + ' photo(s)...';
  for (const file of Array.from(fileList)){
    if (!file.type || !file.type.startsWith('image/')) continue;
    try{
      const dataUrl = await compressImage(file);
      const {playerGuess, dateGuess, angleGuess} = parsePhotoFilename(file.name);
      photoReviewQueue.push({ id: 'p'+(photoIdCounter++), filename: file.name, dataUrl, player: playerGuess, date: dateGuess, angle: angleGuess });
    } catch(e){}
  }
  renderPhotoReviewList();
  status.textContent = photoReviewQueue.length ? 'Check the player and date guesses below, then click Save Photos.' : 'Could not read any images from that drop.';
}

function commitPhotoReview(){
  const status = document.getElementById('photoStatus');
  const missing = photoReviewQueue.filter(it=>!it.player || !it.date || !it.angle);
  if (missing.length){
    status.className='upload-status error';
    status.textContent = missing.length + ' photo(s) still need a player, angle, and/or date selected before saving.';
    return;
  }
  photoReviewQueue.forEach(it=>{
    if (!PHOTOS[it.player]) PHOTOS[it.player] = [];
    const idx = PHOTOS[it.player].findIndex(ph=>ph.date===it.date && (ph.angle||'front')===it.angle);
    const entry = { date: it.date, angle: it.angle, dataUrl: it.dataUrl };
    if (idx>=0) PHOTOS[it.player][idx] = entry; else PHOTOS[it.player].push(entry);
    PHOTOS[it.player].sort((a,b)=>a.date.localeCompare(b.date));
  });
  savePhotos();
  status.className='upload-status success';
  status.textContent = 'Saved ' + photoReviewQueue.length + ' photo(s). Stored in this browser for next time.';
  const savedNames = [...new Set(photoReviewQueue.map(it=>it.player))];
  photoReviewQueue = [];
  renderPhotoReviewList();
  const currentName = document.getElementById('dName') ? document.getElementById('dName').textContent : null;
  if (currentName && savedNames.includes(currentName)) renderPlayerPhotos(currentName);
  setTimeout(closePhotoModal, 1600);
}

function renderPlayerPhotos(name){
  const el = document.getElementById('photoContent');
  if (!el) return;
  const fmtD = ds => { const d = new Date(ds+'T00:00:00'); return isNaN(d) ? ds : (d.getMonth()+1)+'/'+d.getDate()+'/'+d.getFullYear(); };
  const all = (PHOTOS[name]||[]).slice().sort((a,b)=>a.date.localeCompare(b.date));
  if (!all.length){
    el.innerHTML = `<div class="photo-empty">No photos on file yet for ${name}.</div>`;
    return;
  }
  const front = all.filter(p=>(p.angle||'front')==='front');
  const back = all.filter(p=>p.angle==='back');
  const cell = (tag, arr, which) => {
    const ph = which==='before' ? (arr.length ? arr[0] : null) : (arr.length>=2 ? arr[arr.length-1] : null);
    if (!ph){
      const msg = which==='before' ? `No ${tag.toLowerCase()} photo yet` : `Awaiting after photo`;
      return `<div class="pg-cell"><div class="pg-tag">${tag}</div><div class="pg-placeholder">${msg}</div></div>`;
    }
    return `<div class="pg-cell"><div class="pg-tag">${tag}</div><img src="${ph.dataUrl}"><div class="pg-date">${fmtD(ph.date)}</div></div>`;
  };
  el.innerHTML = `<div class="photo-grid4">
      <div class="pg-group"><div class="pg-header">Front</div><div class="pg-row">${cell('Before', front, 'before')}${cell('After', front, 'after')}</div></div>
      <div class="pg-group"><div class="pg-header">Back</div><div class="pg-row">${cell('Before', back, 'before')}${cell('After', back, 'after')}</div></div>
    </div>
    ${(front.length<2 && back.length<2) ? `<div class="photo-note">Upload a later front/back photo to fill in the "After" column.</div>` : ''}`;
}

function openPhotoModal(){ document.getElementById('photoModal').classList.add('open'); }
function closePhotoModal(){
  document.getElementById('photoModal').classList.remove('open');
  photoReviewQueue = [];
  renderPhotoReviewList();
  const s = document.getElementById('photoStatus');
  s.textContent=''; s.className='upload-status';
}

const photoDropZoneEl = document.getElementById('photoDropZone');
const photoFileInputEl = document.getElementById('photoFileInput');
photoDropZoneEl.addEventListener('click', () => photoFileInputEl.click());
photoDropZoneEl.addEventListener('dragover', e => { e.preventDefault(); photoDropZoneEl.classList.add('drag-over'); });
photoDropZoneEl.addEventListener('dragleave', () => photoDropZoneEl.classList.remove('drag-over'));
photoDropZoneEl.addEventListener('drop', e => {
  e.preventDefault(); photoDropZoneEl.classList.remove('drag-over');
  if (e.dataTransfer.files.length) handlePhotoFiles(e.dataTransfer.files);
});
photoFileInputEl.addEventListener('change', e => {
  if (e.target.files.length) handlePhotoFiles(e.target.files);
  e.target.value = '';
});

/* init */
function initDashboard(){
  if (__dashboardInitialized) return;
  __dashboardInitialized = true;
  renderDashboard();
  renderTeamTab('sections-speed','kpiSpeed','SPEED');
  renderTeamTab('sections-bounce','kpiBounce','BOUNCE');
  renderTeamTab('sections-strength','kpiStrength','STRENGTH');
  renderTeamTab('sections-fitness','kpiFitness','FITNESS');
  renderCharacter();
  renderGrid();
  updateDataMeta();
}
</script>
</body>
</html>
"""

HTML = HTML.replace("__DATA_JSON__", DATA_JSON)
HTML = HTML.replace("__LOGO_URI__", LOGO_DATA_URI)
HTML = HTML.replace("__PHOTOS_JSON__", PHOTOS_JSON)
HTML = HTML.replace("__HEADSHOTS_JSON__", HEADSHOTS_JSON)
HTML = HTML.replace("__BUILD_TIME__", BUILD_TIME)
HTML = HTML.replace("__WORKER_URL__", WORKER_URL)
with open('index.html', 'w') as f:
    f.write(HTML)
print("Written", len(HTML), "bytes")
