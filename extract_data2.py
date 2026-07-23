import json, datetime
import openpyxl

SRC = 'data/latest.xlsx'
wb = openpyxl.load_workbook(SRC, data_only=True)

def fmt_date(d):
    return f"{d.month}/{d.day}"

def clean_num(v, coerce_slash_decimal=False):
    if v is None or v == '':
        return None
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        s = v.strip()
        # Known corrupted-cell fix: Excel mangled "33.7" into a fraction-like string "33/7"
        if coerce_slash_decimal and '/' in s:
            parts = s.split('/')
            if len(parts) == 2 and parts[0].strip().replace('.','',1).isdigit() and parts[1].strip().isdigit():
                return float(parts[0].strip() + '.' + parts[1].strip())
        try:
            return float(s)
        except ValueError:
            return None
    return None

# ---------- ROSTER ----------
ws = wb['ROSTER']
header = [c.value for c in ws[1]]
weight_date_idx = [i for i, h in enumerate(header) if i >= 5 and isinstance(h, datetime.datetime)]
weight_dates = [fmt_date(header[i]) for i in weight_date_idx]

order = []
players = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    name = row[0]
    if not name or not str(name).strip():
        continue
    pos = row[1]
    height = row[2]
    start_weight = clean_num(row[4])
    weights = [clean_num(row[i]) for i in weight_date_idx]
    order.append(name)
    players[name] = {
        'name': name,
        'pos': pos,
        'height': height,
        'startWeight': start_weight,
        'weightDates': weight_dates,
        'weights': weights,
        'character': None,
        'metrics': {},
    }

# ---------- CHARACTER EVAL ----------
ws = wb['CHARACTER EVAL']
traits = ['workEthic', 'consistency', 'coachability', 'attitude', 'toughness']
for row in ws.iter_rows(min_row=2, values_only=True):
    name = row[0]
    if not name or name not in players:
        continue
    vals = row[1:6]
    players[name]['character'] = {t: (v if v is not None else None) for t, v in zip(traits, vals)}

# ---------- METRIC SHEETS ----------
# Updated per latest workbook: '3 6 3' sheet removed, 'VERT' renamed to 'CMJ', new 'PEAK POWER'
# sheet added under SPEED.
METRIC_SHEETS = [
    ('10YD', '10 Yard Sprint', 'SPEED', 'low', 'sec'),
    ('PEAK POWER', 'Peak Power', 'SPEED', 'high', 'W/kg'),
    ('3 STEP MPH', 'MPH by Step 3', 'SPEED', 'high', 'mph'),
    ('CMJ', 'CMJ', 'BOUNCE', 'high', 'cm'),
    ('APPROACH', 'Approach Jump', 'BOUNCE', 'high', 'in'),
    ('RSI', 'RSI', 'BOUNCE', 'high', ''),
    ('TRAP DEAD', 'TBDL 1RM (.4m/s)', 'STRENGTH', 'high', 'lb'),
    ('BENCH', 'Bench 1RM', 'STRENGTH', 'high', 'lb'),
    ('CHIN UP', 'Chin Up Max Reps', 'STRENGTH', 'high', 'reps'),
    ('BODY FAT', 'Body Fat', 'FITNESS', 'low', '%'),
    ('LEAN MASS', 'Lean Mass', 'FITNESS', 'high', 'lb'),
    ('CELTIC', 'Celtic Test', 'FITNESS', 'high', ''),
]

metric_meta = {}
team_metric_avg = {}

for sheet_name, label, category, direction, unit in METRIC_SHEETS:
    ws = wb[sheet_name]
    header = [c.value for c in ws[1]]
    date_idx = [i for i, h in enumerate(header) if isinstance(h, datetime.datetime)]
    dates = [fmt_date(header[i]) for i in date_idx]
    best_idx = None
    for i, h in enumerate(header):
        if isinstance(h, str) and h.strip().upper() == 'BEST':
            best_idx = i
            break

    coerce_bug = True  # generically guard against Excel mangling e.g. "33.7" into a string "33/7"
    # TRAP DEAD/BENCH previously had a stray bodyweight-multiplier column swept into their own
    # BEST/AVERAGE formulas (fixed in this file, but harmless to keep guarding). PEAK POWER's BEST
    # cell uses =MIN() instead of =MAX() (a copy-paste bug — higher peak power is better), so its
    # own BEST cell would show the worst test instead of the best. For all three, recompute BEST
    # ourselves from only the real dated columns instead of trusting the sheet's own formula.
    recompute_best_from_series = sheet_name in ('TRAP DEAD', 'BENCH', 'PEAK POWER')

    currents = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        name = row[0]
        if not name or name not in players:
            continue
        series = [clean_num(row[i], coerce_slash_decimal=coerce_bug) for i in date_idx]
        first_v = series[0] if series else None
        current_v = series[-1] if series else None
        if recompute_best_from_series:
            clean_series = [v for v in series if v is not None]
            best_v = (max(clean_series) if direction == 'high' else min(clean_series)) if clean_series else None
        else:
            best_v = clean_num(row[best_idx], coerce_slash_decimal=coerce_bug) if best_idx is not None else None
        if best_v == 0:
            best_v = None
        players[name]['metrics'][label] = {
            'series': series,
            'first': first_v,
            'current': current_v,
            'best': best_v,
        }
        if current_v is not None:
            currents.append(current_v)

    team_avg_current = (sum(currents) / len(currents)) if currents else None
    team_metric_avg[label] = team_avg_current

    # Row 20 holds a coach-written description of what the test measures (A20="Description:", B20=text).
    description = None
    label_cell = ws.cell(row=20, column=1).value
    if isinstance(label_cell, str) and label_cell.strip().rstrip(':').upper() == 'DESCRIPTION':
        desc_val = ws.cell(row=20, column=2).value
        if isinstance(desc_val, str) and desc_val.strip():
            description = desc_val.strip()

    metric_meta[label] = {'category': category, 'direction': direction, 'unit': unit, 'dates': dates, 'description': description}

    for n in order:
        m = players[n]['metrics'].get(label)
        if m is None:
            players[n]['metrics'][label] = {'series': [], 'first': None, 'current': None, 'best': None, 'teamAvgCurrent': team_avg_current}
        else:
            m['teamAvgCurrent'] = team_avg_current

data = {
    'order': order,
    'players': players,
    'teamMetricAvg': team_metric_avg,
    'metricMeta': metric_meta,
}

with open('roster_data2.json', 'w') as f:
    json.dump(data, f)

print('players:', len(order))
print('Curry, Alijah CMJ series:', players['Curry, Alijah']['metrics']['CMJ']['series'])
print('Christie, Marvin Peak Power:', players['Christie, Marvin']['metrics']['Peak Power'])
print('Cunningham, Naas weightDates:', players['Cunningham, Naas']['weightDates'])
print('Cunningham, Naas weights:', players['Cunningham, Naas']['weights'])
