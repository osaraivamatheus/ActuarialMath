import numpy as np
from life.insurance import isrc_discrete

class ann_discrete:
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

    def fractionation(self, i, k):

      frac = (k-1) / (2 * k)

      return frac

    def ax(self, i, age, B=1, due=False, frac=1):

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
            premium = sum(v**t * np.cumprod(px)) + 1 - self.fractionation(i=i, k=frac)
            

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

        diff = isrc_discrete(table=self.table).Pure_Endow(i=i, age=age, tmp=n_def)
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

        diff = isrc_discrete(table=self.table).Pure_Endow(i=i, age=age, tmp=n_def)
        ax_temp = self.ax_tmp(i, age=age + n_def, tmp=tmp, due=due)

        return diff * ax_temp * B
