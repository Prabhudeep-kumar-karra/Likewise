"""Stored p-values and scan-level inference for one completed scan."""
from __future__ import annotations

from ..charts import _rank_p_chart, _scan_z_chart
from ..format import e
from ..layout import blocked_banner, corners, page, tripwire_chip


def statistics_page(sid: str, rec: dict, summary: dict,
                    findings: list[dict], controls: dict | None) -> str:
    test = summary.get("scan_level_test") or {}
    adequate = sum(1 for f in findings if f.get("cell_power") == "adequate")
    underpowered = sum(1 for f in findings if f.get("cell_power") == "underpowered")
    z = test.get("z")
    p = test.get("p")
    direction = (
        "Positive values are the direction the stated reasons would be harder to justify; "
        "negative values point the other way. This is one pooled test across matched cells, "
        "not a z-score for each case.")
    if z is not None and float(z) < 0:
        reading = ("The observed statistic is negative, opposite the tested direction. "
                   "The stored one-sided p-value is %s." % ("not computed" if p is None else e(p)))
    elif z is not None:
        reading = ("The observed statistic is in the tested direction. The stored one-sided "
                   "p-value is %s." % ("not computed" if p is None else e(p)))
    else:
        reading = "The scan-level statistic could not be computed for this scan."

    rows = []
    for index, finding in enumerate(findings, 1):
        fid = str(finding.get("finding_id", ""))
        label = fid[4:12] if fid.startswith("fnd_") else fid[:8]
        rank_p = finding.get("rank_p_value")
        rank_p_text = "not computed" if rank_p is None else "%.6g" % float(rank_p)
        state = "Not enough for significance" if finding.get("cell_power") == "underpowered" else "Eligible"
        rows.append(
            '<tr><td class="mono">%d</td><td><a href="/ui/scans/%s/findings/%s">%s</a></td>'
            '<td class="mono">%s</td><td class="mono">%s</td><td>%s</td></tr>' % (
                index, e(sid), e(fid), e(label), e(finding.get("rank_in_cell")),
                e(rank_p_text), e(state)))

    body = f"""
{blocked_banner(controls, summary)}
<div style="display:flex;align-items:center;gap:14px;margin:14px 0;flex-wrap:wrap">
  <a class="mono" href="/ui/scans/{e(sid)}/queue">← Back to queue</a>
  <span class="spacer"></span>
  <span class="mono muted" style="font-size:11px">{len(findings)} candidate pairs ·
    {adequate} eligible · {underpowered} below power floor</span>
</div>
<h1 class="page">P-values and scan-level z</h1>
<p class="lede">The plot shows the stored within-cell rank p-value for each candidate, in queue order.
  These are descriptive per-pair ranks, not individual significance tests. The z chart below is
  the single pooled scan-level test; no per-case z-scores are computed.</p>

<div class="card blueprint" style="margin-bottom:18px">{corners()}
  <h2 class="sec">WITHIN-CELL RANK P-VALUES · {len(findings)} CASES</h2>
  <p class="muted" style="font:12px/1.5 var(--font-body);margin:0 0 8px">
    Lower values mean the denied record sits nearer the worse-ranked end of its own comparison
    cell. They do not establish case-level significance after multiplicity or the cell-power gate.</p>
  <div class="scroll-x">{_rank_p_chart(findings, sid)}</div>
  <div class="scroll-x"><table class="data">
    <tr><th>QUEUE #</th><th>CASE</th><th>WITHIN-CELL RANK</th><th>RANK P</th><th>POWER STATUS</th></tr>
    {''.join(rows)}
  </table></div>
</div>

<div class="two">
  <div class="card blueprint">{corners()}
    <h2 class="sec">POOLED SCAN-LEVEL TEST</h2>
    <div class="scroll-x">{_scan_z_chart(test)}</div>
    <p class="muted" style="font:12px/1.5 var(--font-body);margin:8px 0 0">{direction}</p>
    <p style="font:13px/1.5 var(--font-body);margin:8px 0 0">{reading}</p>
  </div>
  <div class="card">{corners()}
    <h2 class="sec">STORED TEST VALUES</h2>
    <div style="display:grid;grid-template-columns:1fr auto;gap:8px;font:12.5px/1.4 var(--font-body)">
      <span>z-score</span><b class="mono">{e(z if z is not None else 'not computed')}</b>
      <span>one-sided p-value</span><b class="mono">{e(p if p is not None else 'not computed')}</b>
      <span>matched cells used</span><b class="mono">{e(test.get('cells_used', 'not available'))}</b>
      <span>adequate candidate cells</span><b class="mono">{adequate}</b>
      <span>below power floor</span><b class="mono">{underpowered}</b>
    </div>
    <p class="mono muted" style="font-size:10.5px;line-height:1.55;margin:12px 0 0">
      Scan {e(sid)} · exploratory status and tripwire limits still apply.</p>
  </div>
</div>
"""
    return page("Statistics", body, active="queue", sid=sid,
                crumb="Scans / " + sid + " / Statistics", chip=tripwire_chip(summary))