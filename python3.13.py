class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n</html>"
        return html


class TopLevelTag(HTML):
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        html = "<%s>\n" % self.tag
        for child in self.children:
            html += str(child)
        html += "\n</%s>" % self.tag
        return html


class Tag(TopLevelTag):
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)


def main(output=None):
    with HTML(output=output) as doc:
        # на данном шаге список дочерних элементов children тега html будет пуст, поэтому выводился бы <html></html> с помощью функций класса HTML
        with TopLevelTag("head") as head:
            # на данном шаге список дочерних элементов children будет пуст, выводился бы <head></head> с помощью функций класса TopLevelTag
            with Tag("title") as title:
                title.text = "hello"
                # на данном шаге выведется <title> hello </title>, так как дочерних элементов еще нет, выполнится 81 строчка кода
                head += title
                # на данном шаге выполнится __add__ класса HTML (в случае отсутствия наследования - класса TopLevelTag)
            # на данном шаге у тега head уже есть один дочерний элемент, поэтому выполнится условие функции __str__
            doc += head
            # на данном шаге выполняется __add__ класса HTML
        
        with TopLevelTag("body") as body:
            # на данном шаге выведется <body></body>
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                # на данном шаге выполнится 81 строчка кода
                body += h1
                # на данном шаге выполнится __add__ класса HTML (в случае отсутствия наследования - класса TopLevelTag)

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                # на данном шаге еще нет элементов списка children и выполнилась бы 81 строка кода
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    # на данном шаге выполнится 81 строчка кода
                    div += paragraph
                    # на данном шаге выполняется __add_ класса HTML (в случае отсутствия наследования - класса Tag)

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    # на данном шаге выполнится строчка кода с условием is_single == True
                    div += img
                    # на данном шаге выполнится __add_ класса HTML (в случае отсутствия наследования - класса Tag)
                body += div
                # на данном шаге выполнится __add__ класса HTML (в случае отсутствия наследования - класса TopLevelTag)
            doc += body
            # на данном шаге выполнится __add__ класса HTML

if __name__ == "__main__":
    main()