from sherlock.codelib.generator.dispatcher import add_generator


@add_generator('If')
def generate_if(self, node, ext_info):
    test = self.dispatch(node.test, ext_info)
    self.code_buffer.append('if [ %s ]; then' % test)
    for x in node.body:
        self.code_buffer.append(self.dispatch(x))
    return 'fi'

@add_generator('While')
def generate_while(self, node, ext_info):
    test = self.dispatch(node.test, ext_info)
    self.code_buffer.append('while [ %s ]; do' % test)
    for x in node.body:
        self.code_buffer.append(self.dispatch(x))
    return 'done'

@add_generator('For')
def generate_for(self, node, ext_info):
    iterator = self.dispatch(node.iter, ext_info)
    self.code_buffer.append('for %s in %s\ndo' % (node.target.id, iterator))
    for x in node.body:
        self.code_buffer.append(self.dispatch(x))
    return 'done'
