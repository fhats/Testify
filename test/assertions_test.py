from testify import TestCase
from testify import assertions
from testify import run
from testify import assert_all
from testify import assert_any
from testify import assert_equal
from testify import assert_not_all
from testify import assert_not_any
from testify import assert_raises


class DiffMessageTestCase(TestCase):

    def test_shows_string_diffs(self):
        expected = 'Diff:\nl: abc<>\nr: abc<def>'
        diff_message = assertions._diff_message('abc', 'abcdef')
        assert_equal(expected, diff_message)

    def test_shows_repr_diffs(self):
        class AbcRepr(object):
            __repr__ = lambda self: 'abc'

        class AbcDefRepr(object):
            __repr__ = lambda self: 'abcdef'

        expected = 'Diff:\nl: abc<>\nr: abc<def>'
        diff_message = assertions._diff_message(AbcRepr(), AbcDefRepr())
        assert_equal(expected, diff_message)


class AssertEqualTestCase(TestCase):

    def test_shows_pretty_diff_output(self):
        expected = \
            'assertion failed: l == r\n' \
            "l: 'that reviewboard differ is awesome'\n" \
            "r: 'dat reviewboard differ is ozsom'\n\n" \
            'Diff:' \
            '\nl: <th>at reviewboard differ is <awe>som<e>\n' \
            'r: <d>at reviewboard differ is <oz>som<>'

        try:
            assert_equal('that reviewboard differ is awesome',
                         'dat reviewboard differ is ozsom')
        except AssertionError, e:
            assert_equal(expected, e.args[0])
        else:
            assert False, 'Expected `AssertionError`.'


class AssertAnyTestCase(TestCase):

    def test_assert_any(self):

        nice_list = [None, False, 1, True]
        bad_list = [False, False, None]

        def nice_gen():
            for i in xrange(3):
                yield None
            for i in xrange(10):
                yield i

        def bad_gen():
            for i in xrange(14):
                yield False

        assert_any(nice_list)
        assert_any(nice_gen())

        assert_raises(AssertionError, lambda: assert_any(bad_list))
        assert_raises(AssertionError, lambda: assert_any(bad_gen()))


class AssertNotAnyTestCase(TestCase):

    def test_assert_not_any(self):
        nice_list = [None, False, 1, True]
        bad_list = [False, False, None]

        def nice_gen():
            for i in xrange(3):
                yield None
            for i in xrange(10):
                yield i

        def bad_gen():
            for i in xrange(14):
                yield False

        assert_not_any(bad_list)
        assert_not_any(bad_gen())

        assert_raises(AssertionError, lambda: assert_not_any(nice_list))
        assert_raises(AssertionError, lambda: assert_not_any(nice_gen()))


class AssertAllTestCase(TestCase):

    def test_assert_all(self):

        nice_list = [True, "happy path!", 1, True]
        bad_list = [False, None, True, "sad path :("]

        def nice_gen():
            for i in xrange(10):
                yield i + 1

        def bad_gen():
            for i in xrange(2):
                yield True
            for i in xrange(14):
                yield False

        assert_all(nice_list)
        assert_all(nice_gen())

        assert_raises(AssertionError, lambda: assert_all(bad_list))
        assert_raises(AssertionError, lambda: assert_all(bad_gen()))


class AssertNotAllTestCase(TestCase):

    def test_assert_not_all(self):

        nice_list = [True, "happy path!", 1, True]
        bad_list = [False, None, True, "sad path :("]

        def nice_gen():
            for i in xrange(10):
                yield i + 1

        def bad_gen():
            for i in xrange(2):
                yield True
            for i in xrange(14):
                yield False

        assert_not_all(bad_list)
        assert_not_all(bad_gen())

        assert_raises(AssertionError, lambda: assert_not_all(nice_list))
        assert_raises(AssertionError, lambda: assert_not_all(nice_gen()))


if __name__ == '__main__':
    run()
