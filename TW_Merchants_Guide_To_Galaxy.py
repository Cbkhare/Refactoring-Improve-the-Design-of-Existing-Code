import re

#****************************** Metal Class*************************************


class MetalBase(object):
    """
    This is the base class for a metal. It defines the attribute a metal object.
    """
    _name = ''
    _metal_per_unit_cost = 0

    @property
    def metal_name(self):
        """
        This method gets the metal name attribute of metal object
        :return: metal name (String)
        """
        return self._name

    @metal_name.setter
    def metal_name(self, name):
        """
        This method sets the metal name attribute of metal object
        :param name: String
        :return: None
        """
        self._name = name

    @property
    def metal_cost(self):
        """
        This method gets the metal cost attribute of metal object
        :return: metal per unit cost (Int)
        """
        return self._metal_per_unit_cost

    @metal_cost.setter
    def metal_cost(self, cost):
        """
        This method sets the metal cost attribute of metal object
        :param cost: Int
        :return: None
        """
        self._metal_per_unit_cost = cost


class GalaxyMetals(object):
    """
    This is the wrapper class over base metal class. The job of this class is to
    create metal object and assign metal attribute to the metal object. It also
    hold the object for each metal with reference to its name.
    """
    _metals = {}

    def get_metal(self, name):
        """
        This method gets the object of the metal with reference to its name
        :param name: String
        :return: metal object
        """
        return self._metals.get(name, None)

    def set_metal(self, name, cost):
        """
        This method creates the metal object and sets the following attribute
        :param name: String
        :param cost: Int
        :return: None
        """
        metal_base = MetalBase()
        metal_base.metal_name = name
        metal_base.metal_cost = cost
        self._metals[metal_base.metal_name] = metal_base


#********************* Denominations Class *************************************


class Roman(object):
    '''
    This is the Class to hold Roman values and perform operation on them. I have
    added the method of roman to int conversion in this class because of its
    association with roman reference and the logic to convert roman value to
    integer values.
    '''
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
        """
        This method validates and converts roman value to integer values with
        below logic
        :param roman_string: String
        :return: Value Int if successful else None
        """
        if not bool(re.match(self._pattern, roman_string)):
            return "Not a valid Roman string"
        try:
            # Inline function to calculate value for "index + 1" and "index"
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
    """
    This class is the base class to create denomination object
    """
    _name = ''
    _roman = ''

    @property
    def denomination_name(self):
        """
        This method gets the denominations name for the denomination object
        :return: denomination name
        """
        return self._name

    @denomination_name.setter
    def denomination_name(self, name):
        """
        This method sets the denominations name for the denomination object
        :param name: String
        :return: None
        """
        self._name = name

    @property
    def denomination_roman_value(self):
        """
        This method gets the denomination roman value for the denomination
        object
        :return: roman value of the denomination
        """
        return self._roman

    @denomination_roman_value.setter
    def denomination_roman_value(self, roman_value):
        """
        This method sets the denominations roman value for the denomination
        object
        :param roman_value: String
        :return: None
        """
        self._roman = roman_value


class GalaxyDenominations(Roman):
    """
    This class is a wrapper over the Denomination base class. Its job is to
    create denomination object and assign attribute to the denominations object.
    It also holds the object for each denomination with reference to its name.

    The class also inherits Roman class to
    1) verify roman values while creating denomination object and assigning its
    attributes
    2) convert galaxy denominations to roman string i.e ex glob prok -> IV
    3) convert roman to int.
    """
    _denominations = {}

    def get_denomination(self, name):
        """
        This method get the denomination object with reference to its name
        :param name: name of the denomination
        :return: Denomination object if found else None
        """
        return self._denominations.get(name, None)

    def set_denomination(self, name, roman):
        """
        This method create and sets the attribute for denomination object.
        :param name: String
        :param roman: String
        :return: False if roman
        """
        if roman not in self._reference:
            return False
        denomination = DenominationBase()
        denomination.denomination_name = name
        denomination.denomination_roman_value = roman
        self._denominations[denomination.denomination_name] = denomination
        return True

    def galaxy_to_roman(self, galaxy_string):
        """
        This method translates galaxy denominations to roman string
        :param galaxy_string: String
        :return: roman string if successful and None on exception
        """
        try:
            roman_string = [
                self.get_denomination(galaxy_denoms).denomination_roman_value
                for galaxy_denoms in galaxy_string.split()]
        except Exception as exp:
            return None
        return ''.join(roman_string)

    def roman_to_int(self, roman_string):
        """
        This method translates roman string to integer. It calls parent method
        for the logic of conversion.
        :param roman_string: String
        :return: Translated value if successful else None
        """
        return super(GalaxyDenominations, self).roman_to_int(roman_string)

#*********************** Transaction Class *************************************

