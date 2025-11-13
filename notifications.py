import tkinter as tk

_last_toast = None

def _parent_or_root(parent):
    if parent:
        return parent
    try:
        return tk._get_default_root()
    except Exception:
        return None


def _rounded_rect(canvas, x1, y1, x2, y2, r=8, **kwargs):
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def show_toast(parent, message, duration=5000, bg="#98c379", fg="#fff", width=360, height=80, radius=8):
    global _last_toast
    
    if _last_toast:
        try:
            _last_toast.destroy()
        except Exception:
            pass
    
    p = _parent_or_root(parent)
    toast = tk.Toplevel(p)
    toast.overrideredirect(True)
    try:
        toast.attributes("-topmost", True)
        toast.attributes("-alpha", 0.98)
    except Exception:
        pass

    canvas = tk.Canvas(toast, width=width, height=height, highlightthickness=0)
    canvas.pack()

    canvas.create_rectangle(0, 0, width, height, fill=bg, outline="")

    canvas.create_text((width // 2, height // 2), text=message, fill=fg, font=("Segoe UI", 12), width=width - 32)

    toast.update_idletasks()

    if p:
        px = p.winfo_rootx()
        py = p.winfo_rooty()
        pw = p.winfo_width()
        x = px + pw - width - 20
        y = py + 20
    else:
        screen_w = toast.winfo_screenwidth()
        x = screen_w - width - 50
        y = 40

    toast.geometry(f"{width}x{height}+{x}+{y}")
    _last_toast = toast
    toast.after(duration, toast.destroy)
    return toast

def toast_success(parent, message, duration=2500):
    return show_toast(parent, message, duration=duration, bg="#98c379", fg="#000")

def toast_error(parent, message, duration=3500):
    return show_toast(parent, message, duration=duration, bg="#e06c75", fg="#fff")

def toast_warning(parent, message, duration=3000):
    return show_toast(parent, message, duration=duration, bg="#e5c07b", fg="#000")
