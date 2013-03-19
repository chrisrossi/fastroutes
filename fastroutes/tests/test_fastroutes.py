import unittest


class TestFastRoutes(unittest.TestCase):

    def make_one(self):
        from fastroutes import Routes
        return Routes()

    def define_routes(self, routes):
        routes.register('1', '/foo/bar')
        routes.register('2', '/{foo}/{bar}')
        routes.register('3', '/foo/baz')
        routes.register('4', '/foo/{articles}/manage')
        routes.register('5', '/foo/articles/manage')
        routes.register('6', '/foo/articles/{manage}')

    def test_one_level(self):
        routes = self.make_one()
        routes.register('foo', 'bar')
        matches = list(routes.match('/bar'))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['route'].name, 'foo')

    def test_two_levels(self):
        routes = self.make_one()
        routes.register('foo', '/foo/bar')
        matches = list(routes.match('/foo/bar'))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['route'].name, 'foo')
        self.assertEqual(matches[0]['match'], {})

    def test_match_multiple(self):
        routes = self.make_one()
        routes.register('one', '/foo/bar')
        routes.register('two', '/foo/{bar}')
        matches = list(routes.match('/foo/bar'))
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0]['route'].name, 'one')
        self.assertEqual(matches[0]['match'], {})
        self.assertEqual(matches[1]['route'].name, 'two')
        self.assertEqual(matches[1]['match'], {'bar': 'bar'})

    def test_match_regexp(self):
        routes = self.make_one()
        routes.register('one', '/foo/bar')
        routes.register('two', '/foo/{bar:\d\d}')
        matches = list(routes.match('/foo/22'))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['route'].name, 'two')
        self.assertEqual(matches[0]['match'], {'bar': '22'})

    def test_no_match(self):
        routes = self.make_one()
        routes.register('one', '/foo/{bar:\d\d}')
        matches = list(routes.match('/foo/no/way'))
        self.assertEqual(len(matches), 0)

    def test_variables_before_common_prefix(self):
        routes = self.make_one()
        self.define_routes(routes)
        matches = list(routes.match('/foo/baz'))
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0]['route'].name, '2')
        self.assertEqual(matches[1]['route'].name, '3')
