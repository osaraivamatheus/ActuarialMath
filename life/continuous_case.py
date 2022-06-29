import numpy as np
from numpy.polynomial import Polynomial
from scipy import integrate

class life_insurace:
    
    """
    This class must be used to build a set of functions necesssary to calculate
    the whole life insurance and the term life insurance. 
    
    """
    def __init__(self, qx):
        self.qx = np.array(qx)
        self.age = None
        self.Survival_from_birth = 'Not fitted yet.'
        self.Survival_from_birth_Coef = 'Not estimated yet.' 
        self.Prob_tpx = 'Not fitted yet.'
        self.Ax_integral = 'Not defined yet.'
    
    def calc_tpx(self, t, x):
        """
        This is a method which produces a function that returns $Pr(T_0 > x)$, i.e, the probability of person
        aged zero survives beyound the age x given an qx distribution. Another common notation for that probability is $_xp_0$.
        
                     
        Returns:
        --------
        lambda funtion.
        
        """
        px = 1 - self.qx
        tpx = np.prod(px[x:x+t])
        return tpx
            
    
    def fit_Survival_from_birth(self, deg):
        """
        Given some pair of point x and y a polynomial function with degree deg is fitted. This is method to create a 
        continuous function for tpx throught polynomial interpolation method.
        
        Parameters:
        -----------
        x: list or array.
           X data points (i.e the ages of a life table)
        y: list or array.
           y data points (i.e the tpx af a life table)
        
        deg: int.
           Degree of a the polynomial to be fitted.
           
        Returns:
        --------
        
        numpy.poy1d object is build.
        
        
        """
        
        vec_tpx = np.vectorize(lambda t: self.calc_tpx(t, x=0))
        
        t = np.arange(0, len(self.qx)+1)
        y = vec_tpx(t=t)
        
        f = np.polyfit(t, y, deg=deg)
        
        fitted = np.poly1d(f)
        
        if any(fitted(t) > 1):
            raise Exception('The function does not return a probabilistic result. Fit survival from birth again (increase degree)')
        
        self.Survival_from_birth_Coef = Polynomial(f)
        self.Survival_from_birth = fitted 
        
        
    
    def Survival_from_age(self, age, to):
        
        if self.Survival_from_birth == 'Not fitted yet.':
            raise Exception('You must need to fit survival from birth first')
            
        Sxt = self.Survival_from_birth(age+to) / self.Survival_from_birth(age)
        
#         if (Sxt > 1):
#             raise Exception('The function does not return a probabilistic result. Fit survival from birth again (increase degree)')
        return Sxt
    
    def mu_force(self, age, deg=5):
        
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
        x = np.arange(0, len(self.qx))
        
        mu = -1/self.Survival_from_birth(age) * self.Survival_from_birth.deriv()(age)
        
        return mu
    
    def define_integral(self, delta):
        """
        This method defines a continuos function to be integrated. 
        
        Parameters:
        -----------
        
        delta: float.
               rate of discount factor.
               
        Returns:
        --------
        
        lambda function.
        
        """
        
        if self.Survival_from_birth == 'Not fitted yet.':
            raise Exception('Continuous survival function is not fitted yet.')
            
        if self.mu_force == 'Not fitted yet.':
            raise Exception('Mortality force function is not fitted yet.')
        
        f = lambda time: self.mu_force(time)*np.exp(-time*delta)*self.Survival_from_birth(time)
        
        self.Ax_integral = f
    
    def premium(self, contract, B=1):
        """
        This function is used to calculate the premium of life insurace contract. The premium is the result of 
        the integral defined on the ``define_integral()`` method.
        
        Parameters:
        -----------
        contract: float or int.
                  Time contract. If contract is equal to ``np.infinity`` than premium refers to a wholel life insurance.
        B: float.
           Benefit.
           
        Returns:
        --------
        
        Premium: float.
        
        """
        
        if self.Ax_integral == 'Not defined yet.':
            raise Exception('Integral is not defined yet.')
            
        to_integrate = self.Ax_integral
        
        return integrate.quad(to_integrate, a=0, b=contract)[0] * B