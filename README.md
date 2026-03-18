# Checklist+

A Sublime Text syntax that rivals Obsidian.

Checklist+ began with me making lots of todo lists, and evolved into this: part todo list, part note-taking app, part wiki. I found my todo lists were swiftly becoming a personal knowledge system for capturing tasks, notes, plans, logs, and tracking time. If you've ever found yourself managing your life in a text editor, this was built for you.

---

## Take a peek:

![Checklist+ in action](screenshots/demo.gif)

---

## What It's For

- **Todo lists and checklists** — track what needs doing and what's done
- **Note-taking** — capture thoughts alongside your tasks
- **Planning** — outline projects, break down work, think on the page
- **Time tracking and logging** — record what you did and when
- **A personal knowledgebase** — link files together into a navigable system

---

## Requirements

- Sublime Text 4

---

## Installation

**Via Package Control (recommended)**
1. Open the command palette: `Ctrl+Shift+P` / `Cmd+Shift+P`
2. Select `Package Control: Install Package`
3. Search for `Checklist+`

**Manual**
Clone or download this repo into your Sublime `Packages/` folder:
```
git clone https://github.com/bluejack/Checklist+ "Packages/Checklist+"
```

Supported syntaxes:

```
Checklists: (all take x or . to fill)

[ ] Bracket
( ) Paren
< > Angle Bracket
{ } Curly Bracket

Bullets:

* List Star
- List Dash
> List Prompt
. List Dot

Numbered Lists:

1. Item one
32. Item 32. 

Heading Indicators:

# H1 
## H2 
### H3 

=> A different kind of line 
==> A lesser one of those

Comments:

:: Type 1 (single line)
// Type 2 (single line)
<-- block  --> (multiline)
+-  block2 -+  (multiline)
/*  block3 */  (multiline)

Links:

/* NOTE:

   Links can be followed by right-clicking.
   All links will trigger syntax /string/
   But if the file doesn't match a filename on your drive 
     in the current folder hierarchy; no arrow Indicators
    will appear.

*/

/link/ :: Right-click to load the nearby link.ckl file in Sublime 4
```

---

## File Format

Checklist+ files use the `.ckl` extension. Create any file ending in `.ckl` and the syntax, highlighting, and color scheme features activate automatically. This overrides your otherwise-chosen color scheme, so feel free to edit the color scheme to suit your needs.

---

## Linking Files

Wrap any filename (without extension) in forward slashes to create a live link:

```
/project-notes/
/meeting-log-march/
/someday-maybe/
```

- If a matching `.ckl` file exists in the same folder or any subfolder, it becomes **clickable**
- **Right-click** (or two-finger click on trackpad) anywhere on the link to open the file
- Unresolved links render as plain text so you know when you made a typo.

This turns a folder of `.ckl` files into a lightweight personal wiki.

---

## Color Scheme

Checklist+ ships with a dedicated color scheme that activates automatically for `.ckl` files, leaving your other Sublime themes untouched.

Because Checklist+ makes extensive use of markdown syntax that few color schemes support, either in whole or in part, I found it easier to hard-link these... however, if you don't like it, the file is right there in your Packages folder to edit.

---

## Feature requests & bug reports

You can leave either of these things [here][issues]. Pull requests are welcomed
heartily, but please read [CONTRIBUTING.md][contrib] first! Basically: in this
repo, the main development branch is `dev` and the stable 'production'
branch is `main`. Please remember to base your branch from `dev` and issue
the pull request back to that branch.

---

## Changelog

### v1.0.1 - Patch release (2026.03.18)

* Tweaks to improve paragraph display for longer text.

### v1.0.0 - Initial Publication (2026.03.13)

* Checklist of various types
* Bullet points
* Comments
* Headers
* File linking

## License

MIT — do what thou will.

---

## Background

This package grew out of years of personal use. What started as a structured todo list format slowly expanded to cover planning sessions, work logs, meeting notes, and long-term reference material. The link syntax emerged from a real need to navigate between related files without leaving the editor. If it's useful to you, I'd love to hear how you're using it.
