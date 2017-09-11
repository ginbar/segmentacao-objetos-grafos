
class SuperPixel(object):

    def __init__(self, label, momentos_t, momentos_d):
        self.label = label
        self.momentos_t = momentos_t
        self.momentos_d = momentos_d

    def __str__(self):
        return 'SuperPixel(label:{}, Ts:{}, Ds:{})'.format(self.label, self.momentos_t, self.momentos_d)
    