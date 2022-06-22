class Player(object):
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid
        self.rol = None
        self.afiliacion = None
        # Indica si el jugador tiene el MAGIC TOKEN
        self.has_magic_token = False
        self.esta_muerto = False        
        self.was_investigated = False        
        self.was_investigator = False
        self.fue_el_investigador = False
        self.veteran = False      
