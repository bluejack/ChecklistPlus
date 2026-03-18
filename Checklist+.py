# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os
import re

LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def _walk_for(base_dir, target):
    """Walk base_dir tree looking for target filename; return full path or None."""
    for root, dirs, files in os.walk(base_dir):
        if target in files:
            return os.path.join(root, target)
    return None


def find_ckl_file(view, name):
    """Search for name.ckl starting from the current file's dir, then project folders."""
    target = name + ".ckl"

    # First: search from the current file's directory downward
    current_file = view.file_name()
    base_dir = os.path.dirname(current_file) if current_file else None
    if base_dir:
        result = _walk_for(base_dir, target)
        if result:
            return result

    # Then: search from each project folder root.
    # Skip folders already fully covered by the base_dir search above
    # (i.e., folder is equal to or a subdirectory of base_dir).
    window = view.window()
    if window:
        for folder in window.folders():
            norm_folder = os.path.normcase(os.path.normpath(folder))
            if base_dir:
                norm_base = os.path.normcase(os.path.normpath(base_dir))
                if norm_folder.startswith(norm_base + os.sep) or norm_folder == norm_base:
                    continue
            result = _walk_for(folder, target)
            if result:
                return result

    return None


class FileLinkHighlighter(sublime_plugin.ViewEventListener):
    """Dynamically styles /name/ references as links only when name.ckl exists."""

    @classmethod
    def is_applicable(cls, settings):
        syntax = settings.get('syntax', '')
        return 'Checklist+' in syntax

    def on_load(self):
        self.update_links()

    def on_post_save_async(self):
        self.update_links()

    def on_modified_async(self):
        cc = self.view.change_count()
        sublime.set_timeout(lambda: self._debounced_update(cc), 400)

    def _debounced_update(self, change_count):
        if self.view.change_count() == change_count:
            self.update_links()

    def update_links(self):
        resolved_regions = []
        for r in self.view.find_all(r'/([^/\n]+)/'):
            name = self.view.substr(r).strip('/')
            if find_ckl_file(self.view, name):
                resolved_regions.append(r)
        self.view.add_regions(
            "file_links",
            resolved_regions,
            scope="markup.link",
            flags=sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_SOLID_UNDERLINE
        )


class OpenCklUnderCursorCommand(sublime_plugin.TextCommand):

    def run(self, edit, event):
        click_point = self.view.window_to_text((event["x"], event["y"]))
        line = self.view.line(click_point)
        line_text = self.view.substr(line)
        col = click_point - line.begin()

        # Check markdown links first
        for m in LINK_RE.finditer(line_text):
            link_start = m.start(1) - 1  # include the [
            link_end = m.end(1) + 1      # include the ]
            if link_start <= col < link_end:
                sublime.run_command("open_url", {"url": m.group(2)})
                return

        # Fall through to file link logic
        for m in re.finditer(r'/([^/\n]+)/', line_text):
            if m.start() <= col < m.end():
                name = m.group(1)
                resolved = find_ckl_file(self.view, name)
                if resolved:
                    self.view.window().open_file(resolved)
                else:
                    print(f"File not found: {name}.ckl")
                return

    def is_enabled(self, **kwargs):
        syntax = self.view.syntax()
        return syntax and 'Checklist+' in syntax.name

    def want_event(self):
        return True
