from pathlib import Path
def prompt(): return (Path(__file__).resolve().parents[2]/'prompts'/'diagnose_prompt.md').read_text(encoding='utf-8')
