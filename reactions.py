from substance import *

class reaction:
    def get_name(self):
        return self.name
    
    def get_type(self):
        return type(self)

    def get_num_of_steps(self):
        return len(self.steps)

class proton_proton_chain(reaction):
    def __init__(self):
        self.name = "proton-proton chain"
        self.step1 = (1.442 + 5.493) * 1.6021773E-13 # converting MeV to J
        self.step2 = (12.859/2) * 1.6021773E-13 # divide by two because one chain
                                                # only produces half of the requirements
                                                # for step 2
        self.steps = [self.step1, self.step2]

    def get_energy_output(self, temp):
        # Below 10 MK, the p–p chain does not produce much 4He. [citation needed]
        if temp < 10 * 1000000:
            return self.step1
        else:
            return self.step1 + self.step2

    def get_material_output(self, temp):
        # Below 10 MK, the p–p chain does not produce much 4He. [citation needed]
        if temp < 10 * 1000000:
            out1 = helium3()
            return [[out1], 1]
        else:
            out1 = helium()
            out2 = proton()
            return [[out1, out2], 0.5]
