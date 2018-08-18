import re

#****************************** METAL CLASS*************************************
class MetalBase(object):
    _name = ''
    _metal_per_unit_cost = 0

    @property
    def metal_name(self):
        return self._name

    @metal_name.setter
    def metal_name(self, name):
        self._name = name

    @property
    def metal_cost(self):
        return self._metal_per_unit_cost

    @metal_cost.setter
    def metal_cost(self, cost):
        self._metal_per_unit_cost = cost


class GalaxyMetals(object):
    _metals = {}

    def get_metal(self, name):
        return self._metals.get(name, None)

    def set_metal(self, name, cost):
        metal_base = MetalBase()
        metal_base.metal_name = name
        metal_base.metal_cost = cost
        self._metals[metal_base.metal_name] = metal_base


#*************************** Denominations *************************************

class Roman(object):

    _reference = {'I': 1,
                  'V': 5,
                  'X': 10,
                  'L': 50,
                  'C': 100,
                  'D': 500,
                  'M': 1000
                  }

    _pattern = "^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"

    def roman_to_int(self, roman_string):
        if not bool(re.match(self._pattern, roman_string)):
            return "Not a valid Roman string"
        try:
            inline = lambda x,y: self._reference[x] - self._reference[y]
            value = 0
            index = 0
            length = len(roman_string)
            while index < length:
                if roman_string[index] == 'C':
                    if index+1 < length and \
                                    roman_string[index +1] in ['M', 'D']:
                        value += inline(roman_string[index+1],
                                        roman_string[index])
                        index += 2
                    else:
                        value += self._reference[roman_string[index]]
                        index += 1
                elif roman_string[index] == 'X':
                    if index + 1 < length and \
                                    roman_string[index + 1] in ['C', 'L']:
                        value += inline(roman_string[index+1],
                                        roman_string[index])
                        index += 2
                    else:
                        value += self._reference[roman_string[index]]
                        index += 1
                elif roman_string[index] == 'I':
                    if index + 1 < length and \
                                    roman_string[index + 1] in ['V', 'X']:
                        value += inline(roman_string[index+1],
                                        roman_string[index])
                        index += 2
                    else:
                        value += self._reference[roman_string[index]]
                        index += 1
                else:
                    value += self._reference[roman_string[index]]
                    index +=1
        except Exception as exp:
            return None
        return value

class DenominationBase(object):
    _name = ''
    _roman = ''

    @property
    def denomination_name(self):
        return self._name

    @denomination_name.setter
    def denomination_name(self, name):
        self._name = name

    @property
    def denomination_roman_value(self):
        return self._roman

    @denomination_roman_value.setter
    def denomination_roman_value(self, roman_value):
        self._roman = roman_value

class GalaxyDenominations(Roman):
    _denominations = {}

    def get_denomination(self, name):
        return self._denominations.get(name, None)

    # set denomination for Galaxy
    def set_denomination(self, name, roman):
        if roman not in self._reference:
            return False
        denomination = DenominationBase()
        denomination.denomination_name = name
        denomination.denomination_roman_value = roman
        self._denominations[denomination.denomination_name] = denomination
        return True

    def galaxy_to_roman(self, galaxy_string):
        try:
            roman_string = [
                self.get_denomination(galaxy_denoms).denomination_roman_value
                for galaxy_denoms in galaxy_string.split()]
        except Exception as exp:
            return False
        return ''.join(roman_string)

    def roman_to_int(self, roman_string):
        return super(GalaxyDenominations, self).roman_to_int(roman_string)

#*********************** Transaction Class *************************************

