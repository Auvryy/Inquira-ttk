_active_canvas = None
_bound = False


def _on_mousewheel(event):
    global _active_canvas
    if _active_canvas is None:
        return

    delta = 0
    if getattr(event, "delta", 0):
        delta = int(-1 * (event.delta / 120))
    elif getattr(event, "num", None) == 4:
        delta = -1
    elif getattr(event, "num", None) == 5:
        delta = 1

    if delta:
        _active_canvas.yview_scroll(delta, "units")


def bind_scroll_wheel(scrollable_frame):
    canvas = getattr(scrollable_frame, "_parent_canvas", None)
    if canvas is None:
        return

    def _enter(_event):
        global _active_canvas
        _active_canvas = canvas

    def _leave(_event):
        global _active_canvas
        if _active_canvas is canvas:
            _active_canvas = None

    scrollable_frame.bind("<Enter>", _enter, add="+")
    scrollable_frame.bind("<Leave>", _leave, add="+")

    global _bound
    if not _bound:
        scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind_all("<Button-4>", _on_mousewheel)
        scrollable_frame.bind_all("<Button-5>", _on_mousewheel)
        _bound = True
