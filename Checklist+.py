# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os
import re

def find_ckl_file(view, name):
    """Search current file's dir and all subdirs for name.ckl"""
    current_file = view.file_name()
    if not current_file:
        return None
    base_dir = os.path.dirname(current_file)
    target = name + ".ckl"
    for root, dirs, files in os.walk(base_dir):
        if target in files:
            return os.path.join(root, target)
    return None


class FileLinkListener(sublime_plugin.ViewEventListener):

    def __init__(self, view):
        super().__init__(view)
        self.phantom_set = sublime.PhantomSet(self.view, "file_links")

    def on_load(self):
        self.update_phantoms()

    def on_modified(self):
        self.update_phantoms()

    def update_phantoms(self):
        phantoms = []
        regions = self.view.find_all(r'/([^/\n]+)/')
        for r in regions:
            name = self.view.substr(r).strip('/')
            resolved = find_ckl_file(self.view, name)
            if resolved:
                html = f'<a href="open:{resolved}">↗</a>'
                phantoms.append(
                    sublime.Phantom(r, html, sublime.LAYOUT_INLINE, self.on_click)
                )
        self.phantom_set.update(phantoms)

    def on_click(self, href):
        _, path = href.split(":", 1)
        self.view.window().open_file(path)

class OpenCklUnderCursorCommand(sublime_plugin.TextCommand):

    def run(self, edit, event):
        click_point = self.view.window_to_text((event["x"], event["y"]))
        line = self.view.line(click_point)
        line_text = self.view.substr(line)
        col = click_point - line.begin()

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