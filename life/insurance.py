import numpy as np
from numpy.polynomial import Polynomial
from scipy import integrate
import warnings

class isrc_discrete:
    """
    This is a class to calculate premiums and life expectation for
    the following life insurance products in factional cases:

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

      frac = i / (k * (1 + i)**(1/k) - 1)

      return frac



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
        return premium * B * self.fractionation(i=i, k=frac)

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

class isrc_continuous:
    
    """
    This class must be used to build a set of functions necesssary to calculate
    the whole life insurance and the term life insurance premiumns for the exactly
    moment of death. 
    
    """
    def __init__(self, table):
        self.table = np.array(table)
        self.Survival_from_birth = 'Not fitted yet.'
        self.Survival_from_birth_Coef = 'Not estimated yet.'
 
    def fix_estimation(y_est):
        
        y_est = np.array(y_est)
        fix = (y_est < 0)   
        y_est[fix] = 0

        fix = (y_est > 1)
        y_est[fix] = 1
        
        return y_est
    
    def calc_tpx(self, t, x):
        """
        This is a method which produces a function that returns $Pr(T_0 > x)$, i.e, the probability of person
        aged zero survives beyound the age x given an qx distribution. Another common notation for that probability is $_xp_0$.
        
        Parameters:
        -----------
        t: int
           Argument of tpx.
           
        x: int.
           Age.
           
        Returns:
        --------
        Probability of an aged x to survive until the age x+t years (tpx). float.
        
        """
        px = 1 - self.table
        tpx = np.prod(px[x:x+t])
        return tpx
            
    
    def fit_Survival_from_birth(self, deg):
        """
        Given some pair of point x and y a polynomial function with degree deg is fitted. This is method to create a 
        continuous function for tpx throught polynomial interpolation method. In this case, the values for t lies on the 
        range [0, infinity) and, y values are given by the function calc_tpx, where x=0.
        
        Parameters:
        -----------
               
        deg: int.
           Degree of polynomial function to be fitted.
           
        Returns:
        --------
        
        numpy.poy1d object is build.
        
        
        """
        
        vec_tpx = np.vectorize(lambda t: self.calc_tpx(t, x=0))
        
        t = np.arange(0, len(self.table)+1)
        y = vec_tpx(t=t)
        
        f = np.polyfit(t, y, deg=deg)
        
        fitted = np.poly1d(f)
        
#         if any(fitted(t) > 1):
#             warnings.warn('The function does not return a probabilistic result. Fit survival from birth again and adjust degree.')
        
        self.Survival_from_birth_Coef = Polynomial(f)
        self.Survival_from_birth = fitted 
        
        mse = sum((fitted(t) - y)**2) / len(t)
        print(f" MSE: {np.round(mse, 6)}")
        

    def Survival_from_age(self, age, to):
        """
        Since the ``Survival_from_birth`` function is fitted this function calculates the probability S_0 applied on x.
        
        Parameters:
        -----------
        
        age: int.
             Age.
        
        to: int.
            limit for survival.
            
        Returns:
        --------
        
        The probability of a person aged ``age`` survives until the age ``age+to``. float.
        
        """
        
        if self.Survival_from_birth == 'Not fitted yet.':
            raise Exception('You must need to fit survival from birth first')
            
        if age+to > len(self.table):
            raise Exception('Estimation is out of range. Age + to needs to be lower than len(table).')
        
        prob = self.Survival_from_birth(age+to) / self.Survival_from_birth(age)            
        return prob
    
    def mu_force(self, age):
        
        """
        This function calculates the force of motality at some given age. This function uses the polynomial 
        function fitted on the ``fit()`` method to calculate the force of mortality. 
        
        Parameter:
        ----------
        
        age: int.
             age to be applied on the force of mortality.
             
        Return:
        -------
        
        mu: int
            The force of mortality at given age.
            
        """
        mu = -1/self.Survival_from_birth(age) * self.Survival_from_birth.deriv()(age)
        mu = np.array(mu)
        mu[mu < 0] = 1
        mu[mu > 1] = 1
        return mu 	
    
    def premium(self, age, i, contract=np.infty, B=1):
        """
        This function is used to calculate the premium of life insurace contract. 
        
        Parameters:
        -----------
        age: int.
             Age.
        
        i: float. 
               rate for discount factor
        
        contract: float or int.
                  Time contract. If contract is equal to ``np.infinity`` than premium refers to a wholel life insurance.
        B: float.
           Benefit.
           
        Returns:
        --------
        
        Premium: float.
        
        """
        
        if self.Survival_from_birth == 'Not fitted yet.':
            raise Exception('Continuous survival function is not fitted yet.')
            
        if self.mu_force == 'Not fitted yet.':
            raise Exception('Mortality force function is not fitted yet.')
                                
        delta = np.log(1+i)
        f = lambda time: np.exp(-time*delta) * self.mu_force(age+time) * ( self.Survival_from_birth(time+age) if time+age < len(self.table) else 1)
        
        
        omega = len(self.table) - age
        if ( (contract > omega) | ((contract+age) > omega) ):
            contract = omega
            
#         testing = [integrate.quad(f, a=0, b=tmp)[0] * B for tmp in np.arange(omega+1)]
#         testing = np.array(testing)
        
#         check = ( (testing < 0) | (testing > 1) )
#         if any(check):
#             warnings.warn("Maybe the premium is not valid. Try to fit a new survival function with a higher degree.")
        
        
        premium = integrate.quad(f, a=0, b=contract)[0] * B
        return premium
