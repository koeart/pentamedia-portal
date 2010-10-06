def getTerminalSize():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])


class drug():
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])


style = drug(**dict(
        default    = "\033[m",
        # styles
        bold       = "\033[1m",
        underline  = "\033[4m",
        blink      = "\033[5m",
        reverse    = "\033[7m",
        concealed  = "\033[8m",
        # font colors
        black      = "\033[30m",
        red        = "\033[31m",
        green      = "\033[32m",
        yellow     = "\033[33m",
        blue       = "\033[34m",
        magenta    = "\033[35m",
        cyan       = "\033[36m",
        white      = "\033[37m",
        # background colors
        on_black   = "\033[40m",
        on_red     = "\033[41m",
        on_green   = "\033[42m",
        on_yellow  = "\033[43m",
        on_blue    = "\033[44m",
        on_magenta = "\033[45m",
        on_cyan    = "\033[46m",
        on_white   = "\033[47m"))
