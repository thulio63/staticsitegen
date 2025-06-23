import unittest
from textnode import TextNode, TextType
from splitter import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestSplitter(unittest.TestCase):
    
    def test_markdown_image_extract(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text),  [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_markdown_link_extract(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_markdown_image_splitter(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_markdown_link_splitter(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )
    
    

    def test_md_to_blocks(self):
        text = """This is **bolded** paragraph

 This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        self.assertListEqual(markdown_to_blocks(text), [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ])
        
    def test_block_to_heading(self):
        text = "#### I'm a heading! "
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    
    def test_block_to_code(self):
        text = "```print(I AM CODE)```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_block_to_quote(self):
        text = """>I'm quoting
>a famous guy
>who was famous"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_block_to_unordered(self):
        text = """- a list
- a sick-ass list
- i'm rad as hell"""
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
    
    def test_block_to_ordered(self):
        text = """1. Listen Close
2. You Ignorant Fuck
3. i love you <3"""
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)
    
    def test_block_to_paragraph(self):
        text = """I'm text.
> not a quote
- not unordered
4. not ordered
`print('not code')`
Just text :)"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_heading(self):
        md = """# This is a heading

## This is a smaller heading"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1><h2>This is a smaller heading</h2></div>")
    
    def test_codeblock(self):
        md = """```This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
        
    def test_quote(self):
        md = """> This is a quote from a famous person.
> From what person?
>
> I certainly do not know.
>
> """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote><p>This is a quote from a famous person. From what person?</p><p>I certainly do not know.</p></blockquote></div>")

    def test_unordered_list(self):
        
        pass
    
    def test_ordered_list(self):
        
        pass
    
    def test_paragraphs(self):
        md = """This is a **bolded** paragraph
with the text
in a p tag

This is another paragraph with _italic_ text and `code` here"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(html,
        "<div><p>This is a <b>bolded</b> paragraph with the text in a p tag</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
        
if __name__ == "__main__":
    unittest.main()