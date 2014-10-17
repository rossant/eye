import numpy as np

class KalmanFilter(object):

    def __init__(self, shape=None, estimated_std=1., process_std=1.):
        self.process_variance = process_std ** 2
        self.estimated_variance = estimated_std ** 2
        self.posteri_estimate = np.zeros(shape)
        self.posteri_error_estimate = np.ones(shape)

    def input(self, measurement):
        assert measurement.shape == self.posteri_estimate.shape
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.estimated_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

    def output(self):
        return self.posteri_estimate


if __name__ == '__main__':
    shape = 3
    kf = KalmanFilter(estimated_std=.1, process_std=.01, shape=shape)
    xs = []
    ys = []
    for i in range(100):
        x = i*.01+.025*np.random.randn(shape)
        kf.input(x)
        y = kf.output()
        xs.append(x)
        ys.append(y)
    import matplotlib.pyplot as plt
    plt.plot(np.vstack(xs)[:,0])
    plt.plot(np.vstack(ys)[:,0])
    plt.show()