class GalaxyTransactions(object):
    """
    This class does the transaction on metals and denominations. li
    """
    _galaxy_metal_obj = ''
    _galaxy_denom_obj = ''

    def __init__(self):
        self.galaxy_metal_obj = GalaxyMetals()
        self.galaxy_denomination_obj = GalaxyDenominations()

    @property
    def galaxy_metal_obj(self):
        """
        This method gets the GalaxyMetal class object
        :return: Object
        """
        return self._galaxy_metal_obj

    @galaxy_metal_obj.setter
    def galaxy_metal_obj(self, galaxy_metal_obj):
        """
        This method sets the GalaxyMetal class object
        :param galaxy_metal_obj: Object
        :return: None
        """
        self._galaxy_metal_obj = galaxy_metal_obj

    @property
    def galaxy_denomination_obj(self):
        """
        This method get the Denomination class object
        :return: Object
        """
        return self._galaxy_denom_obj

    @galaxy_denomination_obj.setter
    def galaxy_denomination_obj(self, galaxy_denom_obj):
        """
        This method sets the Denomination class object
        :param galaxy_denom_obj: Object
        :return: None
        """
        self._galaxy_denom_obj = galaxy_denom_obj

    # Case1
    def create_denomination(self, name, roman_value):
        """
        This method creates the denomination. 
        :param name: Denomination Name String
        :param roman_value: Roman Value String
        :return: True if successful else False 
        """
        status = self.galaxy_denomination_obj.set_denomination(name,
                                                               roman_value)
        return status

    # Case2
    def create_metal(self, galaxy_denoms, metal_name, credit):
        """
        This method create the metal object and its attributes.
        :param galaxy_denoms: String
        :param metal_name: String
        :param credit: Integer
        :return: True if successful else False
        """
        int_value = self.galaxy_to_int(galaxy_denoms)
        if not int_value:
            return False
        self.galaxy_metal_obj.set_metal(metal_name, int(credit/int_value))
        return True

    # Case3
    def galaxy_to_int(self, galaxy_string):
        """
        This method hold the steps to convet galaxy denominations to Integer
        :param galaxy_string: String
        :return: Value Int if successful else None
        """
        romans = self.galaxy_denomination_obj.galaxy_to_roman(galaxy_string)
        if not romans:
            return romans
        value = self.galaxy_denomination_obj.roman_to_int(romans)
        if not value:
            return None
        return value

    # Case4
    def total_metal_cost(self, galaxy_denom, metal_name):
        """
        This method calculates the Metal worth for the given galaxy 
        denominations.
        :param galaxy_denom: String
        :param metal_name: String
        :return: Metal cost if successful else None
        """
        quantity = self.galaxy_to_int(galaxy_denom)
        metal_obj = self.galaxy_metal_obj.get_metal(metal_name)
        if metal_obj is None:
            return None # error handling if metal obj doesnot exsits
        return quantity * metal_obj.metal_cost


#**************************** Query Class **************************************

class GalaxyQueryReader(object):
    """
    This class reads the query and call the appropriate method in 
    GalaxyTransaction class
    """
    _galaxy_trnx_obj = ''
    _failed_statement = "I have no idea what you are talking about"

    def __init__(self):
        self.galaxy_trx_obj = GalaxyTransactions()

    @property
    def galaxy_trx_obj(self):
        """
        This method gets the GalaxyTransaction Object
        :return: Object
        """
        return self._galaxy_trnx_obj
    
    @galaxy_trx_obj.setter
    def galaxy_trx_obj(self, galaxy_obj):
        """
        This method sets the GalaxyTransaction Object
        :param galaxy_obj: Object
        :return: None
        """
        self._galaxy_trnx_obj = galaxy_obj

    def output(self, output, statement = None):
        """
        This methos is wrapper over the output of respective methods
        :param output: output of the method (String/Int/Boolean/None)
        :param statement: String
        :return: String
        """
        if not output:
            return self._failed_statement
        else:
            if statement:
                output = str(output) if type(output) != str else output
                output = statement + ' is ' + output
            return output

    def query(self, query_string):
        """
        This method reads the query and calls the appropriate method from the 
        transaction class. In this class there i have usd regular expression to 
        match the statement of the quesry and call the required method.  
        :param query_string: String 
        :return: 
        """
        if len(query_string.split(" "))==3:
            # Case1 Create Denomination object and assign value
            # ex glob is I
            name, roman_value = query_string.split(" is ")
            status = self.galaxy_trx_obj.create_denomination(name, roman_value)
            if not status:
                print(self.output(False))

        elif re.search("(is [0-9]+ Credits)$", query_string):
            # Case2 Metal Value
            # ex glob glob Silver is 34 Credits
            # to pass glob glob = Quantity, Metal name, 
            # Credits to calc cost per unit
            query = query_string.split(' ')
            galaxy_denoms = ' '.join(query[:-4])
            metal_name = query[-4]
            credit = int(query[-2])
            status = self.galaxy_trx_obj.create_metal(galaxy_denoms, metal_name,
                                                      credit)
            if not status:
                print (self.output(False))

        elif re.match("^(how much is )", query_string):
            # Case3 General Query
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
    # Please add the path to input file in path_to_file variable
    path_to_file = "/root/"

    with open(path_to_file + "/input_file.txt", "r+") as file:
        file_obj = file.read().split("\n")
        galaxy_query_reader = GalaxyQueryReader()

        for line in file_obj:
            result = galaxy_query_reader.query(line)
            if '?'in line:
                # if the query is to get the ouput of the query
                print (result)

'''
Test Results

.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK

Process finished with exit code 0
'''