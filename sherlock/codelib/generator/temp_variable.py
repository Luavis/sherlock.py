class TempVariableManager(object):

    def __init__(self, prefix_name):
        self.prefix_name = prefix_name
        self.variable_id = 0

    def get_new_name(self):
        self.variable_id += 1
        return self.get_last_variable_name()

    def get_last_variable_name(self):
        return '%s_%d' % (self.prefix_name, self.variable_id)
