from Boardgamebox.Board import Board

board = Board(7, None)

board.state.resultado_misiones = ["Exsito", "Esxito", "Exsito", "sxito", "Esxito"]
class Player(object):
    def __init__(self, name, uid, veternano):
        self.name = name
        self.uid = uid
        self.rol = None
        self.afiliacion = None
        # Indica si el jugador tiene el MAGIC TOKEN
        self.has_magic_token = False
        self.esta_muerto = False        
        self.was_investigated = False        
        self.es_el_investigador = False
        self.fue_el_investigador = False
        self.veteran = veternano 

playerlist = [
    Player("Juan", 1, True),
    Player("Pedro", 2, True),
    Player("Maria", 3, True),
    Player("Juan", 4, True),
    Player("Pedro", 5, True),
    Player("Maria", 6, True),
    Player("Juan", 7, True),
]

print(board.print_board(playerlist))



# from html2image import Html2Image

# hti = Html2Image(custom_flags=['--no-sandbox'])
# hti.browser_executable = "/usr/bin/google-chrome"
# html = """<h1> An interesting title </h1> This page will be red"""
# css = "body {background: red;}"

# file = hti.screenshot(html_str=html, css_str=css, save_as='red_page.png')

# class Player(object):
#     def __init__(self, name, uid, veternano):
#         self.name = name
#         self.uid = uid
#         self.rol = None
#         self.afiliacion = None
#         # Indica si el jugador tiene el MAGIC TOKEN
#         self.has_magic_token = False
#         self.esta_muerto = False        
#         self.was_investigated = False        
#         self.es_el_investigador = False
#         self.fue_el_investigador = False
#         self.veteran = veternano 

# playerlist = {
#     1 : Player("Juan", 1, True),
#     2 : Player("Pedro", 2, True),
#     3 : Player("Maria", 3, True),
# }

# print(playerlist)

# no_veternaros =   [player[1] for player in playerlist.items() if player[1].veteran == False]

# print(no_veternaros)