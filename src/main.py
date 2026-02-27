from textnode import TextType, TextNode
def main():
    object = TextNode("Hello World", TextType.TEXT, "https://example.com")
    print(object.__repr__())

main()