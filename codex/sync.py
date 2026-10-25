#!/usr/bin/env python3
"""Stage/review a local Claude-to-Codex migration; apply only with --apply.

Never imports authentication, permission allowlists, hook trust or literal secrets.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tomllib

HERE = Path(__file__).resolve().parent
HOME = Path.home()
CLAUDE = HOME / '.claude'
CODEX = HOME / '.codex'
FLEET = HOME / 'github'
MARKER = '<!-- AUTO-GENERATED from CLAUDE.md by ~/github/bin/sync-codex-rules.sh — edit the CLAUDE.md, not this file. -->'
NAMES = {'claude-context-picker': 'codex-context-picker', 'torrentX': 'torrentx'}
SECRET = re.compile(r'(?:gh[pous]_[A-Za-z0-9]{36}|sk-ant-[A-Za-z0-9_-]{25,}|sk-[A-Za-z0-9]{40,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)')
BRIDGE = '''\n\n## Codex execution\n\nUse the tools exposed by the current Codex session. Read/Glob/Grep/Bash map to filesystem search and shell tools; Write/Edit map to apply_patch. Use collaboration spawn_agent only when delegation is authorized; use explorer for focused read-only work and worker for implementation. Inherit the current model; Claude sonnet/haiku/opus names are not Codex model identifiers. Respect the current concurrency limit and run larger panels in waves. Preserve existing user authorization and native sandbox approvals. Do not use Claude session databases or Claude account commands to manage Codex chats.\n'''
SESSION = '''---
name: session-order
description: Organize Codex chats and sidebar projects, find old work, archive finished chats reversibly, or restore an archived chat when the user asks to clean up the sidebar or recover a conversation.
---

# Codex chat organization

Discover list_threads and list_projects tools first. Use exact returned chat titles and IDs. Inspect status before changing a chat; preserve active, pinned and unread work unless the user explicitly includes it. Use native sidebar section, pinning and ordering tools for organization. Use set_thread_archived for archiving and list_archived_threads plus set_thread_archived with archived false for restoration. Do not delete chats as part of cleanup. Do not bulk restore manually archived work.

For a broad cleanup request, inspect recent activity and propose a concrete scope when its intent is unclear. If the user has already supplied the scope, execute it. Use native tools while the app is running. Never edit Codex SQLite files, global state JSON or the Claude session store. Claude account-switch and session-repath scripts operate on Claude only and are not Codex recovery tools.
'''
DEPLOY = '''---
name: deploy-homelab
description: Deploy the current project or a supplied project path to the personal homelab when explicitly requested.
---

Read the homelab-deploy skill and ~/.claude/HOMELAB.md. Classify the project, inspect its DEPLOY.md, run required local checks, deploy through its existing target and verify the live URL. If delegation is available and authorized, homelab-ceo can own the deployment. Save each generated credential in 1Password before using it and report the item title and ID. Protect CT 200/201 and homelab-trinity. Alpina demos and POCs use Hetzner Coolify at <name>.alpina-tech.org instead; apply the user's deployment rules. Never mirror secrets into repository files.
'''

def front(text):
    if not text.startswith('---\n'):
        raise ValueError('Missing frontmatter')
    fm, body = text[4:].split('\n---', 1)
    fields = {}
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r'^([\w-]+):\s*(.*)$', line)
        if not m:
            continue
        k, v = m.groups()
        if v in ('|', '>'):
            block = []
            for item in lines[i+1:]:
                if item and not item.startswith((' ', '\t')):
                    break
                block.append(item.strip())
            v = ' '.join(block)
        elif len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
            if v[0] == '"':
                try:
                    v = json.loads(v)
                except ValueError:
                    v = v[1:-1]
            else:
                v = v[1:-1].replace("''", "'")
        fields[k] = v
    return fields, body.lstrip('\n')

def adapt(text):
    for old, new in NAMES.items():
        text = text.replace(old, new)
    for name in skill_names:
        dest = NAMES.get(name, name)
        text = text.replace('~/.claude/skills/' + name, '~/.codex/skills/' + dest)
        text = text.replace(str(CLAUDE / 'skills' / name), str(CODEX / 'skills' / dest))
    text = text.replace('~/.Codex/', '~/.codex/')
    text = text.replace('Claude Code', 'Codex')
    return text

def skill_text(name, source):
    fields, body = front(source)
    description = fields.get('description', 'Use ' + name + ' for its documented workflow.')
    return '---\nname: ' + name + '\ndescription: ' + json.dumps(adapt(description), ensure_ascii=False) + '\n---\n\n' + adapt(body) + BRIDGE

def safe_bytes(path):
    data = path.read_bytes()
    if SECRET.search(data.decode('utf-8', errors='ignore')):
        raise ValueError('Credential-like content in ' + str(path) + '; refusing to stage it')
    return data

def scalar(value):
    # JSON basic scalars/arrays are valid TOML values for the imported fields.
    return json.dumps(value, ensure_ascii=False)

def stage(output):
    output.mkdir(parents=True, exist_ok=True)
    output.chmod(0o700)
    files = {}
    audit = {'skills': [], 'agents': [], 'commands': [], 'mcp': [], 'plugins': [], 'settings': {}}
    def put(relative, data):
        files[relative] = data.encode() if isinstance(data, str) else data
    for src in sorted((CLAUDE / 'skills').iterdir()):
        actual = src
        recovered = False
        if not (src / 'SKILL.md').exists() and src.name.startswith('org-'):
            actual = FLEET / 'personal/PR-PRODUCTS/orgforge/kit/skills' / src.name
            recovered = True
        if not (actual / 'SKILL.md').is_file():
            audit['skills'].append({'name': src.name, 'status': 'missing-source'})
            continue
        if src.name == 'skill-creator':
            audit['skills'].append({'name': src.name, 'status': 'use-native-codex-skill-creator'})
            continue
        name = NAMES.get(src.name, src.name)
        for p in sorted(actual.rglob('*')):
            if not p.is_file() or any(x in p.parts for x in ['__pycache__', '.git', 'node_modules']) or p.suffix == '.pyc':
                continue
            data = safe_bytes(p)
            relative = p.relative_to(actual)
            if relative.as_posix() == 'SKILL.md':
                data = skill_text(name, data.decode())
                if name == 'session-order':
                    data = SESSION
                if name == 'project-new':
                    data += '\n## Shared fleet scaffold\n\nThe bundled new_project.py remains the shared fleet scaffold and intentionally creates Claude metadata too. After running it, generate AGENTS.md next to the new project CLAUDE.md using ~/github/bin/sync-codex-rules.sh --repos, or perform the same marker-preserving transform only for that new project. Do not translate Claude permission allowlists into Codex approvals.\n'
            elif p.suffix in ('.md', '.txt'):
                data = adapt(data.decode('utf-8', errors='strict'))
            put('skills/' + name + '/' + str(relative), data)
        existing = HOME / '.agents/skills' / src.name / 'SKILL.md'
        audit['skills'].append({'name': src.name, 'target': name, 'recovered_broken_link': recovered,
            'shared_existing': existing.exists(), 'status': 'adapted-copy', 'files': sum(k.startswith('skills/' + name + '/') for k in files)})
    # Commands become discoverable Codex skills.
    for p in sorted((CLAUDE / 'commands').glob('*.md')):
        fields, body = front(p.read_text())
        name = p.stem
        text = skill_text(name, '---\nname: ' + name + '\ndescription: ' + json.dumps(fields['description'], ensure_ascii=False) + '\n---\n' + body)
        text = text.replace('$ARGUMENTS', 'the user-supplied arguments')
        if name == 'deploy-homelab':
            text = DEPLOY
        if name == 'analis-load':
            text += '\nAlso inspect Codex processes. A shell PPID is not proof of the chat process ID. Never expose complete command-line arguments that may contain secrets; redact them before display.\n'
        put('skills/' + name + '/SKILL.md', text)
        audit['commands'].append({'name': name, 'status': 'converted-to-skill'})
    config = (CODEX / 'config.toml').read_text()
    parsed = tomllib.loads(config)
    # The Claude plugin sends an empty optional auth header when no key is
    # configured. Codex treats a missing header env var as a config warning.
    # Use Context7's documented anonymous mode rather than inventing a key.
    prior_context = parsed.get('mcp_servers', {}).get('context7')
    if prior_context == {'url': 'https://mcp.context7.com/mcp', 'env_http_headers': {'Authorization': 'CONTEXT7_API_KEY'}}:
        config = re.sub(r'(\[mcp_servers\.context7\]\nurl = "https://mcp.context7.com/mcp"\n)env_http_headers = \{ Authorization = "CONTEXT7_API_KEY" \}\n', r'\1', config)
    # Both legacy ~/.codex and shared ~/.agents roots are discoverable here.
    # Disable only duplicate shared entries in Codex; preserve their files for
    # other agents and keep the native skill creator available.
    configured = {item.get('path') for item in parsed.get('skills', {}).get('config', [])}
    for item in audit['skills']:
        if item['status'] != 'adapted-copy':
            continue
        shared = HOME / '.agents/skills' / item['name'] / 'SKILL.md'
        if shared.exists() and str(shared) not in configured:
            config += '\n[[skills.config]]\npath = ' + scalar(str(shared)) + '\nenabled = false\n'
            item['duplicate_shared_entry'] = 'disabled-in-codex; source file preserved'
    # Keep native persona names already registered. Add missing aliases by source filename.
    agent_tables = []
    for p in sorted((CLAUDE / 'agents').glob('*.md')):
        fields, body = front(p.read_text())
        name = p.stem
        desc = adapt(fields.get('description', name))
        target = 'agents/' + name + '.toml'
        put(target, 'name = ' + scalar(name) + '\ndescription = ' + scalar(desc) + '\ndeveloper_instructions = ' + scalar(adapt(body) + BRIDGE) + '\n')
        if name not in parsed.get('agents', {}):
            agent_tables.append('\n[agents.' + scalar(name) + ']\ndescription = ' + scalar(desc) + '\nconfig_file = ' + scalar(str(CODEX / target)) + '\n')
        audit['agents'].append({'name': name, 'status': 'adapted', 'source_model': fields.get('model', 'inherit'), 'target_model': 'inherit'})
    # Repair existing migrated personas only for known invalid paths.
    for p in (CODEX / 'agents').glob('*.toml'):
        if 'agents/' + p.name in files:
            continue
        data = p.read_text()
        if '~/.Codex/' in data:
            # Keep the actual shared source of operational references.
            put('agents/' + p.name, data.replace('~/.Codex/', '~/.claude/'))
    config += ''.join(agent_tables)
    # Preserve server conflicts. Import only missing non-secret definitions.
    mcp = json.loads((HOME / '.claude.json').read_text()).get('mcpServers', {})
    for name, server in mcp.items():
        if name in parsed.get('mcp_servers', {}):
            audit['mcp'].append({'name': name, 'status': 'preserved-existing', 'same_command': server.get('command') == parsed['mcp_servers'][name].get('command'), 'same_args': server.get('args', []) == parsed['mcp_servers'][name].get('args', [])})
            continue
        if server.get('env') or server.get('headers'):
            audit['mcp'].append({'name': name, 'status': 'needs-secret-reference-review'})
            continue
        command = server.get('command')
        if command and '/' in command and not Path(command).is_file():
            audit['mcp'].append({'name': name, 'status': 'missing-executable'})
            continue
        if any(arg.startswith('/') and not Path(arg).exists() for arg in server.get('args', []) if command != 'ssh'):
            audit['mcp'].append({'name': name, 'status': 'missing-local-script'})
            continue
        values = {k: server[k] for k in ['command', 'args', 'url'] if k in server}
        # Local/LAN URLs contain no credentials. Do not reproduce authenticated URLs.
        if 'url' in values and (re.search(r'[?@#]', values['url']) or not re.match(r'^https?://(?:192\.168\.|127\.0\.0\.1|localhost)', values['url'])):
            audit['mcp'].append({'name': name, 'status': 'needs-url-review'})
            continue
        config += '\n[mcp_servers.' + scalar(name) + ']\n' + ''.join(k + ' = ' + scalar(v) + '\n' for k,v in values.items())
        audit['mcp'].append({'name': name, 'status': 'imported'})
    tomllib.loads(config)
    put('config.toml', config)
    rules = (CLAUDE / 'CLAUDE.md').read_text().replace('Global Claude Code Rules', 'Global Codex Rules').replace('Claude Code', 'Codex')
    rules += '''\n\n## Codex compatibility\n\n- Claude operational documents under ~/.claude/docs and ~/.claude/HOMELAB.md remain shared sources. Resolve docs/*.md against ~/.claude, not the current repository.\n- Use the current Codex tools and inherit its selected model for delegates. Claude model names and slash commands are not Codex configuration. Native approval and sandbox rules take precedence over imported Claude permission lists.\n- The fleet hooks require native review through /hooks before their first run. Session recall reads the canonical Claude journal plus Codex outcomes in ~/.codex/journals. The Stop hook records bounded, filtered final messages without invoking another model. Save durable Codex findings in the project wiki or the appropriate vault.\n- Organize Codex chats through native thread/sidebar tools. Do not edit app databases or Claude session records.\n'''
    put('AGENTS.md', MARKER + '\n\n' + rules)
    hooks = json.loads((CODEX / 'hooks.json').read_text())
    events = hooks.setdefault('hooks', {})
    adapter = CODEX / 'hooks/fleet-adapter.py'
    specs = [('PreToolUse','Bash','bash'),('PreToolUse','apply_patch|Edit|Write|MultiEdit|NotebookEdit','secret'),
             ('PostToolUse','apply_patch|Edit|Write','post'),('SessionStart','startup|resume|clear|compact|fork','recall'),
             ('SessionStart','startup|resume|clear|compact|fork','preflight'),('Stop',None,'git'),('Stop',None,'journal'),('UserPromptSubmit',None,'prompt')]
    for event, matcher, mode in specs:
        command = 'python3 ' + str(adapter) + ' ' + mode
        groups = events.setdefault(event, [])
        if not any(h.get('command') == command for g in groups for h in g.get('hooks', [])):
            group = {'hooks': [{'type':'command','command':command,'timeout':20}]}
            if matcher:
                group['matcher'] = matcher
            groups.append(group)
    put('hooks.json', json.dumps(hooks, ensure_ascii=False, indent=2) + '\n')
    put('hooks/fleet-adapter.py', (HERE / 'hook_adapter.py').read_bytes())
    settings = json.loads((CLAUDE / 'settings.json').read_text())
    # Record disposition of EVERY top-level setting without values or secrets.
    for key in settings:
        audit['settings'][key] = {
            'hooks':'8 adapted handlers; native trust review required; notification/status/audio and Claude transcript writer excluded',
            'permissions':'preserve Codex sandbox and approvals; no blanket allow import',
            'autoMode':'preserve Codex native approval policy',
            'model':'preserve current Codex model', 'effortLevel':'preserve current Codex effort',
            'env':'not copied; shared integrations use existing environment/1Password',
            'enabledPlugins':'audit only; preserve Codex plugin state',
            'attribution':'global rules prohibit AI attribution',
            'theme':'preserve Codex app appearance; generated UI remains light per global rules'
        }.get(key,'Claude-specific; preserve existing Codex behavior')
    # Native replacements for enabled Claude-only maintenance plugins.
    replacements = {
        'agents-md-improver': ('Audit and improve Codex AGENTS.md guidance when the user asks to maintain project instructions or memory rules.',
            'Read applicable AGENTS.md files and compare their instructions with actual repository commands and conventions. Report outdated paths, contradictory rules, repeated generic advice and missing verification commands. Make focused updates within the requested scope. For a generated AGENTS.md, edit its documented source, usually CLAUDE.md, then regenerate using the fleet sync script. Preserve client-authored AGENTS.md files and avoid copying secrets or machine-specific temporary paths.'),
        'session-report': ('Review progress, outcomes and recurring blockers across Codex chats when the user requests a session report.',
            'Discover native list_threads and read_thread tools. Select chats within the requested project and time range; preserve exact returned titles. Summarize completed work, unresolved blockers and evidence from returned turns. Distinguish observed results from inferred outcomes. Use ~/.codex/journals only as bounded outcome memory, not a complete transcript. Do not run Claude session analyzers against Codex storage or read its SQLite files. Do not send messages or change chat states unless explicitly requested.')}
    for name,(description,body) in replacements.items():
        put('skills/' + name + '/SKILL.md', '---\nname: ' + name + '\ndescription: ' + scalar(description) + '\n---\n\n' + body + '\n')
    if 'context7' not in parsed.get('mcp_servers', {}):
        config += '\n[mcp_servers.context7]\nurl = "https://mcp.context7.com/mcp"\n'
        put('config.toml', config)
        audit['mcp'].append({'name':'context7','status':'imported-plugin-equivalent; anonymous mode, optional API key is not required'})
    plugins = json.loads((CLAUDE / 'plugins/installed_plugins.json').read_text()).get('plugins', {})
    for name, installs in plugins.items():
        for install in installs:
            path = Path(install['installPath'])
            skill_files = list(path.glob('skills/*/SKILL.md'))
            # Read all plugin skill content and inventory portability indicators.
            content = '\n'.join(p.read_text(errors='replace') for p in skill_files)
            audit['plugins'].append({'name':name,'enabled_in_claude':settings.get('enabledPlugins',{}).get(name,False),
                'skill_names':[p.parent.name for p in skill_files], 'skill_count':len(skill_files),
                'claude_api_mentions':len(re.findall(r'CLAUDE_PLUGIN_ROOT|claude -p|subagent_type',content)),
                'codex_cache_present':any((CODEX / 'plugins/cache').glob('*/' + name.split('@')[0] + '/*')),
                'status':'preserve-plugin-installation; do not copy Claude manifests'})
    # Read and summarize all active source skill resources without writing them to the report.
    audit['limitations'] = ['New hooks need /hooks trust review; trust hashes are deliberately untouched.',
        'Stop records bounded, filtered final messages in ~/.codex/journals; this is outcome recall, not full transcript summarization.',
        'Existing model, effort, app appearance, approval policy and plugin enabled state are preserved.',
        'Existing MCP definitions win on conflicts, including the different homelab server command.',
        'Claude LSP/status-line/auto-mode and plugin-private services require native equivalents; no fake parity claimed.',
        'MCP runtime connectivity and OAuth must be verified in a fresh Codex session.']
    hashes = {}
    for relative, data in files.items():
        path = output / 'payload' / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(0o600)
        hashes[relative] = hashlib.sha256(data).hexdigest()
    (output / 'manifest.json').write_text(json.dumps(hashes,indent=2)+'\n')
    (output / 'audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'stage':str(output),'files':len(files),'skills':len(audit['skills']),'agents':len(audit['agents']),'commands':len(audit['commands']),'mcp':audit['mcp']},ensure_ascii=False))

def apply(output):
    manifest = json.loads((output / 'manifest.json').read_text())
    changes = []
    for relative, digest in manifest.items():
        source = output / 'payload' / relative
        if '..' in Path(relative).parts or Path(relative).is_absolute():
            raise ValueError('Invalid target path')
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError('Staged file changed: ' + relative)
        dest = CODEX / relative
        if dest.is_symlink():
            raise ValueError('Refusing to overwrite symlink: ' + str(dest))
        if dest.exists() and dest.read_bytes() == data:
            continue
        changes.append((relative, data))
    # Refuse stale merges if another session changed the base config/hooks.
    bases = json.loads((output / 'bases.json').read_text())
    for name,digest in bases.items():
        current = hashlib.sha256((CODEX / name).read_bytes()).hexdigest()
        staged = manifest.get(name)
        if current not in (digest, staged):
            raise ValueError('Configuration changed after staging: ' + name + '. Restage first.')
    backup = CODEX / 'backups' / ('claude-parity-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    if changes:
        backup.mkdir(parents=True)
        backup.chmod(0o700)
        ledger = []
        for relative,data in changes:
            dest = CODEX / relative
            existed = dest.exists() or dest.is_symlink()
            ledger.append({'path':relative,'existed':existed})
            if existed:
                target = backup / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dest,target)
        (backup / 'ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
        for relative,data in changes:
            dest = CODEX / relative
            dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.is_symlink():
                raise ValueError('Refusing to overwrite symlink: ' + str(dest))
            temp = dest.with_name(dest.name + '.parity-tmp')
            temp.write_bytes(data)
            temp.chmod(0o600)
            temp.replace(dest)
    print(json.dumps({'changed':len(changes),'backup':str(backup) if changes else None}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',type=Path,required=True)
    parser.add_argument('--apply',action='store_true')
    args = parser.parse_args()
    skill_names = [p.name for p in (CLAUDE / 'skills').iterdir()]
    if args.apply:
        apply(args.stage)
    else:
        stage(args.stage)
        (args.stage / 'bases.json').write_text(json.dumps({n:hashlib.sha256((CODEX/n).read_bytes()).hexdigest() for n in ['config.toml','hooks.json','AGENTS.md']},indent=2)+'\n')