class GalaxyTransactions(object):
    _galaxy_metal_obj = ''
    _galaxy_denom_obj = ''

    def __init__(self):
        self.galaxy_metal_obj = GalaxyMetals()
        self.galaxy_denomination_obj = GalaxyDenominations()

    @property
    def galaxy_metal_obj(self):
        return self._galaxy_metal_obj

    @galaxy_metal_obj.setter
    def galaxy_metal_obj(self, galaxy_metal_obj):
        self._galaxy_metal_obj = galaxy_metal_obj

    @property
    def galaxy_denomination_obj(self):
        return self._galaxy_denom_obj

    @galaxy_denomination_obj.setter
    def galaxy_denomination_obj(self, galaxy_denom_obj):
        self._galaxy_denom_obj = galaxy_denom_obj

    # Case1
    def create_denomination(self, name, roman_value):
        status = self.galaxy_denomination_obj.set_denomination(name,
                                                               roman_value)
        return status

    # Case2
    def create_metal(self, galaxy_denoms, metal_name, credit):
        int_value = self.galaxy_to_int(galaxy_denoms)
        if not int_value:
            return False
        self.galaxy_metal_obj.set_metal(metal_name, int(credit/int_value))
        return True

    # Case3
    def galaxy_to_int(self, galaxy_string):
        romans = self.galaxy_denomination_obj.galaxy_to_roman(galaxy_string)
        if not romans:
            return romans
        value = self.galaxy_denomination_obj.roman_to_int(romans)
        if not value:
            return None
        return value

    # Case4
    def total_metal_cost(self, galaxy_denom, metal_name):
        quantity = self.galaxy_to_int(galaxy_denom)
        metal_obj = self.galaxy_metal_obj.get_metal(metal_name)
        if metal_obj is None:
            return None # error handling if metal obj doesnot exsits
        return quantity * metal_obj.metal_cost


class GalaxyQueryReader(object):
    _galaxy_trnx_obj = ''
    _failed_statement = "I have no idea what you are talking about"

    def __init__(self):
        self.galaxy_trx_obj = GalaxyTransactions()

    @property
    def galaxy_trx_obj(self):
        return self._galaxy_trnx_obj
    
    @galaxy_trx_obj.setter
    def galaxy_trx_obj(self, galaxy_obj):
        self._galaxy_trnx_obj = galaxy_obj

    def output(self, status, statement = None):
        if not status:
            return self._failed_statement
        else:
            if statement:
                status = str(status) if type(status) != str else status
                status = statement + ' is ' +  status
            return status

    def query(self, query_string):
        if len(query_string.split(" "))==3:
            #Case1 Create Denomination object and assign value
            # ex glob is I
            name, roman_value = query_string.split(" is ")
            status = self.galaxy_trx_obj.create_denomination(name, roman_value)
            if not status:
                print(self.output(False))

        elif re.search("(is [0-9]+ Credits)$", query_string):
            #Case2 Metal Value
            # ex glob glob Silver is 34 Credits
            # to pass glob glob = Quantity, Metal name, Credits to calc cost per unit
            query = query_string.split(' ')
            galaxy_denoms = ' '.join(query[:-4])
            metal_name = query[-4]
            credit = int(query[-2])
            status = self.galaxy_trx_obj.create_metal(galaxy_denoms, metal_name,
                                                      credit)
            if not status:
                print (self.output(False))

        elif re.match("^(how much is )", query_string):
            #Case3 General Query
            # ex how much is pish tegj glob glob ?
            string = query_string.split("how much is ")[1][:-2]
            value = self.galaxy_trx_obj.galaxy_to_int(string)
            return (self.output(value, statement=string))

        elif re.match("^(how many Credits is)", query_string):
            # Case 4 Metal Cost Query
            # ex how many Credits is glob prok Iron ?
            # split is needed to extract glalaxy denom and metal name
            string = query_string.split("how many Credits is ")[1].split(" ")
            galaxy_denom = ' '.join(string[:-2])
            metal_name = string[-2]
            value = self.galaxy_trx_obj.total_metal_cost(galaxy_denom,
                                                         metal_name)
            return (self.output(value, statement=galaxy_denom + ' ' + metal_name))
        else:
            # case 5 invalid query
            return (self.output(False))



if __name__=="__main__":
    path_to_file = "/root/"
    with open(path_to_file +"/input_file.txt", "r+") as file:
        file_obj = file.read().split("\n")
        galaxy_query_reader = GalaxyQueryReader()
        for line in file_obj:
            result = galaxy_query_reader.query(line)
            if '?'in line:
                print (result)


