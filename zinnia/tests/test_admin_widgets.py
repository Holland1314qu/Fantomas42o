# coding=utf-8
"""Test cases for Zinnia's admin widgets"""
from django.test import TestCase
from django.utils.encoding import smart_text

from zinnia.models.entry import Entry
from zinnia.signals import disconnect_entry_signals
from zinnia.admin.widgets import TagAutoComplete
from zinnia.admin.widgets import MPTTFilteredSelectMultiple


class MPTTFilteredSelectMultipleTestCase(TestCase):

    def test_render_option(self):
        widget = MPTTFilteredSelectMultiple('test', False)

        option = widget.render_option([], 1, 'Test', (4, 5))

        self.assertEqual(
            option,
            '<option value="1" data-tree-id="4"'
            ' data-left-value="5">Test</option>')

        option = widget.render_option(['0', '1', '2'], 1, 'Test', (4, 5))

        self.assertEqual(
            option,
            '<option value="1" selected="selected" data-tree-id="4"'
            ' data-left-value="5">Test</option>')

    def test_render_option_non_ascii_issue_317(self):
        widget = MPTTFilteredSelectMultiple('test', False)

        option = widget.render_option([], 1, 'тест', (1, 1))

        self.assertEqual(
            option,
            smart_text('<option value="1" data-tree-id="1"'
                       ' data-left-value="1">тест</option>'))

    def test_render_options(self):
        widget = MPTTFilteredSelectMultiple('test', False)
        self.assertEqual(widget.render_options([], []), '')

        options = widget.render_options([
            (1, 'Category 1', (1, 1)),
            (2, '|-- Category 2', (1, 2))], [])

        self.assertEqual(
            options,
            '<option value="1" data-tree-id="1" data-left-value="1">'
            'Category 1</option>\n<option value="2" data-tree-id="1" '
            'data-left-value="2">|-- Category 2</option>')

        options = widget.render_options([
            (1, 'Category 1', (1, 1)),
            (2, '|-- Category 2', (1, 2))], [2])

        self.assertEqual(
            options,
            '<option value="1" data-tree-id="1" data-left-value="1">'
            'Category 1</option>\n<option value="2" selected="selected" '
            'data-tree-id="1" data-left-value="2">|-- Category 2</option>')


class TagAutoCompleteTestCase(TestCase):

    def setUp(self):
        disconnect_entry_signals()

    def test_get_tags(self):
        widget = TagAutoComplete()
        self.assertEqual(
            widget.get_tags(),
            [])

        params = {'title': 'My entry',
                  'tags': 'zinnia, test',
                  'slug': 'my-entry'}
        Entry.objects.create(**params)
        self.assertEqual(
            widget.get_tags(),
            ['test', 'zinnia'])

    def test_render(self):
        widget = TagAutoComplete()
        params = {'title': 'My entry',
                  'tags': 'zinnia, test',
                  'slug': 'my-entry'}
        Entry.objects.create(**params)
        self.assertEqual(
            widget.render('tag', 'test,'),
            '<input class="vTextField" name="tag" type="text" value="test," />'
            '\n<script type="text/javascript">\n(function($) {'
            '\n  $(document).ready(function() {'
            '\n    $("#id_tag").select2({'
            '\n       width: "element",'
            '\n       maximumInputLength: 50,'
            '\n       tokenSeparators: [",", " "],'
            '\n       tags: [\'test\',\'zinnia\']'
            '\n     });\n    });'
            '\n}(django.jQuery));\n</script>')
