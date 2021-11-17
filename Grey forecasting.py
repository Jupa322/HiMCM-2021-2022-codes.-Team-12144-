import pandas as pd
import numpy as np


class GrayForecast():
    def __init__(self, data, datacolumn=None):

        if isinstance(data, pd.core.frame.DataFrame):
            self.data=data
            try:
                self.data.columns = ['ElevationData']
            except:
                if not datacolumn:
                    raise Exception
                else:
                    self.data = pd.DataFrame(data[datacolumn])
                    self.data.columns=['ElevationData']
        elif isinstance(data, pd.core.series.Series):
            self.data = pd.DataFrame(data, columns=['ElevationData'])
        else:
            self.data = pd.DataFrame(data, columns=['ElevationData'])

        self.forecast_list = self.data.copy()

        if datacolumn:
            self.datacolumn = datacolumn
        else:
            self.datacolumn = None

    def GMmakemodel(self, forecast=5):
        if forecast > len(self.data):
            raise Exception
        X_0 = np.array(self.forecast_list['ElevationData'].tail(forecast))
        X_1 = np.zeros(X_0.shape)
        for i in range(X_0.shape[0]):
            X_1[i] = np.sum(X_0[0:i+1])
        Z_1 = np.zeros(X_1.shape[0]-1)
        for i in range(1, X_1.shape[0]):
            Z_1[i-1] = -0.5*(X_1[i]+X_1[i-1])

        B = np.append(np.array(np.mat(Z_1).T), np.ones(Z_1.shape).reshape((Z_1.shape[0], 1)), axis=1)
        Yn = X_0[1:].reshape((X_0[1:].shape[0], 1))

        B = np.mat(B)
        Yn = np.mat(Yn)
        a_ = (B.T*B)**-1 * B.T * Yn

        a, b = np.array(a_.T)[0]

        X_ = np.zeros(X_0.shape[0])
        def f(k):
            return (X_0[0]-b/a)*(1-np.exp(a))*np.exp(-a*(k))

        self.forecast_list.loc[len(self.forecast_list)] = f(X_.shape[0])

    def forecast(self, time=5, forecast_data_len=5):
        for i in range(time):
            self.GMmakemodel(forecast=forecast_data_len)

    def log(self):
        res = self.forecast_list.copy()
        if self.datacolumn:
            res.columns = [self.datacolumn]
        return res


    def reset(self):
        self.forecast_list = self.data.copy()


gf = GrayForecast([12902678.34,12474061.06,11997350.86,11617700.42,11528992.9,11553500.51,11531363.09])
gf.forecast(370)
gf.log().to_csv('111forecast.csv')
