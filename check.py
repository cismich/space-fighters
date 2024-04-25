
#nevim jestli tohle je ten nejlepsi jak zjistit jestli ma nekdo vsechno nainstalovane ale funguje to 
def init() -> int:
    try:
        import curses
    except:
        return 1
    return 0
