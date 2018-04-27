import sublime
import sublime_plugin


class highlight_scopes_interactive(sublime_plugin.WindowCommand):
    def run(self):
        window = self.window
        view = window.active_view()

        _highlight_scopes_interactive(view)


def _highlight_scopes_interactive(view):
    window = view.window()

    def on_change(text):
        regions = view.find_by_selector(text)
        highlight_regions(view, regions)

    def on_done(_text=None):
        erase_regions(view)

    on_cancels = on_done
    sel = view.sel()
    try:
        first_sel = next(iter(sel))
    except StopIteration:
        cursor = 0
    else:
        cursor = first_sel.begin()

    caption = 'Enter selector to highlight in the view'
    initial_text = view.scope_name(cursor)
    window.show_input_panel(
        caption, initial_text, on_done, on_change, on_cancels)


REGION_KEY = 'HS.highlight_scopes'
HIGHLIGHT_SCOPE = 'comment'
HIGHLIGHT_FLAGS = sublime.DRAW_NO_OUTLINE


def highlight_regions(view, regions):
    scope = HIGHLIGHT_SCOPE
    flags = HIGHLIGHT_FLAGS
    view.add_regions(REGION_KEY, regions, scope=scope, flags=flags)


def erase_regions(view):
    view.erase_regions(REGION_KEY)
