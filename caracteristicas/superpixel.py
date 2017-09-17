
class SuperPixel(object):

    def __init__(self, label, momentos):
        self.label = label
        self.momentos = momentos

    def __str__(self):
        return 'SuperPixel(label:{}, momentos:{})'.format(self.label, self.momentos)
    