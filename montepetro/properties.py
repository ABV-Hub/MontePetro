import numpy as np
from montepetro.generators import RandomGenerator


class Property(object):
    def __init__(self,  name=None, desc=None):
        self.name = name
        self.desc = desc
        self.values = None

    def generate_values(self):
        pass

    def update_seed(self, *args, **kwargs):
        pass


class RandomProperty(Property):
    def __init__(self, seed_generator, n=None, random_number_function=None, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.seed = None
        self.update_seed(seed_generator)
        self.random_generator = RandomGenerator(self.seed, n, random_number_function)
        self.mean = None

    def update_seed(self, seed_generator):
        self.seed = seed_generator.request_seed()

    def generate_values(self, *args, **kwargs):
        self.values = self.random_generator.get_n_random_numbers(*args, **kwargs)

    def calculate_property_statistics(self):
        self.mean = np.mean(self.values)


class NumericalProperty(Property):
    def __init__(self, numerical_function=None, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.numerical_function = numerical_function
        self.mean = None

    def generate_values(self, *args, **kwargs):
        self.values = self.numerical_function(*args, **kwargs)

    def calculate_property_statistics(self):
        self.mean = np.mean(self.values)


class OriginalOilInPlace(NumericalProperty):
    def __init__(self):
        NumericalProperty.__init__(self, name="OOIP",
                                   desc="Original Oil in Place Property",
                                   numerical_function=self.original_oil_in_place())
        self.numerical_function = self.original_oil_in_place

    def original_oil_in_place(self,**kwargs):
        area = kwargs['regions'].properties['area']
        phi = kwargs['regions'].properties['porosity']
        sw = kwargs['regions'].properties['sw']
        result = []
        for i in range(len(area)):
            result.append(area[i]*phi[i]*(1-sw[i]))
        return np.array(result)