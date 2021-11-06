class substance:
    def get_name(self):
        return self.name

    def get_molecular_mass(self):
        return self.molecular_mass

class molecular_hydrogen(substance):
    def __init__(self):
        self.name = "molecular hydrogen"
        self.molecular_mass = 2.01588/(1000 * 6.02214076*(10**23)) #kg per molecule

class proton(substance):
    def __init__(self):
        self.name = "proton"
        self.molecular_mass = (2.01588 * 0.5)/(1000 * 6.02214076*(10**23)) #kg per molecule

class helium(substance):
    def __init__(self):
        self.name = "helium"
        self.molecular_mass = 4.002602/(1000 * 6.02214076*(10**23)) #kg per molecule

class helium3(substance):
    def __init__(self):
        self.name = "helium3"
        self.molecular_mass = 3.0160293/(1000 * 6.02214076*(10**23)) #kg per molecule
