import unittest
from block_maker import markdown_to_blocks, block_to_block_type, BlockType

#things to test:
#Test to make sure it splits blocks correctly DONE
#Test to make sure it doesn't include empty blocks DONE
#Test to make sure it stripping whitespace correctly
class TestBlockMaker(unittest.TestCase):
    #Test to make sure it splits blocks correctly
    #Example:
    #Input: 
    #This is a heading
    #
    #This is a paragraph.
    #With multiple lines.
    #like this

    #-This is a list item
    #-This is another list item

    #output: [
    #"This is a heading",
    #"This is a paragraph.\nWith multiple lines.\nlike this",
    #"-This is a list item\n-This is another list item"]
    def test_markdown_to_blocks(self):
        markdown = """This is a heading

This is a paragraph.
With multiple lines.
like this

-This is a list item
-This is another list item"""
        expected = [
            "This is a heading",
            "This is a paragraph.\nWith multiple lines.\nlike this",
            "-This is a list item\n-This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_markdown_to_blocks_empty_blocks(self):
        markdown = """This is a heading with an empty block after it
        



        This is a paragraph with an empty block before it"""
        expected = [
            "This is a heading with an empty block after it",
            "This is a paragraph with an empty block before it"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_whitespace(self):
        markdown = """   This is a heading with whitespace before and after it   """
        expected = [
            "This is a heading with whitespace before and after it"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\nThis is a code block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote block\n> With multiple lines"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- This is an unordered list item\n- With multiple lines"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is an ordered list item\n2. With multiple lines"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)

        #Text quotes where not every line starts with > should not be considered a quote block
        self.assertEqual(block_to_block_type("> This is a quote block\nThis is not a quote block"), BlockType.PARAGRAPH)
        #Test unordered list where there isnt a space after some - should not be considered an unordered list block
        self.assertEqual(block_to_block_type("- This is an unordered list item\n-This is not an unordered list item"), BlockType.PARAGRAPH)
        #Test ordered list where there is a space after some numbers should not be considered an ordered list block
        self.assertEqual(block_to_block_type("1. This is an ordered list item\n2. This is an ordered list item\n3.This is not an ordered list item"), BlockType.PARAGRAPH)
        #Test ordered list where there is no . after some numbers should not be considered an ordered list block
        self.assertEqual(block_to_block_type("1. This is an ordered list item\n2 This is not an ordered list item\n3. This is not an ordered list item"), BlockType.PARAGRAPH)
        #Test ordered list where the numbers do not increment correctly should not be considered an ordered list block
        self.assertEqual(block_to_block_type("1. This is an ordered list item\n3. This is not an ordered list item\n4. This is not an ordered list item"), BlockType.PARAGRAPH)
        #Test Heading with more than 6 # should not be considered a heading block
        self.assertEqual(block_to_block_type("####### This is not a heading"), BlockType.PARAGRAPH)