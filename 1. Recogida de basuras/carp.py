# ================================================
# Main
# ================================================

class CARP:

    aristas = {}
    
    def main(self, data):
        self.aristas = data['lista_aristas_req']
        return self.aristas