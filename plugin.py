import sublime
import sublime_plugin


State = {
    'view': None,
    'widget': None
}


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

        # If the user 'just' opens another widget for another view,
        # Sublime fires 'on_done' **after** opening the other one,
        # so before we clear here, we need to check if we're still
        # the 'owner'.
        if State['view'] == view:
            State.clear()

    on_cancels = on_done

    caption = 'Enter selector to highlight in the view'
    initial_text = get_scope_under_cursor(view)
    widget = window.show_input_panel(
        caption, initial_text, on_done, on_change, on_cancels)

    State.update({
        'view': view,
        'widget': widget
    })


REGION_KEY = 'HS.highlight_scopes'
HIGHLIGHT_SCOPE = 'comment'
HIGHLIGHT_FLAGS = sublime.DRAW_NO_OUTLINE


def highlight_regions(view, regions):
    scope = HIGHLIGHT_SCOPE
    flags = HIGHLIGHT_FLAGS
    view.add_regions(REGION_KEY, regions, scope=scope, flags=flags)


def erase_regions(view):
    view.erase_regions(REGION_KEY)


def get_scope_under_cursor(view):
    cursor = get_cursor(view)
    return view.scope_name(cursor)


def get_cursor(view):
    sel = view.sel()
    try:
        first_sel = next(iter(sel))
    except StopIteration:
        cursor = 0
    else:
        cursor = first_sel.begin()

    return cursor


class UpdateWidgetText(sublime_plugin.EventListener):
    def on_selection_modified_async(self, view):
        parent_view = State.get('view')
        if not parent_view or view.id() != parent_view.id():
            return

        widget = State.get('widget')
        if not widget:
            return

        scope = get_scope_under_cursor(parent_view)
        widget.run_command('_replace_view_text', {'text': scope})


class _replace_view_text(sublime_plugin.TextCommand):
    def run(self, edit, text=''):
        view = self.view

        region = sublime.Region(0, view.size())
        view.replace(edit, region, text)
