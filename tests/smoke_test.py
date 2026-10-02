"""Synthetic helper checks; no translation quality claims."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]

def run(script, *args):
    return subprocess.run([sys.executable, str(ROOT/'scripts'/script), *map(str,args)], capture_output=True, text=True)

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    source = tmp/'source.pdf'
    d = fitz.open(); p = d.new_page()
    p.insert_text((50,70), 'Synthetic paper inventory fixture, 2026.')
    d.save(source); d.close()
    inventory_dir = tmp/'inventory'
    first = run('paper_inventory.py',source,inventory_dir,'--no-render')
    assert first.returncode == 0, first.stderr
    inv = json.loads((inventory_dir/'inventory.json').read_text())
    assert len(inv['pages']) == 1 and len(inv['units']) == 1
    assert inv['source']['sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
    plan_path = inventory_dir/'translation.json'
    original_plan = plan_path.read_bytes()
    second = run('paper_inventory.py',source,inventory_dir,'--no-render')
    assert second.returncode == 0 and plan_path.read_bytes() == original_plan
    audit = run('audit_translation.py', inventory_dir/'inventory.json',plan_path,source,tmp/'qa')
    assert audit.returncode == 1, audit.stdout + audit.stderr
    report = json.loads((tmp/'qa'/'audit.json').read_text())
    assert report['issues'], 'Incomplete translation/reviews must fail'
    optimize = run('optimize_pdf_fonts.py',source,source)
    assert optimize.returncode != 0 and 'Keep the original' in optimize.stderr
    for script in ['paper_inventory.py','overlay_regions.py','audit_translation.py','optimize_pdf_fonts.py']:
        help_result = run(script,'--help')
        assert help_result.returncode == 0, help_result.stderr
print('PASS: inventory, plan preservation, incomplete-audit rejection, source overwrite rejection, CLI help')
