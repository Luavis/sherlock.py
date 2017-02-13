def generate_if(generator, node, ext_info):
    test = generator._generate(node.test, ext_info)
    generator.code_buffer.append('if [ %s ]; then' % test)
    for x in node.body:
        generator.code_buffer.append(generator._generate(x))
    return 'fi'

def generate_while(generator, node, ext_info):
    test = generator._generate(node.test, ext_info)
    generator.code_buffer.append('while [ %s ]; do' % test)
    for x in node.body:
        generator.code_buffer.append(generator._generate(x))
    return 'done'

def generate_for(generator, node, ext_info):
    iterator = generator._generate(node.iter, ext_info)
    generator.code_buffer.append('for %s in %s\ndo' % (node.target.id, iterator))
    for x in node.body:
        generator.code_buffer.append(generator._generate(x))
    return 'done'
