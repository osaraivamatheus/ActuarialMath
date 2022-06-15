import numpy as np

class seguros:
    def __init__(self, tabua):

        self.tabua = np.array(tabua)

    def Ax(self, i, idade, B=1):
        """
        Esta função calcula o prêmio puro único de um seguro de vida vitalício.

        Parameters:
        -----------

        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               Idade do segurado.
        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio puro único.

        """

        qx = self.tabua[idade:]  # Cutting down probability distribution
        px = list(1 - qx[:-1])  # Calculating 1_p_x
        px.insert(0, 1)  # setting 0_p_x = 1
        px = np.array(px)  # tranforming into array
        v = (1 + i) ** -1  # Discount factor
        t = np.arange(0, len(qx))  # time range

        premio = sum(v ** (t + 1) * np.cumprod(px) * qx)
        return premio * B

    def Ax_temp(self, i, idade, cobertura, B=1):
        """
        Esta função calcula o prêmio puro único de um seguro de vida temporário por n anos.

        Parameters:
        -----------

        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               Idade do segurado.
        cobertura: int.
           Tempo de cobertura.
        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio puro único.

        """

        N = idade + cobertura
        qx = self.tabua[idade:N]  # Cutting down probability distribution
        px = list(1 - qx[:-1])  # Calculating 1_p_x
        px.insert(0, 1)  # setting 0_p_x = 1
        px = np.array(px)  # tranforming into array
        v = (1 + i) ** -1  # Discount factor
        t = np.arange(0, len(qx))  # time range
        premio = sum(v ** (t + 1) * np.cumprod(px) * qx)
        return premio * B

    def Dotal(self, i, idade, cobertura, B=1):
        """
        Esta função calcula o prêmio puro único de um seguro de vida dotal por m anos.

        Parameters:
        -----------

        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               Idade do segurado.
        cobertra: int.
                     Tempo de cobertura.
        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio puro único.

        """

        v = (1 + i) ** -cobertura
        M = idade + cobertura
        qx = self.tabua[idade:M]  # Cutting down probability distribution
        px = list(1 - qx)  # Calculating 1_p_x
        px.insert(0, 1)  # setting 0_p_x = 1
        premio = v * np.prod(px)

        return premio * B

    def Ax_dif(self, i, idade, diferimento, B=1):
        """
        Esta função calcula o prêmio puro único de um seguro de vida vitalício com diferimento.

        Parameters:
        -----------

        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               Idade do segurado.
        diferimento: int.
           Tempo de cobertura.
        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio puro único.

        """
        dotal = self.Dotal(i=i, idade=idade, cobertura=diferimento)
        Ax = self.Ax(i=i, idade=idade + diferimento)

        premio = dotal * Ax

        return premio * B

    def Ax_dif_temp(self, i, idade, cobertura, diferimento, B=1):
        """
        Esta função calcula o prêmio puro único de um seguro de vida temporário com diferimento.

        Parameters:
        -----------

        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               Idade do segurado.
        cobertura: int.
                   Tempo de cobertura.
        diferimento: int.
                     Tempo de diferimento.
        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio puro único.

        """

        dotal = self.Dotal(i=i, idade=idade, cobertura=diferimento)
        Ax_temp = self.Ax_temp(i=i, idade=idade + diferimento, cobertura=cobertura)

        premio = dotal * Ax_temp

        return premio * B


class anuidades:
    def __init__(self, tabua):
        self.tabua = np.array(tabua)

    def ax(self, i, idade, B=1, antecipado=False):

        """
        Esta função calcula o prêmio puro único de uma anuidade  vitalícia.

        Parameters:
        -----------
        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               idade do segurado.

        antecipado: bool.
                    Calcula uma anuidade antecipada ou postecipada.

        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio.
        """

        qx = self.tabua[idade:]  # Cutting down probability distribution
        v = (1 + i) ** -1

        t = np.arange(1, len(qx) + 1)
        qx = self.tabua[idade:]  # Cutting down probability distribution
        px = list(1 - qx)  # Calculating 1_p_x

        premio = sum(v**t * np.cumprod(px))

        if antecipado:
            premio = sum(v**t * np.cumprod(px)) + 1

        return premio * B

    def ax_temp(self, i, idade, cobertura, B=1, antecipado=False):

        """
        Esta função calcula o prêmio puro único de uma anuidade temporária.

        Parameters:
        -----------
        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               idade do segurado.

        cobertura: int.
                   Tempo de cobertura.

        antecipado: bool.
                    Calcula uma anuidade antecipada ou postecipada.

        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio.
        """

        N = idade + cobertura
        qx = self.tabua[idade:N]  # Cutting down probability distribution
        px = list(1 - qx)
        t = np.arange(1, cobertura + 1)
        v = (1 + i) ** -1

        if antecipado:
            px = list(1 - qx[:-1])  # Calculating 1_p_x
            px.insert(0, 1)  # setting 0_p_x = 1
            t = t - 1

        premio = sum(v**t * np.cumprod(px))

        return premio * B

    def ax_dif(self, i, idade, diferimento, B=1, antecipado=False):

        """
        Esta função calcula o prêmio puro único de uma anuidade vitalícia com diferimento.

        Parameters:
        -----------
        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               idade do segurado.

        diferimento: int.
                     Tempo de diferimento.

        antecipado: bool.
                    Calcula uma anuidade antecipada ou postecipada.


        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio.
        """

        diff = seguros(tabua=self.tabua).Dotal(
            i=i, idade=idade, cobertura=diferimento
        )

        ax = self.ax(i=i, idade=idade + diferimento, antecipado=antecipado)

        return diff * ax * B

    def ax_temp_dif(self, i, idade, diferimento, cobertura, B=1, antecipado=False):
        """
        Esta função calcula o prêmio puro único de uma anuidade temporária com diferimento.

        Parameters:
        -----------
        i: float.
           Taxa de juros a ser utilizada.

        idade: int.
               idade do segurado.

        cobertura: int.
                   Tempo de cobertura.

        diferimento: int.
                     Tempo de diferimento.

        antecipado: bool.
                    Calcula uma anuidade antecipada ou postecipada.


        B: float.
           Benefício segurado.

        Returns:
        --------

        Prêmio.
        """

        diff = seguros(tabua=self.tabua).Dotal(
            i=i, idade=idade, cobertura=diferimento
        )
        ax_tmp = self.ax_temp(
            i, idade=idade + diferimento, cobertura=cobertura, antecipado=antecipado
        )

        return diff * ax_tmp * B
