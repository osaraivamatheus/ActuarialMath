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
        self.continuous_xp0_fitted = 'Not fitted yet.'
        self.Prob_xp0 = 'Not fitted yet.'
        self.Ax_integral = 'Not defined yet.'
    
    def build_xp0(self, age):
        """
        This is a method which produces a function that returns $Pr(T_0 > x)$, i.e, the probability of person
        aged zero survives beyound the age x given an qx distribution. Another common notation for that probability is $_xp_0$.
        
                     
        Returns:
        --------
        lambda funtion.
        
        """
        self.age = age
        px = 1 - self.qx
        tpx = (lambda t: np.prod(px[:t]))
        self.Prob_xp0 = tpx
    
    def fit(self, x, y, deg):
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
        x = np.array(x)
        y = np.array(y)

        f = np.polyfit(x, y, deg=deg)
        print(Polynomial(f))
        self.continuous_xp0_fitted = np.poly1d(f)
        
        return self
    
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
        
        if self.continuous_xp0_fitted == 'Not fitted yet.':
            raise Exception('Continuous survival function is not fitted yet.')
        
        mu = -1/self.continuous_xp0_fitted(age) * self.continuous_xp0_fitted.deriv()(age)
        
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
        
        if self.continuous_xp0_fitted == 'Not fitted yet.':
            raise Exception('Continuous survival function is not fitted yet.')
            
        if self.mu_force == 'Not fitted yet.':
            raise Exception('Mortality force function is not fitted yet.')
        
        f = lambda time: self.mu_force(time)*np.exp(-time*delta)*self.continuous_xp0_fitted(time)
        
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