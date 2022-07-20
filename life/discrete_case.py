import numpy as np

"""
IMPORTANT: All of these classes were bild to calculate premiums for anual case.
"""


class life_insurance:
    """
    This is a class to calculate premiums and life expectation for
    the following life insurance products:

    - The whole life insurance;
    - The term life insurance;
    - The deffered whole life insurance;
    - The deffered term life insurance;
    - Pure Endowment;
    - Endowment.
    """

    def __init__(self, table):

        self.table = np.array(table)

    def fractionation(self, i, k=1):

      return (i / (k * ((1+i)**(1/k) - 1)))

    def life_expectation(self, age):
        """
        This function calculates the life expectation at age x according to
        a life table.

        Parameters:
        -----------

        age: int.
             Age.

        Return:
        -------

        Life expectation at age x: float.
        """

        qx = self.table[age:]  # Cutting down probability distribution
        px = list(1 - qx[:-1])  # Calculating 1_p_x
        px.insert(0, 1)  # setting 0_p_x = 1
        px = np.array(px)  # tranforming into array
        t = np.arange(1, len(qx)+1)  # time range

        ex = sum(t * np.cumprod(px) * qx)
        return np.round(ex)

    def Ax(self, i, age, B=1, frac=1):
        """
        This function calculates the premium of a whole life insurance for
        the annual case.

        Parameters:
        -----------

        i: float.
           Nominal rate.

        age: int.
               Age.
        B: float.
           Benefit.

        Returns:
        --------

        Premium.

        """

        qx = self.table[age:]  # Cutting down probability distribution
        px = list(1 - qx[:-1])  # Calculating 1_p_x
        px.insert(0, 1)  # setting 0_p_x = 1
        px = np.array(px)  # tranforming into array
        v = (1 + i) ** -1  # Discount factor
        t = np.arange(0, len(qx))  # time range

        premium = sum(v ** (t + 1) * np.cumprod(px) * qx)
        return premium * B * self.fractionation(i=i, k=frac)

    def Ax_tmp(self, i, age, tmp, B=1, frac=1):
        """
        This function calculates the premium of a term life insurance for
        the annual case.

        Parameters:
        -----------

        i: float.
           Nominal rate.

        age: int.
               Age.

        tmp: int.
             Number of year of contract.

        B: float.
           Benefit.

        Returns:
        --------

        Premium.

        """

        N = age + tmp
        qx = self.table[age:N]  # Cutting down probability distribution
        px = list(1 - qx[:-1])  # Calculating 1_p_x
        px.insert(0, 1)  # setting 0_p_x = 1
        px = np.array(px)  # tranforming into array
        v = (1 + i) ** -1  # Discount factor
        t = np.arange(0, len(qx))  # time range
        premium = sum(v ** (t + 1) * np.cumprod(px) * qx)
        return premium * B  * self.fractionation(i=i, k=frac)

    def Pure_Endow(self, i, age, tmp, B=1, frac=1):
        """
        This function calculates a premium for a pure endowment life insurance.

        Parameters:
        -----------

        i: float.
           Nominal rate.

        age: int.
               Age.

        tmp: int.
             Number of year of contract.

        B: float.
           Benefit.

        Returns:
        --------

        Premium.

        """

        v = (1 + i) ** -tmp
        M = age + tmp
        qx = self.table[age:M]  # Cutting down probability distribution
        px = list(1 - qx)  # Calculating 1_p_x
        px.insert(0, 1)  # setting 0_p_x = 1
        premium = v * np.prod(px)

        return premium * B * self.fractionation(i=i, k=frac)

    def def_Ax(self, i, age, n_def, B=1, frac=1):
        """
        This function calculates the pure premium for a deffered whole life insurance.

        Parameters:
        -----------

        i: float.
           Nominal rate.

        age: int.
               Age.

        n_def: int.
               Number of year of deffering.

        B: float.
           Benefit.

        Returns:
        --------

        Premium.

        """
        dotal = self.Pure_Endow(i=i, age=age, tmp=n_def)
        Ax = self.Ax(i=i, age=age + n_def)

        premium = dotal * Ax

        return premium * B * self.fractionation(i=i, k=frac)

    def def_Ax_tmp(self, i, age, tmp, n_def, B=1, frac=1):
        """
        This function calculates the pure premium of a deffered term life insurance.

        Parameters:
        -----------

        i: float.
           Nominal rate.

        age: int.
               Age.

        tmp: int.
             Number of year of contract.

        n_def: int.
               Number of year of deffering.

        B: float.
           Benefit.


        Returns:
        --------

        Premium.
        """

        dotal = self.Pure_Endow(i=i, age=age, tmp=n_def)
        Ax_temp = self.Ax_tmp(i=i, age=age + n_def, tmp=tmp)

        premium = dotal * Ax_temp

        return premium * B * self.fractionation(i=i, k=frac)

    def Endowment(self, i, age, tmp, B=1, frac=1):
        """
        This function calculates a premium for an endowment life insurance.

        Parameters:
        -----------

        i: float.
           Nominal rate.

        age: int.
               Age.

        tmp: int.
             Number of year of contract.

        B: float.
           Benefit.

        Returns:
        --------

        Premium.

        """

        dotal = self.Pure_Endow(i=i, age=age, tmp=tmp)
        Ax_temp = self.Ax_tmp(i=i, age=age, tmp=tmp)

        premium = B * (dotal + Ax_temp) * self.fractionation(i=i, k=frac)

        return premium
    
    def var(PROD, **params):
        """
        This function calculates the variance of a premium of a whole life insurance 
        for the annual case.

        Parameters:
        -----------

        i: float.
           Nominal rate.

        age: int.
               age

        B: float.
            Benefit

         Returns:
         --------

         Premium.

         """
        i2 = ((i + 1) ** 2) - 1
        return np.abs((PROD(i=i2,**params)-(PROD(**params) ** 2)))


