import pytest

from source.TagSystem import TagSystem

class TestTags:

    
    @pytest.mark.parametrize(
    "test_input, expected",
    [(['lamb', 'chicken', 'vegan', 'spicy'], ['chicken', 'lamb', 'spicy', 'vegan']), 
     (['lamb', 'chicken','lamb'], ['chicken', 'lamb']),
     ([], [])
    ])
    def testInit(self, test_input, expected):
        assert TagSystem(test_input).get_tags() == expected

    def testCreate_empty(self):
        ts = TagSystem()
        ts.create_tag("chicken")
        assert ts.get_tags() == ['chicken']

    def testCreate_nonempty(self):
        ts = TagSystem(['lamb', 'chicken','lamb'])
        ts.create_tag("pork")
        assert ts.get_tags() == ['chicken', 'lamb', 'pork']

    def testCreate_double(self):
        ts = TagSystem(['lamb', 'chicken','lamb'])
        ts.create_tag("lamb")
        assert ts.get_tags() == ['chicken', 'lamb']

    def testRemove(self):
        ts = TagSystem(['lamb', 'chicken','pork'])
        ts.remove_tag("lamb")
        assert ts.get_tags() == ['chicken', 'pork']