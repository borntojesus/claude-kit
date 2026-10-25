#!/usr/bin/env python3
"""Adapt existing fleet hooks to Codex tool payloads without changing Claude."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import hashlib
import datetime

SOURCE = Path.home() / '.claude/hooks'

def journal_dir(data):
    cwd = Path(data.get('cwd') or os.getcwd())
    root = subprocess.run(['git', '-C', str(cwd), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    project = root.stdout.strip() if root.returncode == 0 else str(cwd)
    slug = re.sub(r'[^A-Za-z0-9_-]', '-', Path(project).name)[:80]
    return Path.home() / '.codex/journals' / (slug + '-' + hashlib.sha256(project.encode()).hexdigest()[:10])

def journal(data):
    message = data.get('last_assistant_message') or ''
    if not message or data.get('stop_hook_active'):
        return {}
    # Retain outcome text, never raw tool output or prompts. Drop suspicious
    # lines entirely, including credentials not covered by provider prefixes.
    message = '\n'.join(line for line in message.splitlines() if not re.search(
        r'gh[pous]_|github_pat_|sk-ant-|sk-[A-Za-z0-9]{20}|xox[baprs]-|BEGIN .*PRIVATE KEY|eyJ[A-Za-z0-9_-]{20}|(?:password|token|secret|пароль|токен)\s*[:=]|://[^/\s]+:[^/\s]+@', line, re.I))[:6000]
    if not message.strip():
        return {}
    key = hashlib.sha256((str(data.get('session_id')) + ':' + str(data.get('turn_id')) + ':' + message).encode()).hexdigest()
    target = journal_dir(data)
    target.mkdir(parents=True, exist_ok=True)
    target.chmod(0o700)
    entry = target / (key + '.md')
    if not entry.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with entry.open('x') as stream:
            stream.write('## ' + stamp + '\n\n' + message + '\n')
        entry.chmod(0o600)
    return {}

def edits(data):
    ti = data.get('tool_input') or {}
    if isinstance(ti, str):
        ti = {'command': ti}
    patch = ti.get('command') or ti.get('patch') or ti.get('input') or ''
    if data.get('tool_name') != 'apply_patch' and not patch.startswith('*** Begin Patch'):
        yield data
        return
    current = None
    content = []
    for line in patch.splitlines():
        match = re.match(r'\*\*\* (?:Add|Update|Delete) File: (.+)', line)
        if match:
            if current:
                yield dict(data, tool_input={'file_path': current, 'content': '\n'.join(content)})
            current, content = match[1], []
        elif line.startswith('*** Move to: '):
            current = line[len('*** Move to: '):]
        elif line.startswith('+'):
            content.append(line[1:])
    if current:
        yield dict(data, tool_input={'file_path': current, 'content': '\n'.join(content)})

def run(name, data):
    path = SOURCE / name
    if not path.is_file():
        return {}
    ti = data.get('tool_input')
    if isinstance(ti, dict) and ti.get('file_path'):
        path_value = Path(ti['file_path'])
        if not path_value.is_absolute():
            data = dict(data, tool_input=dict(ti, file_path=str(Path(data.get('cwd') or os.getcwd()) / path_value)))
    result = subprocess.run(['bash', str(path)], input=json.dumps(data), text=True,
                            capture_output=True, timeout=12, cwd=data.get('cwd') or None)
    if result.returncode == 2:
        return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny',
                'permissionDecisionReason': 'Fleet hook blocked this action; inspect the source hook.'}}
    try:
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except ValueError:
        return {}

def main(mode, data):
    if mode == 'bash':
        ti = data.get('tool_input') or {}
        if isinstance(ti, dict):
            ti = dict(ti, command=ti.get('command') or ti.get('cmd') or '')
        data = dict(data, tool_name='Bash', tool_input=ti)
        return run('bash-guard.sh', data)
    if mode == 'secret':
        for item in edits(data):
            result = run('secret-guard.sh', item)
            hs = result.get('hookSpecificOutput', {})
            if hs.get('permissionDecision') in ('ask', 'deny'):
                # Codex does not support ask. Block this write so the model can
                # store the credential in 1Password and retry without it.
                hs['permissionDecision'] = 'deny'
                hs['permissionDecisionReason'] = 'Possible credential in repository write. Store it in 1Password first and use a reference. Request explicit approval if this write is intentional.'
                return result
        return {}
    if mode == 'post':
        contexts = []
        for item in edits(data):
            run('format.sh', item)
            result = run('copy-lint.sh', item)
            context = result.get('hookSpecificOutput', {}).get('additionalContext')
            if context:
                contexts.append(context)
        if contexts:
            return {'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': '\n'.join(contexts)}}
        return {}
    if mode == 'recall':
        # Read the canonical cross-agent journal, never feed Codex transcripts
        # to the Claude-only summarizer.
        result = run('session-recall.sh', data)
        entries = sorted(journal_dir(data).glob('*.md'), key=lambda p: p.stat().st_mtime)[-4:]
        if entries:
            hs = result.setdefault('hookSpecificOutput', {'hookEventName': 'SessionStart'})
            hs['additionalContext'] = (hs.get('additionalContext', '') + '\nRecent Codex outcomes:\n' + '\n'.join(p.read_text() for p in entries))[-9000:]
        return result
    if mode == 'journal':
        return journal(data)
    return run({'preflight': 'repo-preflight.sh', 'git': 'git-state.sh', 'prompt': 'prompt-router.sh'}[mode], data)

if __name__ == '__main__':
    try:
        output = main(sys.argv[1], json.load(sys.stdin))
        if output:
            print(json.dumps(output, ensure_ascii=False))
    except Exception as exc:
        # Advisory bridge failures are visible, never silently presented as a pass.
        print(json.dumps({'systemMessage': 'Fleet hook adapter failed: ' + type(exc).__name__}))