class life_annuity:
    """
    This is a class to calculate premiums for
    the following life annuity products:

    - The whole life annuity;
    - The term life annuity;
    - The deffered whole life annuity;
    - The deffered term life annuity.
    """

    def __init__(self, table):
        self.table = np.array(table)

    def ax(self, i, age, B=1, due=False):

        """
        This function calculates the premium of a whole life annuitiy.

        Parameters:
        -----------
        i: float.
           Nominal rate.

        age: int.
             Age.

        B: float.
           Benefit.

        due: bool.
             If true the premium refers to an annuity which benefit is payd immediatly.

        Returns:
        --------

        Premium.
        """

        qx = self.table[age:]  # Cutting down probability distribution
        v = (1 + i) ** -1

        t = np.arange(1, len(qx) + 1)
        qx = self.table[age:]  # Cutting down probability distribution
        px = list(1 - qx)  # Calculating 1_p_x

        premium = sum(v**t * np.cumprod(px))

        if due:
            premium = sum(v**t * np.cumprod(px)) + 1

        return premium * B

    def ax_tmp(self, i, age, tmp, B=1, due=False):

        """
        This function calculates the premium of a term life annuitiy.

        Parameters:
        -----------
        i: float.
           Nominal rate.

        age: int.
              Age.

        tmp: int.
              Number of year of contract.

        B: float.
           Benefit.

        due: bool.
              If true the premium refers to an annuity which benefit is payd immediatly.

        Returns:
        --------

        Premium.
        """

        N = age + tmp
        qx = self.table[age:N]  # Cutting down probability distribution
        px = list(1 - qx)
        t = np.arange(1, tmp + 1)
        v = (1 + i) ** -1

        if due:
            px = list(1 - qx[:-1])  # Calculating 1_p_x
            px.insert(0, 1)  # setting 0_p_x = 1
            t = t - 1

        premium = sum(v**t * np.cumprod(px))

        return premium * B

    def def_ax(self, i, age, n_def, B=1, due=False):
        """
        This function calculates the premium of a deffered life annuitiy.

        Parameters:
        -----------
        i: float.
           Nominal rate.

        age: int.
             Age.

        n_def: int.
               Number of year of deffering.

        B: float.
           Benefit.

        due: bool.
             If true the premium refers to an annuity which benefit is payd immediatly.

        Returns:
        --------

        Premium.
        """

        diff = life_insurance(table=self.table).Pure_Endow(i=i, age=age, tmp=n_def)
        ax = self.ax(i=i, age=age + n_def, due=due)

        return diff * ax * B

    def def_ax_tmp(self, i, age, n_def, tmp, B=1, due=False):
        """
        This function calculates the premium of a deffered term life annuity.

        Parameters:
        -----------
        i: float.
           Nominal rate.

        age: int.
             Age.

        n_def: int.
               Number of year of deffering.

        tmp: int.
             Number of years of contract.

        B: float.
           Benefit.

        due: bool.
             If true the premium refers to an annuity which benefit is payd immediatly.

        Returns:
        --------

        Premium.
        """

        diff = life_insurance(table=self.table).Pure_Endow(i=i, age=age, tmp=n_def)
        ax_temp = self.ax_tmp(i, age=age + n_def, tmp=tmp, due=due)

        return diff * ax_temp * B
