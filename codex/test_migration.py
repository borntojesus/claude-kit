#!/usr/bin/env python3
"""Behavioral checks for Codex payload adaptation and migration integrity."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('adapter', HERE / 'hook_adapter.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class AdapterTests(unittest.TestCase):
    def test_multiple_patch_files_and_move(self):
        items = list(mod.edits({'tool_name':'apply_patch','tool_input':{'command':'*** Begin Patch\n*** Add File: one.ts\n+hello\n*** Update File: old.ts\n*** Move to: new.ts\n-old\n+new\n*** End Patch'}}))
        self.assertEqual([x['tool_input'] for x in items],[{'file_path':'one.ts','content':'hello'},{'file_path':'new.ts','content':'new'}])

    def test_secret_ask_becomes_supported_deny_without_echo(self):
        with patch.object(mod, 'run', return_value={'hookSpecificOutput':{'permissionDecision':'ask','permissionDecisionReason':'secret-value'}}):
            result = mod.main('secret', {'tool_name':'Write','tool_input':{'file_path':'app.ts','content':'x'}})
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'],'deny')
        self.assertNotIn('secret-value',json.dumps(result))

    def test_exec_command_normalization(self):
        with patch.object(mod, 'run', return_value={}) as call:
            mod.main('bash', {'tool_name':'exec_command','tool_input':{'cmd':'git status'}})
        self.assertEqual(call.call_args.args[1]['tool_input']['command'],'git status')

    def test_real_secret_guard_receives_patch(self):
        if not (mod.SOURCE / 'secret-guard.sh').exists():
            self.skipTest('source guard unavailable')
        # A synthetic provider token, never a real credential.
        token = 'ghp_' + 'A' * 36
        result = mod.main('secret', {'tool_name':'apply_patch','cwd':str(HERE),'tool_input':{'command':'*** Begin Patch\n*** Add File: app.ts\n+const key = "' + token + '"\n*** End Patch'}})
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'],'deny')
        self.assertNotIn(token,json.dumps(result))

    def test_real_bash_guard_rejects_ai_attribution(self):
        if not (mod.SOURCE / 'bash-guard.sh').exists():
            self.skipTest('source guard unavailable')
        result = mod.main('bash', {'tool_name':'Bash','cwd':str(HERE),'tool_input':{'command':'git commit -m "fix: sample\n\nCo-Authored-By: Claude"'}})
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'],'deny')

    def test_journal_dedup_redaction_and_recall(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(mod.Path, 'home', return_value=Path(tmp)), patch.object(mod, 'run', return_value={}):
            data = {'cwd':tmp,'session_id':'s','turn_id':'t','last_assistant_message':'Fixed issue.\npassword: unsafe-example\nVerified build.'}
            mod.main('journal',data)
            mod.main('journal',data)
            files = list(Path(tmp).glob('.codex/journals/*/*.md'))
            self.assertEqual(len(files),1)
            text = files[0].read_text()
            self.assertNotIn('unsafe-example',text)
            self.assertIn('Verified build.',mod.main('recall',data)['hookSpecificOutput']['additionalContext'])

class StageTests(unittest.TestCase):
    def test_payload_integrity(self):
        stage = Path(os.environ.get('PARITY_STAGE','/private/tmp/codex-claude-parity'))
        audit = json.loads((stage / 'audit.json').read_text())
        self.assertFalse([s for s in audit['skills'] if s['status']=='missing-source'])
        self.assertEqual(len([s for s in audit['skills'] if s.get('recovered_broken_link')]),5)
        for p in (stage / 'payload').rglob('*.toml'):
            tomllib.loads(p.read_text())
        for p in (stage / 'payload/skills').glob('*/SKILL.md'):
            text = p.read_text()
            self.assertTrue(text.startswith('---\nname: ' + p.parent.name + '\n'))
            desc = text.split('\ndescription: ',1)[1].split('\n',1)[0]
            self.assertGreater(len(desc),10)
        native = tomllib.loads((Path.home()/'.codex/config.toml').read_text())
        staged = tomllib.loads((stage/'payload/config.toml').read_text())
        for key in ['model','model_reasoning_effort','features','plugins','hooks','permissions','sandbox_mode','approval_policy']:
            self.assertEqual(native.get(key),staged.get(key),key)
        for name,server in native.get('mcp_servers',{}).items():

            if name == 'context7' and server == {'url':'https://mcp.context7.com/mcp','env_http_headers':{'Authorization':'CONTEXT7_API_KEY'}}:
                self.assertEqual(staged['mcp_servers'][name], {'url':'https://mcp.context7.com/mcp'})
            else:
                self.assertEqual(server,staged['mcp_servers'][name])
        original = json.loads((Path.home()/'.codex/hooks.json').read_text())
        new = json.loads((stage/'payload/hooks.json').read_text())
        for event,groups in original['hooks'].items():
            for group in groups:
                self.assertIn(group,new['hooks'][event])

if __name__ == '__main__':
    unittest.main(verbosity=2)
