import re


class Routes(object):

    def __init__(self):
        self.tree = RouteNode()

    def register(self, name, route):
        elements = filter(None, route.split('/'))
        node = self.tree.get_register(elements)
        assert node.route is None, "Registration conflict"
        node.route = Route(name)

    def match(self, path):
        elements = filter(None, path.split('/'))
        state = []
        node = self.tree
        match = {}
        while elements:
            element = elements.pop(0)
            children = list(node.children)
            while children:
                pattern, childnode = children.pop(0)
                if pattern_matches(pattern, element, match):
                    if elements:
                        state.append(
                            (FakeNode(children), list(elements), match.copy()))
                        node = childnode
                        break
                    if childnode.route:
                        yield {'route': childnode.route, 'match': match.copy()}
            if state:
                node, elements, match = state.pop(-1)


def pattern_matches(pattern, element, match):
    if isinstance(pattern, tuple):
        name, regexp = pattern
        if regexp.match(element):
            match[name] = element
            return True
        return False
    return pattern == element


class Route(object):

    def __init__(self, name):
        self.name = name


class RouteNode(object):
    route = None

    def __init__(self):
        self.children = []

    def get_register(self, elements):
        pattern = elements.pop(0)
        if pattern.startswith('{'):
            pattern = pattern[1:-1]
            if ':' in pattern:
                name, regexp = pattern.split(':', 1)
            else:
                name = pattern
                regexp = '[^/]+'
            pattern = (name, re.compile(regexp))
        node = self.get(pattern)
        if not node:
            node = RouteNode()
            self.children.append((pattern, node))
        if elements:
            return self.get_register(elements)
        return node

    def get(self, name):
        children = self.children
        for childname, node in children:
            if childname == name:
                return node


class FakeNode(object):

    def __init__(self, children):
        self.children = children
