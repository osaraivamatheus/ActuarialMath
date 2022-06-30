import numpy as np
from numpy.polynomial import Polynomial
from scipy import integrate

import warnings
import matplotlib.pyplot as plt

def fix_estimation(y_est):
        
    y_est = np.array(y_est)
    fix = (y_est < 0)   
    y_est[fix] = 0

    fix = (y_est > 1)
    y_est[fix] = 1
    
    return y_est

class life_insurance:
    
    """
    This class must be used to build a set of functions necesssary to calculate
    the whole life insurance and the term life insurance. 
    
    """
    def __init__(self, table):
        self.table = np.array(table)
        self.Survival_from_birth = 'Not fitted yet.'
        self.Survival_from_birth_Coef = 'Not estimated yet.'
 
    
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
        if contract > len(self.table):
            contract = omega
            
        testing = [integrate.quad(f, a=0, b=tmp)[0] * B for tmp in np.arange(omega+1)]
        testing = np.array(testing)
        
        check = ( (testing < 0) | (testing > 1) )
        if any(check):
            warnings.warn("Maybe the premium is not valid. Try to fit a new survival function with a higher degree.")
        
        
        return integrate.quad(f, a=0, b=contract)[0] * B