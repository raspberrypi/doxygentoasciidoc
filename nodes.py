import re

from bs4 import BeautifulSoup, NavigableString

from .helpers import escape_text, sanitize, title


class Node:
    """The base class of a Doxygen XML node, able to convert itself to AsciiDoc.

    By default, it will walk any children of the given element, escaping text
    and handling whitespace as necessary, looking up any child elements in a
    mapping of element names to Node subclasses, delegating to their own
    implementation of an AsciiDoc conversion.
    """

    BLOCK_LEVEL_NODES = (
        "entry",
        "itemizedlist",
        "listitem",
        "orderedlist",
        "para",
        "parameteritem",
        "parameterlist",
        "programlisting",
        "row",
        "sect1",
        "sect2",
        "sect3",
        "simplesect",
        "table",
        "verbatim",
    )

    def __init__(self, node, position=0, xmldir=None):
        self.node = node
        self.position = position
        self.xmldir = xmldir

    @property
    def id(self):
        return sanitize(self.node["id"])

    def __getitem__(self, item):
        return self.node[item]

    def to_asciidoc(self, **kwargs):
        """Return an AsciiDoc representation of this node.

        By default, text nodes will be escaped with whitespace processed as in
        an HTML Document Object Model (unless we're inside a program listing,
        in which case it will be printed verbatim). Other elements will be
        looked up in a mapping of element names to Node subclasses and
        conversion delegated to instances of the appropriate subclass.

        In order to properly handle whitespace, we process child elements as
        either within an "inline" context (the default) or a "block" context
        (if at least one of the child elements is considered to be a "block",
         e.g. a admonition). If we're in a block context, all consecutive
        inline elements will be combined into a new block element.

        See https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Whitespace
        """
        if isinstance(self.node, NavigableString):
            if self.node:
                if kwargs.get("programlisting", False):
                    return str(self.node)

                # 1. Remove whitespace around a line break
                # 2. Convert line breaks to spaces
                # 3. Ignore spaces immediately following another space
                stripped = re.sub(
                    r"\s{2,}",
                    " ",
                    re.sub(r"\s+\n\s+", "\n", escape_text(self.node)).replace(
                        "\n", " "
                    ),
                )
                # 4. Sequences of spaces at the beginning and end of an element are removed
                if self.position == 0:
                    stripped = stripped.lstrip()
                if (
                    self.node.parent
                    and self.position == len(self.node.parent.contents) - 1
                ):
                    stripped = stripped.rstrip()
                return stripped

            return ""

        if self.isblockcontext():
            # Because we're inside a block formatting context, everything must be a block
            # including any text nodes.
            para = None
            children = self.node.contents[:]
            for child in children:
                if child.name not in self.BLOCK_LEVEL_NODES:
                    # Wrap contiguous inline elements into a block
                    if para:
                        # If there is already a wrapper, add this inline
                        # element to it
                        para.append(child)
                    else:
                        # If there isn't already a wrapper, start one by
                        # wrapping this element in a <para>
                        para = child.wrap(self.soup().new_tag("para"))
                elif para and para.get_text(strip=True):
                    # If there is a wrapper and it isn't empty, prepend it before this block
                    child.insert_before(para)
                    para = None
            if para:
                # Append any remaining wrapped inline elements at the end
                self.node.append(para)

            # Combine any adjacent text nodes since we modified the tree
            self.node.smooth()

            return self.block_separator(**kwargs).join(
                asciidoc for asciidoc in self.asciidoc_contents(**kwargs) if asciidoc
            )

        return "".join(self.asciidoc_contents(**kwargs))

    def soup(self):
        """Return the Beautiful Soup object for this node."""
        node = self.node
        while not isinstance(node, BeautifulSoup):
            node = node.parent
        return node

    def block_separator(self, **_kwargs):
        """Return the separator to be used between blocks in a block context."""
        return "\n\n"

    def isblockcontext(self):
        """Return whether this node is a block context or not based on its children."""
        return any(child.name in self.BLOCK_LEVEL_NODES for child in self.node.children)

    def asciidoc_contents(self, **kwargs):
        """Return a list of the AsciiDoc contents of this node."""
        return [child.to_asciidoc(**kwargs) for child in self.children()]

    def child(self, selector):
        child = self.node.find(selector, recursive=False)
        if not child:
            return None
        return self.nodefor(child)(child, xmldir=self.xmldir)

    def children(self, selector=None, **kwargs):
        """Return a list of the child Nodes of this node.

        Takes an optional selector to only return certain child elements."""
        if selector:
            children = self.node(selector, recursive=False, **kwargs)
        else:
            children = self.node.children

        return [
            self.nodefor(child)(child, position=position, xmldir=self.xmldir)
            for position, child in enumerate(children)
        ]

    def attributes(self):
        """Return the attributes for this node."""
        return {
            key: self.node.attrs.get(key)
            for key in ("id", "role", "type", "tag")
            if key in self.node.attrs
        }

    def descendants(self, selector, **kwargs):
        """Return a list of descendant Nodes matching the given selector."""
        return [
            self.nodefor(child)(child, position=position, xmldir=self.xmldir)
            for position, child in enumerate(
                self.node(selector, recursive=True, **kwargs)
            )
        ]

    def text(self, selector=None):
        """Return the stripped text of the given child."""
        if not selector:
            return self.node.get_text(strip=True)

        child = self.node.find(selector, recursive=False)
        if not child:
            return None

        return child.get_text(strip=True)

    def previous_node(self):
        """Return the previous sibling element to this Node, skipping text nodes."""
        return next((node for node in self.node.previous_siblings if node.name), None)

    def next_node(self):
        """Return the next sibling element to this Node, skipping text nodes."""
        return next((node for node in self.node.next_siblings if node.name), None)

    def nodefor(self, element):
        """Return the appropriate Node class for a given element."""
        if element.name == "compounddef":
            return {"group": GroupNode, "page": PageNode}[element["kind"]]

        if element.name == "sectiondef":
            return {
                "define": DefineSectiondefNode,
                "enum": EnumSectiondefNode,
                "typedef": TypedefSectiondefNode,
                "func": FunctionSectiondefNode,
                "var": VariableSectiondefNode,
                "user-defined": UserDefinedSectiondefNode,
            }[element["kind"]]

        if element.name == "memberdef":
            return {
                "define": DefineMemberdefNode,
                "enum": EnumMemberdefNode,
                "typedef": TypedefMemberdefNode,
                "function": FunctionMemberdefNode,
                "variable": VariableMemberdefNode,
            }[element["kind"]]

        return {
            "anchor": AnchorNode,
            "bold": BoldNode,
            "briefdescription": Node,
            "detaileddescription": DetaileddescriptionNode,
            "description": Node,
            "codeline": CodelineNode,
            "compound": Node,
            "computeroutput": ComputeroutputNode,
            "copy": CopyrightNode,
            "emphasis": EmphasisNode,
            "entry": EntryNode,
            "enumvalue": Node,
            "highlight": Node,
            "initializer": Node,
            "innergroup": InnergroupNode,
            "innerclass": InnerclassNode,
            "itemizedlist": ItemizedlistNode,
            "listitem": ListitemNode,
            "linebreak": LinebreakNode,
            "mdash": MdashNode,
            "ndash": NdashNode,
            "nonbreakablespace": NonbreakablespaceNode,
            "orderedlist": OrderedlistNode,
            "para": Node,
            "param": Node,
            "parameterdescription": ParameterdescriptionNode,
            "parameteritem": Node,
            "parameterlist": ParameterlistNode,
            "parameternamelist": ParameternamelistNode,
            "programlisting": ProgramlistingNode,
            "ref": RefNode,
            "row": RowNode,
            "sect1": SectNode,
            "sect2": SectNode,
            "sect3": SectNode,
            "simplesect": SimplesectNode,
            "sp": SpNode,
            "table": TableNode,
            "type": Node,
            "ulink": UlinkNode,
            "verbatim": VerbatimNode,
            None: Node,
        }[element.name]


