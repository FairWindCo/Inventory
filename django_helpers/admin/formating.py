def format_popup(title, text=None, href=None):
    if not href and not text:
        return title
    else:
        start_link = f'<a class="fw_tooltip" href="{href}">' if href else '<a class="fw_tooltip">'
        internal_text = f'<span class="tooltiptext tooltiplong">{text}</span>'
    return f'{start_link}{title}{internal_text}</a>'
