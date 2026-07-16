---
name: obsidian
description: Work with Obsidian vault — create, read, search, and edit notes. Use when the user mentions notes, obsidian, vault, or knowledge base.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: "[action] [note-name or search query]"
---

# Obsidian Vault Skill

## Vault Location

The Obsidian vault is located at: `~/Obsidian`

If the vault path does not exist, ask the user where their vault is located.

## Core Actions

### Create a note
- Create `.md` files in the vault directory
- Use YAML frontmatter with `date`, `tags` fields
- Use `[[wiki-links]]` for linking between notes
- Follow the existing folder structure in the vault

### Search notes
- Use Grep to search note contents
- Use Glob to find notes by name pattern: `~/Obsidian/**/*.md`

### Edit a note
- Read the note first, then use Edit to modify

### List notes
- Use Glob `~/Obsidian/**/*.md` to list all notes
- Use Glob with subfolder patterns to list notes in specific folders

### Daily note
- Path format: `~/Obsidian/Daily/YYYY-MM-DD.md`
- Template:

```markdown
---
date: {{date}}
tags: [daily]
---

# {{date}}

## Tasks
- [ ]

## Notes

## Links
```

## Formatting Rules

- Use Obsidian-flavored Markdown
- Internal links: `[[Note Name]]` or `[[folder/Note Name|Display Text]]`
- Tags: `#tag-name` inline or in frontmatter `tags: [tag1, tag2]`
- Callouts: `> [!note]`, `> [!warning]`, `> [!tip]`
- Do not break existing links when editing notes