class DoxygenindexNode(Node):
    """Return the AsciiDoc representation from a root Doxygen doxygenindex node."""

    def to_asciidoc(self, depth=0, **kwargs):
        output = []
        for module in self.rootmodules():
            title_ = module.node.text("title")
            output.append(
                title(
                    title_,
                    depth,
                    attributes={
                        **self.attributes(),
                        "id": module.refid,
                        "reftext": title_,
                    },
                ),
            )
            briefdescription = module.node.child("briefdescription").to_asciidoc(
                **kwargs, depth=depth
            )
            if briefdescription:
                output.append(briefdescription)
            detaileddescription = module.node.child("detaileddescription").to_asciidoc(
                **kwargs, documentation=True, depth=depth + 1
            )
            if detaileddescription:
                output.append(detaileddescription)
            table = ['[cols="1,4"]', "|==="]
            for child in module.children:
                table.append(child.to_asciidoc_row())
            table.append("|===")
            if len(table) > 3:
                output.append("\n".join(table))
            for child in module.children:
                output.append(child.to_asciidoc(**kwargs, depth=depth + 1))
        return "\n\n".join(output)

    def rootmodules(self):
        """Return a list of root modules from the Doxygen index.

        Traverse the full list of modules from the Doxygen index, building up a
        hierarchy in memory before returning only the root nodes."""
        groups = {}

        for compound in self.children("compound", kind="group"):
            with open(
                f'{self.xmldir}/{compound["refid"]}.xml', encoding="utf-8"
            ) as compoundxml:
                doxygenroot = Node(
                    BeautifulSoup(compoundxml, "xml").doxygen, xmldir=self.xmldir
                )
            for compounddef in doxygenroot.children("compounddef", kind="group"):
                group = groups.setdefault(
                    compounddef["id"], self.Group(compounddef["id"])
                )
                group.node = compounddef

                for innergroup in compounddef.children("innergroup"):
                    child = groups.setdefault(
                        innergroup["refid"], self.Group(innergroup["refid"])
                    )
                    child.parent = group
                    group.children.append(child)

        return (group for (refid, group) in groups.items() if group.isroot())

    class Group:
        """An inner class to represent the full hierarchy of modules."""

        def __init__(self, refid):
            self.refid = refid
            self.parent = None
            self.children = []
            self.node = None

        def isroot(self):
            return self.parent is None

        def to_asciidoc(self, depth=0, **kwargs):
            output = [self.node.to_asciidoc(**kwargs, depth=depth)]
            for child in self.children:
                output.append(child.to_asciidoc(**kwargs, depth=depth + 1))
            return "\n\n".join(output)

        def to_asciidoc_row(self, depth=0):
            indent = "{nbsp}" * 4 * depth
            briefdescription = self.node.child("briefdescription").to_asciidoc()
            output = []
            row = (
                f"|{indent}<<{sanitize(self.refid)},{escape_text(self.node.text('title'))}>>",
                f"|{briefdescription}",
            )
            output.append("\n".join(row))
            for child in self.children:
                output.append(child.to_asciidoc_row(depth=depth + 1))
            return "\n\n".join(output)


class GroupNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        # pylint: disable=too-many-locals,too-many-branches
        output = [self.__output_title(depth=depth)]
        briefdescription = self.__output_briefdescription(**kwargs, depth=depth)
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = self.__output_detaileddescription(
            **kwargs, depth=depth + 1
        )
        if detaileddescription:
            output.append(detaileddescription)
        modules = self.__list_modules(**kwargs, depth=depth + 1)
        if modules:
            output.append(modules)
        macros = self.__list_macros(**kwargs, depth=depth + 1)
        if macros:
            output.append(macros)
        typedefs = self.__list_typedefs(**kwargs, depth=depth + 1)
        if typedefs:
            output.append(typedefs)
        enums = self.__list_enums(**kwargs, depth=depth + 1)
        if enums:
            output.append(enums)
        functions = self.__list_functions(**kwargs, depth=depth + 1)
        if functions:
            output.append(functions)
        variables = self.__list_variables(**kwargs, depth=depth + 1)
        if variables:
            output.append(variables)
        userdefinedsections = self.__list_userdefined_sections(
            **kwargs, depth=depth + 1
        )
        if userdefinedsections:
            output.append(userdefinedsections)
        macrodetails = self.__list_macro_details(**kwargs, depth=depth + 1)
        if macrodetails:
            output.append(macrodetails)
        typedefdetails = self.__list_typedef_details(**kwargs, depth=depth + 1)
        if typedefdetails:
            output.append(typedefdetails)
        enumdetails = self.__list_enum_details(**kwargs, depth=depth + 1)
        if enumdetails:
            output.append(enumdetails)
        functiondetails = self.__list_function_details(**kwargs, depth=depth + 1)
        if functiondetails:
            output.append(functiondetails)
        variabledetails = self.__list_variable_details(**kwargs, depth=depth + 1)
        if variabledetails:
            output.append(variabledetails)
        return "\n\n".join(output)

    def __output_title(self, depth=0):
        title_ = self.text("title")
        return title(title_, depth, attributes={**self.attributes(), "reftext": title_})

    def __output_briefdescription(self, **kwargs):
        return self.child("briefdescription").to_asciidoc(**kwargs)

    def __output_detaileddescription(self, **kwargs):
        return self.child("detaileddescription").to_asciidoc(**kwargs)

    def __list_modules(self, depth=0, **kwargs):
        innergroups = self.children("innergroup")
        if not innergroups:
            return ""

        output = [title("Modules", depth)]
        modules = []
        for innergroup in innergroups:
            modules.append(innergroup.to_asciidoc(**kwargs, depth=depth))
        output.append("\n".join(modules))
        return "\n\n".join(output)

    def __list_macros(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="define"):
            output.append(sectiondef.to_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_enums(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="enum"):
            output.append(sectiondef.to_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_typedefs(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="typedef"):
            output.append(sectiondef.to_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_variables(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="var"):
            output.append(sectiondef.to_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_functions(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="func"):
            output.append(sectiondef.to_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_userdefined_sections(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="user-defined"):
            output.append(sectiondef.to_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_typedef_details(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="typedef"):
            output.append(sectiondef.to_details_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_function_details(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="func"):
            output.append(sectiondef.to_details_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_enum_details(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="enum"):
            output.append(sectiondef.to_details_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_variable_details(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="var"):
            output.append(sectiondef.to_details_asciidoc(**kwargs))
        return "\n\n".join(output)

    def __list_macro_details(self, **kwargs):
        output = []
        for sectiondef in self.children("sectiondef", kind="define"):
            output.append(sectiondef.to_details_asciidoc(**kwargs))
        return "\n\n".join(output)


class PageNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        output = []

        title_ = self.__output_title(depth=depth)
        if title_:
            output.append(title_)

        detaileddescription = self.__output_detaileddescription(**kwargs, depth=depth)
        if detaileddescription:
            output.append(detaileddescription)

        return "\n\n".join(output)

    def __output_title(self, depth=0):
        title_ = self.text("title")
        if title_:
            return title(title_, depth, attributes=self.attributes())
        return None

    def __output_detaileddescription(self, **kwargs):
        return self.child("detaileddescription").to_asciidoc(
            **kwargs, documentation=True
        )


class InnergroupNode(Node):
    def to_asciidoc(self, **kwargs):
        with open(
            f"{self.xmldir}/{self.node['refid']}.xml", encoding="utf-8"
        ) as compoundxml:
            compounddef = Node(
                BeautifulSoup(compoundxml, "xml").compounddef, xmldir=self.xmldir
            )
            output = [
                f"<<{compounddef.id},{escape_text(compounddef.text('title'))}>>::"
            ]
            briefdescription = compounddef.child("briefdescription").to_asciidoc(
                **kwargs
            )
            if briefdescription:
                output.append(briefdescription)
            else:
                output.append("{empty}")
            return " ".join(output)


class InnerclassNode(Node):
    def to_asciidoc(self, **kwargs):
        with open(
            f"{self.xmldir}/{self.node['refid']}.xml", encoding="utf-8"
        ) as compoundxml:
            compounddef = Node(
                BeautifulSoup(compoundxml, "xml").compounddef, xmldir=self.xmldir
            )
            output = [
                f"struct <<{compounddef.id},{escape_text(compounddef.text('compoundname'))}>>::"
            ]
            briefdescription = compounddef.child("briefdescription").to_asciidoc(
                **kwargs
            )
            if briefdescription:
                output.append(briefdescription)
            else:
                output.append("{empty}")
            return " ".join(output)


class ProgramlistingNode(Node):
    def to_asciidoc(self, **kwargs):
        output = []
        if "filename" in self.node.attrs:
            output.append(f"// {self.node['filename']}")
        output.append("[source,c,linenums]\n----")
        for codeline in self.children("codeline"):
            output.append(codeline.to_asciidoc(**kwargs))
        output.append("----")
        return "\n".join(output)


class VerbatimNode(Node):
    def to_asciidoc(self, **kwargs):
        kwargs["programlisting"] = True
        return f"[source,c]\n----\n{super().to_asciidoc(**kwargs)}----"


class CodelineNode(Node):
    def to_asciidoc(self, **kwargs):
        kwargs["programlisting"] = True
        return super().to_asciidoc(**kwargs)


class AnchorNode(Node):
    def to_asciidoc(self, **kwargs):
        return f"[[{self.id}]]"


class SpNode(Node):
    def to_asciidoc(self, **kwargs):
        return " "


class NdashNode(Node):
    def to_asciidoc(self, **kwargs):
        return "–"


class MdashNode(Node):
    def to_asciidoc(self, **kwargs):
        return "—"


class UlinkNode(Node):
    def to_asciidoc(self, **kwargs):
        return f"{self.node['url']}[{super().to_asciidoc(**kwargs)}]"


class NonbreakablespaceNode(Node):
    def to_asciidoc(self, **kwargs):
        return "{nbsp}"


class SectNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        output = []

        title_ = self.text("title")
        if title_:
            output.append(title(title_, depth + 1, attributes=self.attributes()))

        for child in self.children(["para", "sect2", "sect3"]):
            output.append(child.to_asciidoc(**kwargs, depth=depth + 1))

        return "\n\n".join(output)


class SimplesectNode(Node):
    def to_asciidoc(self, **kwargs):
        previous_node = self.previous_node()
        next_node = self.next_node()
        kind = self.node.get("kind")

        if kind == "see":
            output = []
            if not (
                previous_node
                and previous_node.name == "simplesect"
                and previous_node.get("kind") == "see"
            ):
                output.append("--\n*See also*\n\n")
            output.append(super().to_asciidoc(**kwargs))
            if not (
                next_node
                and next_node.name == "simplesect"
                and next_node.get("kind") == "see"
            ):
                output.append("\n--")
            return "".join(output)

        if kind == "return":
            return f"--\n*Returns*\n\n{super().to_asciidoc(**kwargs)}\n--"

        if kind == "note":
            output = []
            if not (
                previous_node
                and previous_node.name == "simplesect"
                and previous_node.get("kind") == "note"
            ):
                output.append("[NOTE]\n====\n")
            output.append(super().to_asciidoc(**kwargs))
            if not (
                next_node
                and next_node.name == "simplesect"
                and next_node.get("kind") == "note"
            ):
                output.append("\n====")

            return "".join(output)

        if kind == "par":
            output = []

            title_ = self.text("title")
            if title_:
                output.append(f"*{escape_text(title_)}*")

            for para in self.children("para"):
                asciidoc = para.to_asciidoc(**kwargs)
                if asciidoc:
                    output.append(asciidoc)

            return "\n\n".join(output)

        return super().to_asciidoc(**kwargs)


class ParameterlistNode(Node):
    def to_asciidoc(self, **kwargs):
        if self.node["kind"] == "param":
            return "".join(
                (
                    "*Parameters*\n\n",
                    "[horizontal]\n",
                    super().to_asciidoc(**kwargs),
                )
            )

        return super().to_asciidoc(**kwargs)

    def block_separator(self, **_kwargs):
        return "\n"


class ParameternamelistNode(Node):
    def to_asciidoc(self, **kwargs):
        return f"`{escape_text(self.text('parametername'))}`::"


class ParameterdescriptionNode(Node):
    def to_asciidoc(self, **kwargs):
        output = super().to_asciidoc(**kwargs)
        if not output:
            return "{empty}"

        return output


class RefNode(Node):
    def to_asciidoc(self, **kwargs):
        if kwargs.get("programlisting", False):
            return super().to_asciidoc(**kwargs)

        return f"<<{self.refid},{escape_text(self.text())}>>"

    @property
    def refid(self):
        return sanitize(self.node["refid"])


class EmphasisNode(Node):
    def to_asciidoc(self, **kwargs):
        return f"_{super().to_asciidoc(**kwargs)}_"


class BoldNode(Node):
    def to_asciidoc(self, **kwargs):
        return f"*{super().to_asciidoc(**kwargs)}*"


class CopyrightNode(Node):
    def to_asciidoc(self, **kwargs):
        return "©"


class ComputeroutputNode(Node):
    def to_asciidoc(self, **kwargs):
        return f"`{super().to_asciidoc(**kwargs)}`"


class ItemizedlistNode(Node):
    def to_asciidoc(self, **kwargs):
        kwargs["ordered"] = False
        kwargs["unordereddepth"] = kwargs.get("unordereddepth", 0) + 1
        return super().to_asciidoc(**kwargs)


class OrderedlistNode(Node):
    def to_asciidoc(self, **kwargs):
        kwargs["ordered"] = True
        kwargs["ordereddepth"] = kwargs.get("ordereddepth", 0) + 1
        return super().to_asciidoc(**kwargs)


class ListitemNode(Node):
    def to_asciidoc(self, **kwargs):
        if kwargs.get("ordered", False):
            marker = "." * kwargs.get("ordereddepth", 1)
        else:
            marker = "*" * kwargs.get("unordereddepth", 1)
        if kwargs.get("ordereddepth", 0) + kwargs.get("unordereddepth", 0) == 1:
            return f"{marker} {{empty}}\n+\n--\n{super().to_asciidoc(**kwargs)}\n--"
        return f"{marker} {{empty}}\n+\n{super().to_asciidoc(**kwargs)}"

    def block_separator(self, **kwargs):
        if kwargs.get("ordereddepth", 0) + kwargs.get("unordereddepth", 0) == 1:
            return "\n\n"
        return "\n+\n"


class LinebreakNode(Node):
    def to_asciidoc(self, **kwargs):
        return " +\n"


class TableNode(Node):
    def to_asciidoc(self, **kwargs):
        return f"|===\n{super().to_asciidoc(**kwargs)}\n|==="


class RowNode(Node):
    def block_separator(self, **_kwargs):
        if self.position == 0:
            return " "
        return "\n"


class EntryNode(Node):
    def to_asciidoc(self, **kwargs):
        return f"|{super().to_asciidoc(**kwargs)}"


class DetaileddescriptionNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        output = []
        contents = super().to_asciidoc(**kwargs, depth=depth)
        if contents:
            if not kwargs.get("documentation", False):
                output.append(
                    title(
                        "Detailed Description",
                        depth,
                        attributes=self.attributes(),
                    )
                )
            output.append(contents)
            return "\n\n".join(output)
        return ""


class FunctionMemberdefNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        output = [title(self.text("name"), depth, attributes=self.attributes())]
        if self.node["static"] == "yes":
            definition = ["[.memname]`static "]
        else:
            definition = ["[.memname]`"]
        definition.append(self.child("type").to_asciidoc(**kwargs, depth=depth))
        definition.append(f" {escape_text(self.text('name'))} ")
        params = self.children("param")
        if params:
            args = []
            for param in params:
                arg = []
                arg.append(param.child("type").to_asciidoc(**kwargs, depth=depth))
                declname = param.text("declname")
                if declname:
                    arg.append(escape_text(declname))
                args.append(" ".join(arg))
            definition.append(f"({', '.join(args)})")
        suffix = []
        if self.node["inline"] == "yes":
            suffix.append("[inline]")
        if self.node["static"] == "yes":
            suffix.append("[static]")
        if suffix:
            definition.append(" ")
            definition.append(", ".join(suffix))
        definition.append("`")
        output.append("".join(definition))
        briefdescription = self.child("briefdescription").to_asciidoc(
            **kwargs, depth=depth
        )
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = self.child("detaileddescription").to_asciidoc(
            **kwargs, depth=depth + 1, documentation=True
        )
        if detaileddescription:
            output.append(detaileddescription)
        return "\n\n".join(output)


class TypedefMemberdefNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        output = [title(self.text("name"), depth, attributes=self.attributes())]
        output.append(f"[.memname]`{escape_text(self.text('definition'))}`")
        briefdescription = self.child("briefdescription").to_asciidoc(
            **kwargs, depth=depth
        )
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = self.child("detaileddescription").to_asciidoc(
            **kwargs, depth=depth + 1, documentation=True
        )
        if detaileddescription:
            output.append(detaileddescription)
        return "\n\n".join(output)


class EnumMemberdefNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        name = self.text("name")
        output = [title(name or "anonymous enum", depth, attributes=self.attributes())]
        if name:
            output.append(f"[.memname]`enum {escape_text(name)}`")
        else:
            output.append("[.memname]`anonymous enum`")
        briefdescription = self.child("briefdescription").to_asciidoc(
            **kwargs, depth=depth
        )
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = self.child("detaileddescription").to_asciidoc(
            **kwargs, depth=depth + 1, documentation=True
        )
        if detaileddescription:
            output.append(detaileddescription)

        enumvalues_with_descriptions = self.children(
            lambda tag: tag.name == "enumvalue"
            and tag.briefdescription.get_text(strip=True)
        )
        if enumvalues_with_descriptions:
            table = [".Enumerator"]
            table.append('[cols="h,1"]')
            table.append("|===")
            rows = []
            for enumvalue in enumvalues_with_descriptions:
                row = [f"|[[{enumvalue.id}]]{enumvalue.text('name')}"]
                briefdescription = enumvalue.child("briefdescription").to_asciidoc(
                    **kwargs
                )
                row.append(f"|{briefdescription}")
                rows.append("\n".join(row))
            table.append("\n\n".join(rows))
            table.append("|===")
            output.append("\n".join(table))
        return "\n\n".join(output)


class VariableMemberdefNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        name = self.text("name") or self.text("qualifiedname")
        output = [
            title(name, depth, attributes=self.attributes()),
        ]
        definition = self.text("definition")
        if self.text("initializer"):
            initializer = self.child("initializer").to_asciidoc(programlisting=True)
            output.append(
                "\n".join(
                    (
                        "[source,c]",
                        "----",
                        f"{definition} {initializer.lstrip()}",
                        "----",
                    )
                )
            )
        else:
            output.append(f"[.memname]`{escape_text(definition)}`")
        briefdescription = self.child("briefdescription").to_asciidoc(
            **kwargs, depth=depth
        )
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = self.child("detaileddescription").to_asciidoc(
            **kwargs, depth=depth + 1, documentation=True
        )
        if detaileddescription:
            output.append(detaileddescription)
        return "\n\n".join(output)


class DefineMemberdefNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        output = [title(self.text("name"), depth, attributes=self.attributes())]
        name = self.text("name")
        params = [param.text() for param in self.children("param")]
        if params:
            argsstring = f"({', '.join(params)})"
        else:
            argsstring = ""
        if self.text("initializer"):
            initializer = self.child("initializer").to_asciidoc(programlisting=True)
            if "\n" in initializer:
                output.append(
                    "\n".join(
                        (
                            "[source,c]",
                            "----",
                            f"#define {name}{argsstring} {initializer.lstrip()}",
                            "----",
                        )
                    )
                )
            else:
                output.append(
                    f"[.memname]`#define {escape_text(name)}{escape_text(argsstring)} "
                    f"{escape_text(initializer).rstrip()}`"
                )
        else:
            output.append(
                f"[.memname]`#define {escape_text(name)}{escape_text(argsstring)}`"
            )
        briefdescription = self.child("briefdescription").to_asciidoc(
            **kwargs, depth=depth
        )
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = self.child("detaileddescription").to_asciidoc(
            **kwargs, depth=depth + 1, documentation=True
        )
        if detaileddescription:
            output.append(detaileddescription)
        return "\n\n".join(output)


class FunctionSectiondefNode(Node):
    def to_details_asciidoc(self, depth=0, **kwargs):
        memberdefs = self.children("memberdef", kind="function")
        if not memberdefs:
            return ""

        output = [title("Function Documentation", depth)]
        functions = []
        for memberdef in sorted(
            memberdefs, key=lambda memberdef: memberdef.text("name")
        ):
            functions.append(memberdef.to_asciidoc(**kwargs, depth=depth + 1))
        output.append("\n\n".join(functions))
        return "\n\n".join(output)

    def to_asciidoc(self, depth=0, **kwargs):
        output = [title("Functions", depth)]
        functions = []
        for memberdef in self.children("memberdef", kind="function"):
            if memberdef["static"] == "yes":
                function = ["`static "]
            else:
                function = ["`"]
            function.append(memberdef.child("type").to_asciidoc(**kwargs, depth=depth))
            function.append(
                f" <<{memberdef.id},{escape_text(memberdef.text('name'))}>> "
            )
            function.append(f"{escape_text(memberdef.text('argsstring'))}`:: ")
            briefdescription = memberdef.child("briefdescription").to_asciidoc(
                **kwargs, depth=depth
            )
            if briefdescription:
                function.append(briefdescription)
            else:
                function.append("{empty}")
            functions.append("".join(function))
        output.append("\n".join(functions))
        return "\n\n".join(output)


class TypedefSectiondefNode(Node):
    def to_details_asciidoc(self, depth=0, **kwargs):
        memberdefs = self.children("memberdef", kind="typedef")
        if not memberdefs:
            return ""
        output = [title("Typedef Documentation", depth)]
        typedefs = []
        for memberdef in memberdefs:
            typedefs.append(memberdef.to_asciidoc(**kwargs, depth=depth + 1))
        output.append("\n".join(typedefs))
        return "\n\n".join(output)

    def to_asciidoc(self, depth=0, **kwargs):
        output = [title("Typedefs", depth)]
        typedefs = []
        for memberdef in self.children("memberdef", kind="typedef"):
            type_ = memberdef.child("type").to_asciidoc(**kwargs, depth=depth)
            typedef = [
                f"`typedef {type_} <<{memberdef.id},{escape_text(memberdef.text('name'))}>>"
                f"{escape_text(memberdef.text('argsstring'))}`::"
            ]
            briefdescription = memberdef.child("briefdescription").to_asciidoc(
                **kwargs, depth=depth
            )
            if briefdescription:
                typedef.append(briefdescription)
            else:
                typedef.append("{empty}")
            typedefs.append(" ".join(typedef))
        output.append("\n".join(typedefs))
        return "\n\n".join(output)


class EnumSectiondefNode(Node):
    def to_details_asciidoc(self, depth=0, **kwargs):
        memberdefs = self.children("memberdef", kind="enum")
        if not memberdefs:
            return ""

        output = [title("Enumeration Type Documentation", depth)]
        enums = []
        for memberdef in memberdefs:
            enums.append(memberdef.to_asciidoc(**kwargs, depth=depth + 1))
        output.append("\n".join(enums))
        return "\n\n".join(output)

    def to_asciidoc(self, depth=0, **kwargs):
        output = [title("Enumerations", depth)]
        enums = []
        for memberdef in self.children("memberdef", kind="enum"):
            enum = []
            name = memberdef.text("name")
            if name:
                enum.append(
                    f"`enum <<{memberdef.id},{escape_text(memberdef.text('name'))}>>"
                )
                enum.append(" { ")
            else:
                enum.append("`enum { ")
            enumvalues = []
            for enumvalue in memberdef.children("enumvalue"):
                if enumvalue.text("briefdescription"):
                    value = [
                        f"<<{enumvalue.id},{escape_text(enumvalue.text('name'))}>>"
                    ]
                else:
                    value = [escape_text(enumvalue.text("name"))]
                initializer = enumvalue.text("initializer")
                if initializer:
                    value.append(escape_text(initializer))
                enumvalues.append(" ".join(value))
            enum.append(", ".join(enumvalues))
            enum.append(" }`:: ")
            briefdescription = memberdef.child("briefdescription").to_asciidoc(
                **kwargs, depth=depth
            )
            if briefdescription:
                enum.append(briefdescription)
            else:
                enum.append("{empty}")
            enums.append("".join(enum))
        output.append("\n".join(enums))
        return "\n\n".join(output)


class DefineSectiondefNode(Node):
    def to_details_asciidoc(self, depth=0, **kwargs):
        memberdefs = self.children("memberdef", kind="define")
        if not memberdefs:
            return ""

        output = [title("Macro Definition Documentation", depth)]
        macros = []
        for memberdef in memberdefs:
            macros.append(memberdef.to_asciidoc(**kwargs, depth=depth + 1))
        output.append("\n".join(macros))
        return "\n\n".join(output)

    def to_asciidoc(self, depth=0, **kwargs):
        output = [title("Macros", depth)]
        macros = []
        for memberdef in self.children("memberdef", kind="define"):
            params = [param.text() for param in memberdef.children("param")]
            if params:
                argsstring = f"({', '.join(params)})"
            else:
                argsstring = ""
            macro = [
                f"* `#define <<{memberdef.id},{escape_text(memberdef.text('name'))}>>"
                f"{escape_text(argsstring)}"
            ]
            if memberdef.text("initializer"):
                initializer = memberdef.child("initializer").to_asciidoc(
                    programlisting=True
                )
                if "\n" not in initializer:
                    macro.append(f" {escape_text(initializer)}`")
                else:
                    macro.append("`")
            else:
                macro.append("`")
            macros.append("".join(macro))
        output.append("\n".join(macros))
        return "\n\n".join(output)


class VariableSectiondefNode(Node):
    def to_details_asciidoc(self, depth=0, **kwargs):
        memberdefs = self.children("memberdef", kind="variable")
        if not memberdefs:
            return ""

        output = [title("Variable Documentation", depth)]
        variables = []
        for memberdef in memberdefs:
            variables.append(memberdef.to_asciidoc(**kwargs, depth=depth + 1))
        output.append("\n".join(variables))
        return "\n\n".join(output)

    def to_asciidoc(self, depth=0, **kwargs):
        output = [title("Variables", depth)]
        variables = []
        for memberdef in self.children("memberdef", kind="variable"):
            variable = ["`"]
            variable.append(memberdef.child("type").to_asciidoc(**kwargs, depth=depth))
            variable.append(
                f" <<{memberdef.id},{escape_text(memberdef.text('name'))}>>"
            )
            argsstring = memberdef.text("argsstring")
            if argsstring:
                variable.append(argsstring)
            variable.append("`:: ")
            briefdescription = memberdef.child("briefdescription").to_asciidoc(
                **kwargs, depth=depth
            )
            if briefdescription:
                variable.append(briefdescription)
            else:
                variable.append("{empty}")
            variables.append("".join(variable))
        output.append("\n".join(variables))
        return "\n\n".join(output)


class UserDefinedSectiondefNode(Node):
    def to_asciidoc(self, depth=0, **kwargs):
        output = []
        header = self.text("header")
        if header:
            output.append(title(header, depth))
        description = self.child("description")
        if description:
            output.append(description.to_asciidoc(**kwargs, depth=depth))
        members = []
        for memberdef in self.children("memberdef"):
            members.append(memberdef.to_asciidoc(**kwargs, depth=depth + 1))
        output.append("\n".join(members))
        return "\n\n".join(output)
