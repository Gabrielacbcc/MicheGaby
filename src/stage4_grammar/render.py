from html import escape

from src.profiles import profile_names
from src.stage4_grammar.dsl import model_to_dict

LABELS = {
    "FULL_STACK_DEVELOPER": "Full Stack Developer",
    "MACHINE_LEARNING_ENGINEER": "Machine Learning Engineer",
    "DEVOPS_ENGINEER": "DevOps Engineer",
    "DATA_ENGINEER": "Data Engineer",
}


def render_markdown(model):
    """Short Markdown visualization of a validated candidate model."""
    d = model_to_dict(model)
    lines = [f"# {d['name'] or 'Unnamed candidate'}", ""]
    if d["email"] or d["phone"]:
        lines.append(" | ".join(x for x in (d["email"], d["phone"]) if x))
        lines.append("")
    if d["education"]:
        lines += ["## Education", ""]
        lines += [f"- {e['degree']}, {e['institution']} ({e['year']})" for e in d["education"]]
        lines.append("")
    if d["experience"]:
        lines += ["## Experience", ""]
        lines += [f"- {e['role']}, {e['company']} ({e['duration']})" for e in d["experience"]]
        lines.append("")
    lines += ["## Profile screening", "", "| Profile | Result | Normalized qualifications |", "|---|---|---|"]
    for p in profile_names():
        mark = "ACCEPTED" if d["results"][p] else "REJECTED"
        lines.append(f"| {LABELS[p]} | {mark} | {', '.join(d['qualifications'][p]) or '-'} |")
    lines += ["", "_ResumeLens checks whether stated qualifications satisfy a formal pattern. It does not rank candidates or make hiring decisions._"]
    return "\n".join(lines)


def render_html(model):
    """Short, self-contained HTML page of a validated candidate model."""
    d = model_to_dict(model)
    e = escape
    rows = []
    for p in profile_names():
        ok = d["results"][p]
        chips = "".join(f"<span class='chip'>{e(t)}</span>" for t in d["qualifications"][p]) or "<em>none</em>"
        rows.append(
            f"<tr><td>{e(LABELS[p])}</td>"
            f"<td><span class='badge {'ok' if ok else 'no'}'>{'ACCEPTED' if ok else 'REJECTED'}</span></td>"
            f"<td>{chips}</td></tr>"
        )
    edu = "".join(f"<li>{e(x['degree'])}, {e(x['institution'])} ({e(x['year'])})</li>" for x in d["education"])
    exp = "".join(f"<li>{e(x['role'])}, {e(x['company'])} ({e(x['duration'])})</li>" for x in d["experience"])
    contact = " &middot; ".join(e(x) for x in (d["email"], d["phone"]) if x)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>ResumeLens: {e(d['name'] or 'Unnamed candidate')}</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;max-width:820px;margin:2rem auto;padding:0 1rem;color:#222}}
h1{{margin-bottom:.2rem}} .contact{{color:#555}} table{{border-collapse:collapse;width:100%;margin-top:.5rem}}
td,th{{border:1px solid #ddd;padding:.5rem;text-align:left;vertical-align:top}}
.chip{{display:inline-block;background:#eef;border-radius:10px;padding:1px 8px;margin:2px;font-size:.85rem}}
.badge{{padding:2px 8px;border-radius:4px;color:#fff;font-weight:600}} .ok{{background:#2e7d32}} .no{{background:#9e9e9e}}
footer{{margin-top:2rem;color:#777;font-size:.85rem}}
</style></head><body>
<h1>{e(d['name'] or 'Unnamed candidate')}</h1>
<div class="contact">{contact}</div>
{'<h2>Education</h2><ul>' + edu + '</ul>' if edu else ''}
{'<h2>Experience</h2><ul>' + exp + '</ul>' if exp else ''}
<h2>Profile screening</h2>
<table><tr><th>Profile</th><th>Result</th><th>Normalized qualifications</th></tr>{''.join(rows)}</table>
<footer>ResumeLens checks whether stated qualifications satisfy a formal pattern. It does not rank candidates or make hiring decisions.</footer>
</body></html>"""
