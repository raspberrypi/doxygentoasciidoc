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
        "title",
        "verbatim",
    )

    def __init__(self, node, position=0, xmldir=None):
        self.node = node
        self.position = position
        self.xmldir = xmldir

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

                stripped = re.sub(
                    r"\s{2,}",
                    " ",
                    re.sub(r"\s+\n\s+", "\n", escape_text(self.node)).replace(
                        "\n", " "
                    ),
                )
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
            para = None
            children = self.node.contents[:]
            for child in children:
                if child.name not in self.BLOCK_LEVEL_NODES:
                    # Move inline elements into a new block
                    if para:
                        # If there is already a wrapper, append this to it
                        para.append(child)
                    else:
                        # If there isn't already a wrapper, make one
                        para = child.wrap(self.soup().new_tag("para"))
                elif para and para.get_text(strip=True):
                    # If there is a wrapper and it isn't empty, prepend it before this block
                    child.insert_before(para)
                    para = None
            if para:
                # Append any remaining lifted inline elements at the end
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
        """Return a generator of the AsciiDoc contents of this node."""
        return (child.to_asciidoc(**kwargs) for child in self.children())

    def children(self):
        """Return a generator of the child Nodes of this node."""
        return (
            self.mapping()[child.name](child, position=position, xmldir=self.xmldir)
            for position, child in enumerate(self.node.children)
        )

    @property
    def previous_node(self):
        """Return the previous sibling element to this Node, skipping text nodes."""
        return next((node for node in self.node.previous_siblings if node.name), None)

    @property
    def next_node(self):
        """Return the next sibling element to this Node, skipping text nodes."""
        return next((node for node in self.node.next_siblings if node.name), None)

    def mapping(self):
        """Return a mapping of element names to Node subclasses."""
        return {
            "bold": BoldNode,
            "codeline": CodelineNode,
            "computeroutput": ComputeroutputNode,
            "emphasis": EmphasisNode,
            "entry": EntryNode,
            "highlight": Node,
            "itemizedlist": ItemizedlistNode,
            "listitem": ListitemNode,
            "mdash": MdashNode,
            "ndash": NdashNode,
            "nonbreakablespace": NonbreakablespaceNode,
            "orderedlist": OrderedlistNode,
            "para": Node,
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
            "title": TitleNode,
            "ulink": UlinkNode,
            "verbatim": VerbatimNode,
            None: Node,
        }


class DoxygenindexNode(Node):
    """Return the AsciiDoc representation from a root Doxygen doxygenindex node."""

    def to_asciidoc(self, **kwargs):
        output = []
        for module in self.rootmodules():
            output.append(
                "\n".join(
                    (
                        f"[[{sanitize(module.refid)},{escape_text(module.node.title)}]]",
                        title(module.node.title, 2),
                    )
                )
            )
            briefdescription = module.node.briefdescription
            if briefdescription:
                output.append(briefdescription)
            table = ['[cols="1,4"]', "|==="]
            for child in module.children:
                table.append(child.to_asciidoc_row())
            table.append("|===")
            if len(table) > 3:
                output.append("\n".join(table))
            detaileddescription = module.node.detaileddescription
            if detaileddescription:
                output.append(detaileddescription)
            for child in module.children:
                output.append(child.to_asciidoc(**kwargs))
        output.append(
            "\n".join(
                (
                    "[#datastructures]",
                    title("Data Structures", 2),
                )
            )
        )
        for datastructure in self.datastructures():
            output.append(datastructure.to_asciidoc(**kwargs))
        return "\n\n".join(output)

    def rootmodules(self):
        """Return a list of root modules from the Doxygen index.

        Traverse the full list of modules from the Doxygen index, building up a
        hierarchy in memory before returning only the root nodes."""
        groups = {}

        for compound in self.node("compound", kind="group", recursive=False):
            with open(
                f'{self.xmldir}/{compound["refid"]}.xml', encoding="utf-8"
            ) as compoundxml:
                doxygenroot = BeautifulSoup(compoundxml, "xml").doxygen
            for compounddef in doxygenroot(
                "compounddef", kind="group", recursive=False
            ):
                group = groups.setdefault(
                    compounddef["id"], self.Group(compounddef["id"])
                )
                group.node = GroupNode(compounddef, xmldir=self.xmldir)

                for innergroup in compounddef("innergroup", recursive=False):
                    child = groups.setdefault(
                        innergroup["refid"], self.Group(innergroup["refid"])
                    )
                    child.parent = group
                    group.children.append(child)

        return (group for (refid, group) in groups.items() if group.isroot())

    def datastructures(self):
        """Return a list of data structures from the Doxygen index."""
        datastructures = []
        for compound in self.node("compound", kind="struct", recursive=False):
            with open(
                f'{self.xmldir}/{compound["refid"]}.xml', encoding="utf-8"
            ) as compoundxml:
                doxygenroot = BeautifulSoup(compoundxml, "xml").doxygen
            for compounddef in doxygenroot(
                "compounddef", kind="struct", recursive=False
            ):
                datastructures.append(
                    DataStructureNode(compounddef, xmldir=self.xmldir)
                )
        return datastructures

    class Group:
        """An inner class to represent the full hierarchy of modules."""

        def __init__(self, refid):
            self.refid = refid
            self.parent = None
            self.children = []
            self.node = None

        def isroot(self):
            return self.parent is None

        def to_asciidoc(self, **kwargs):
            output = [self.node.to_asciidoc(**kwargs)]
            for child in self.children:
                kwargs["depth"] = kwargs.get("depth", 0) + 1
                output.append(child.to_asciidoc(**kwargs))
            return "\n\n".join(output)

        def to_asciidoc_row(self, depth=0):
            indent = "{nbsp}" * 4 * depth
            briefdescription = self.node.briefdescription
            output = []
            row = (
                f"|{indent}<<{sanitize(self.refid)},{escape_text(self.node.title)}>>",
                f"|{briefdescription}",
            )
            output.append("\n".join(row))
            for child in self.children:
                output.append(child.to_asciidoc_row(depth=depth + 1))
            return "\n\n".join(output)


class GroupNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [self.__output_title(**kwargs)]
        briefdescription = self.__output_briefdescription(**kwargs)
        if briefdescription:
            output.append(briefdescription)
        modules = self.__list_modules(**kwargs)
        if modules:
            output.append(modules)
        data_structures = self.__list_data_structures(**kwargs)
        if data_structures:
            output.append(data_structures)
        macros = self.__list_macros(**kwargs)
        if macros:
            output.append(macros)
        typedefs = self.__list_typedefs(**kwargs)
        if typedefs:
            output.append(typedefs)
        enums = self.__list_enums(**kwargs)
        if enums:
            output.append(enums)
        functions = self.__list_functions(**kwargs)
        if functions:
            output.append(functions)
        variables = self.__list_variables(**kwargs)
        if variables:
            output.append(variables)
        detaileddescription = self.__output_detaileddescription(**kwargs)
        if detaileddescription:
            output.append(detaileddescription)
        macrodetails = self.__list_macro_details(**kwargs)
        if macrodetails:
            output.append(macrodetails)
        typedefdetails = self.__list_typedef_details(**kwargs)
        if typedefdetails:
            output.append(typedefdetails)
        enumdetails = self.__list_enum_details(**kwargs)
        if enumdetails:
            output.append(enumdetails)
        functiondetails = self.__list_function_details(**kwargs)
        if functiondetails:
            output.append(functiondetails)
        variabledetails = self.__list_variable_details(**kwargs)
        if variabledetails:
            output.append(variabledetails)
        return "\n\n".join(output)

    def __output_title(self, **kwargs):
        return "\n".join(
            (
                f"[[{self.sanitized_id},{self.title}]]",
                title(self.title, 3 + kwargs.get("depth", 0)),
            )
        )

    def __output_briefdescription(self, **kwargs):
        kwargs["depth"] = 2 + kwargs.get("depth", 0)
        return Node(self.node.find("briefdescription", recursive=False)).to_asciidoc(
            **kwargs
        )

    def __output_detaileddescription(self, **kwargs):
        kwargs["depth"] = 2 + kwargs.get("depth", 0)
        return DetaileddescriptionNode(
            self.node.find("detaileddescription", recursive=False)
        ).to_asciidoc(**kwargs)

    def __list_modules(self, **kwargs):
        innergroups = self.node("innergroup", recursive=False)
        if not innergroups:
            return ""

        output = [title("Modules", 4 + kwargs.get("depth", 0))]
        modules = []
        for innergroup in innergroups:
            modules.append(
                InnergroupNode(innergroup, xmldir=self.xmldir).to_asciidoc(**kwargs)
            )
        output.append("\n".join(modules))
        return "\n\n".join(output)

    def __list_data_structures(self, **kwargs):
        innerclasses = self.node("innerclass", recursive=False)
        if not innerclasses:
            return ""

        output = [title("Data Structures", 4 + kwargs.get("depth", 0))]
        datastructures = []
        for innerclass in innerclasses:
            datastructures.append(
                InnerclassNode(innerclass, xmldir=self.xmldir).to_asciidoc(**kwargs)
            )
        output.append("\n".join(datastructures))
        return "\n\n".join(output)

    def __list_macros(self, **kwargs):
        output = []
        for sectiondef in self.node("sectiondef", kind="define", recursive=False):
            output.append(
                DefineSectiondefNode(sectiondef, xmldir=self.xmldir).to_asciidoc(
                    **kwargs
                )
            )
        return "\n\n".join(output)

    def __list_enums(self, **kwargs):
        output = []
        for sectiondef in self.node("sectiondef", kind="enum", recursive=False):
            output.append(
                EnumSectiondefNode(sectiondef, xmldir=self.xmldir).to_asciidoc(**kwargs)
            )
        return "\n\n".join(output)

    def __list_typedefs(self, **kwargs):
        output = []
        for sectiondef in self.node("sectiondef", kind="typedef", recursive=False):
            output.append(
                TypedefSectiondefNode(sectiondef, xmldir=self.xmldir).to_asciidoc(
                    **kwargs
                )
            )
        return "\n\n".join(output)

    def __list_variables(self, **kwargs):
        memberdefs = self.node("memberdef", kind="variable")
        if not memberdefs:
            return ""

        output = [title("Variables", 4 + kwargs.get("depth", 0))]
        variables = []
        for memberdef in memberdefs:
            variable = ["`"]
            variable.append(
                Node(
                    memberdef.find("type", recursive=False), xmldir=self.xmldir
                ).to_asciidoc(**kwargs)
            )
            variable.append(
                f" <<{sanitize(memberdef['id'])},{escape_text(memberdef.find('name', recursive=False).get_text(strip=True))}>>`:: "
            )
            briefdescription = Node(
                memberdef.briefdescription, xmldir=self.xmldir
            ).to_asciidoc(**kwargs)
            if briefdescription:
                variable.append(briefdescription)
            else:
                variable.append("{empty}")
            variables.append("".join(variable))
        output.append("\n".join(variables))
        return "\n\n".join(output)

    def __list_functions(self, **kwargs):
        output = []
        for sectiondef in self.node("sectiondef", kind="func", recursive=False):
            output.append(
                FunctionSectiondefNode(sectiondef, xmldir=self.xmldir).to_asciidoc(
                    **kwargs
                )
            )
        return "\n\n".join(output)

    def __list_typedef_details(self, **kwargs):
        memberdefs = self.node("memberdef", kind="typedef")
        if not memberdefs:
            return ""
        output = [title("Typedef Documentation", 4 + kwargs.get("depth", 0))]
        typedefs = []
        for memberdef in memberdefs:
            typedefs.append(
                TypedefMemberdefNode(memberdef, xmldir=self.xmldir).to_asciidoc(
                    **kwargs
                )
            )
        output.append("\n".join(typedefs))
        return "\n\n".join(output)

    def __list_function_details(self, **kwargs):
        memberdefs = self.node("memberdef", kind="function")
        if not memberdefs:
            return ""

        output = [title("Function Documentation", 4 + kwargs.get("depth", 0))]
        functions = []
        for memberdef in sorted(
            memberdefs,
            key=lambda memberdef: memberdef.find("name", recursive=False).get_text(
                strip=True
            ),
        ):
            functions.append(
                FunctionMemberdefNode(memberdef, xmldir=self.xmldir).to_asciidoc(
                    **kwargs
                )
            )
        output.append("\n\n".join(functions))
        return "\n\n".join(output)

    def __list_enum_details(self, **kwargs):
        memberdefs = self.node("memberdef", kind="enum")
        if not memberdefs:
            return ""

        output = [title("Enumeration Type Documentation", 4 + kwargs.get("depth", 0))]
        enums = []
        for memberdef in memberdefs:
            enums.append(
                EnumMemberdefNode(memberdef, xmldir=self.xmldir).to_asciidoc(**kwargs)
            )
        output.append("\n".join(enums))
        return "\n\n".join(output)

    def __list_variable_details(self, **kwargs):
        memberdefs = self.node("memberdef", kind="variable")
        if not memberdefs:
            return ""

        output = [title("Variable Documentation", 4 + kwargs.get("depth", 0))]
        variables = []
        for memberdef in memberdefs:
            variables.append(
                VariableMemberdefNode(memberdef, xmldir=self.xmldir).to_asciidoc(
                    **kwargs
                )
            )
        output.append("\n".join(variables))
        return "\n\n".join(output)

    def __list_macro_details(self, **kwargs):
        memberdefs = self.node("memberdef", kind="define")
        if not memberdefs:
            return ""

        output = [title("Macro Definition Documentation", 4 + kwargs.get("depth", 0))]
        macros = []
        for memberdef in memberdefs:
            macros.append(
                DefineMemberdefNode(memberdef, xmldir=self.xmldir).to_asciidoc(**kwargs)
            )
        output.append("\n".join(macros))
        return "\n\n".join(output)

    @property
    def briefdescription(self):
        return Node(
            self.node.find("briefdescription", recursive=False), xmldir=self.xmldir
        ).to_asciidoc()

    @property
    def detaileddescription(self):
        return Node(
            self.node.find("detaileddescription", recursive=False), xmldir=self.xmldir
        ).to_asciidoc()

    @property
    def sanitized_id(self):
        return sanitize(self.node["id"])

    @property
    def title(self):
        return self.node.find("title", recursive=False).get_text(strip=True)


class DataStructureNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [
            "\n".join(
                (
                    f"[#{sanitize(self.node['id'])}]",
                    title(
                        self.node.find("compoundname", recursive=False).get_text(
                            strip=True
                        ),
                        3 + kwargs.get("depth", 0),
                    ),
                )
            )
        ]
        briefdescription = Node(
            self.node.find("briefdescription", recursive=False),
            xmldir=self.xmldir,
        ).to_asciidoc()
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = Node(
            self.node.find("detaileddescription", recursive=False),
            xmldir=self.xmldir,
        ).to_asciidoc()
        if detaileddescription:
            output.append(detaileddescription)
        memberdefs = self.node("memberdef", kind="variable")
        if memberdefs:
            output.append(title("Variable Documentation", 4 + kwargs.get("depth", 0)))
            variables = []
            for memberdef in memberdefs:
                variables.append(
                    VariableMemberdefNode(memberdef, xmldir=self.xmldir).to_asciidoc(
                        **kwargs
                    )
                )
            output.append("\n\n".join(variables))
        return "\n\n".join(output)


class InnergroupNode(Node):
    def to_asciidoc(self, **kwargs):
        with open(
            f"{self.xmldir}/{self.node['refid']}.xml", encoding="utf-8"
        ) as compoundxml:
            compounddef = BeautifulSoup(compoundxml, "xml").compounddef
            output = [
                f"<<{sanitize(compounddef['id'])},{escape_text(compounddef.find('title', recursive=False).get_text(strip=True))}>>::"
            ]
            briefdescription = Node(
                compounddef.find("briefdescription", recursive=False),
                xmldir=self.xmldir,
            ).to_asciidoc(**kwargs)
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
            compounddef = BeautifulSoup(compoundxml, "xml").compounddef
            output = [
                f"struct <<{sanitize(compounddef['id'])},{escape_text(compounddef.find('compoundname', recursive=False).get_text(strip=True))}>>::"
            ]
            briefdescription = Node(
                compounddef.find("briefdescription", recursive=False),
                xmldir=self.xmldir,
            ).to_asciidoc(**kwargs)
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
        for codeline in self.node("codeline", recursive=False):
            output.append(
                CodelineNode(codeline, xmldir=self.xmldir).to_asciidoc(**kwargs)
            )
        output.append("----")
        return "\n".join(output)


class VerbatimNode(Node):
    def to_asciidoc(self, **kwargs):
        kwargs["programlisting"] = True
        return "".join(("[source,c]\n----\n", super().to_asciidoc(**kwargs), "----"))


class CodelineNode(Node):
    def to_asciidoc(self, **kwargs):
        kwargs["programlisting"] = True
        return super().to_asciidoc(**kwargs)


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
        return "".join((f"{self.node['url']}[", super().to_asciidoc(**kwargs), "]"))


class NonbreakablespaceNode(Node):
    def to_asciidoc(self, **kwargs):
        return "{nbsp}"


class SectNode(Node):
    def to_asciidoc(self, **kwargs):
        return "\n".join(
            (f"[#{sanitize(self.node['id'])}]", super().to_asciidoc(**kwargs))
        )


class TitleNode(Node):
    def to_asciidoc(self, **kwargs):
        return "".join((".", super().to_asciidoc(**kwargs)))


class SimplesectNode(Node):
    def to_asciidoc(self, **kwargs):
        if self.node["kind"] == "see":
            output = []
            if not (
                self.previous_node
                and self.previous_node.name == "simplesect"
                and self.previous_node["kind"] == "see"
            ):
                output.append("--\n*See also*\n\n")
            output.append(super().to_asciidoc(**kwargs))
            if not (
                self.next_node
                and self.next_node.name == "simplesect"
                and self.next_node["kind"] == "see"
            ):
                output.append("\n--")
            return "".join(output)

        if self.node["kind"] == "return":
            return "".join(("--\n*Returns*\n\n", super().to_asciidoc(**kwargs), "\n--"))

        if self.node["kind"] == "note":
            output = []
            if not (
                self.previous_node
                and self.previous_node.name == "simplesect"
                and self.previous_node["kind"] == "note"
            ):
                output.append("[NOTE]\n====\n")
            output.append(super().to_asciidoc(**kwargs))
            if not (
                self.next_node
                and self.next_node.name == "simplesect"
                and self.next_node["kind"] == "note"
            ):
                output.append("\n====")

            return "".join(output)

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
        return f"`{escape_text(self.node.parametername.get_text(strip=True))}`::"


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

        return f"<<{self.refid},{self.node.string}>>"

    @property
    def refid(self):
        return sanitize(self.node["refid"])


class EmphasisNode(Node):
    def to_asciidoc(self, **kwargs):
        return "".join(("_", super().to_asciidoc(**kwargs), "_"))


class BoldNode(Node):
    def to_asciidoc(self, **kwargs):
        return "".join(("*", super().to_asciidoc(**kwargs), "*"))


class ComputeroutputNode(Node):
    def to_asciidoc(self, **kwargs):
        return "".join(("`", super().to_asciidoc(**kwargs), "`"))


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


class TableNode(Node):
    def to_asciidoc(self, **kwargs):
        return "".join(("|===\n", super().to_asciidoc(**kwargs), "\n|==="))


class RowNode(Node):
    def block_separator(self, **_kwargs):
        if self.position == 0:
            return " "
        return "\n"


class EntryNode(Node):
    def to_asciidoc(self, **kwargs):
        return "".join(("|", super().to_asciidoc(**kwargs)))


class DetaileddescriptionNode(Node):
    def to_asciidoc(self, **kwargs):
        output = []
        contents = super().to_asciidoc(**kwargs)
        if contents:
            if not kwargs.get("documentation", False):
                output.append(title("Detailed Description", 2 + kwargs.get("depth", 0)))
            output.append(contents)
            return "\n\n".join(output)
        return ""


class FunctionMemberdefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [
            "\n".join(
                (
                    f"[#{sanitize(self.node['id'])}]",
                    title(
                        self.node.find("name", recursive=False).string,
                        5 + kwargs.get("depth", 0),
                    ),
                )
            )
        ]
        if self.node["static"] == "yes":
            definition = ["`static "]
        else:
            definition = ["`"]
        definition.append(
            Node(
                self.node.find("type", recursive=False), xmldir=self.xmldir
            ).to_asciidoc(**kwargs)
        )
        definition.append(
            f" {self.node.find('name', recursive=False).get_text(strip=True)} "
        )
        if self.node.find("argsstring", recursive=False) is not None:
            definition.append(
                escape_text(
                    self.node.find("argsstring", recursive=False).get_text(strip=True)
                ).replace(",", ", +\n{nbsp}{nbsp}{nbsp}{nbsp}{nbsp}{nbsp}")
            )
        definition.append("`")
        output.append("".join(definition))
        kwargs["depth"] = 5 + kwargs.get("depth", 0)
        kwargs["documentation"] = True
        briefdescription = Node(
            self.node.briefdescription, xmldir=self.xmldir
        ).to_asciidoc(**kwargs)
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = DetaileddescriptionNode(
            self.node.detaileddescription, xmldir=self.xmldir
        ).to_asciidoc(**kwargs)
        if detaileddescription:
            output.append(detaileddescription)
        return "\n\n".join(output)


class TypedefMemberdefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [
            "\n".join(
                (
                    f"[#{sanitize(self.node['id'])}]",
                    title(
                        self.node.find("name", recursive=False).string,
                        5 + kwargs.get("depth", 0),
                    ),
                )
            )
        ]
        output.append(f"`{escape_text(self.node.definition.get_text(strip=True))}`")
        kwargs["depth"] = 5 + kwargs.get("depth", 0)
        kwargs["documentation"] = True
        briefdescription = Node(
            self.node.briefdescription, xmldir=self.xmldir
        ).to_asciidoc(**kwargs)
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = DetaileddescriptionNode(
            self.node.detaileddescription, xmldir=self.xmldir
        ).to_asciidoc(**kwargs)
        if detaileddescription:
            output.append(detaileddescription)
        return "\n\n".join(output)


class EnumMemberdefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [
            "\n".join(
                (
                    f"[#{sanitize(self.node['id'])}]",
                    title(
                        self.node.find("name", recursive=False).string,
                        5 + kwargs.get("depth", 0),
                    ),
                )
            )
        ]
        output.append(
            f"`enum {escape_text(self.node.find('name', recursive=False).get_text(strip=True))}`"
        )
        kwargs["depth"] = 5 + kwargs.get("depth", 0)
        kwargs["documentation"] = True
        briefdescription = Node(
            self.node.find("briefdescription", recursive=False), xmldir=self.xmldir
        ).to_asciidoc(**kwargs)
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = DetaileddescriptionNode(
            self.node.find("detaileddescription", recursive=False), xmldir=self.xmldir
        ).to_asciidoc(**kwargs)
        if detaileddescription:
            output.append(detaileddescription)

        enumvalues_with_descriptions = self.node(
            lambda tag: tag.name == "enumvalue"
            and tag.briefdescription.get_text(strip=True),
            recursive=False,
        )
        if enumvalues_with_descriptions:
            table = [".Enumerator"]
            table.append('[cols="h,1"]')
            table.append("|===")
            rows = []
            for enumvalue in enumvalues_with_descriptions:
                row = [
                    f"|[[{sanitize(enumvalue['id'])}]]{enumvalue.find('name', recursive=False).string}"
                ]
                briefdescription = Node(
                    enumvalue.briefdescription, xmldir=self.xmldir
                ).to_asciidoc(**kwargs)
                row.append(f"|{briefdescription}")
                rows.append("\n".join(row))
            table.append("\n\n".join(rows))
            table.append("|===")
            output.append("\n".join(table))
        return "\n\n".join(output)


class VariableMemberdefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [
            "\n".join(
                (
                    f"[#{sanitize(self.node['id'])}]",
                    title(
                        self.node.find("name", recursive=False).string,
                        5 + kwargs.get("depth", 0),
                    ),
                )
            )
        ]
        output.append(f"`{escape_text(self.node.definition.get_text(strip=True))}`")
        kwargs["depth"] = 5 + kwargs.get("depth", 0)
        kwargs["documentation"] = True
        output.append(
            Node(self.node.briefdescription, xmldir=self.xmldir).to_asciidoc(**kwargs)
        )
        output.append(
            DetaileddescriptionNode(
                self.node.detaileddescription, xmldir=self.xmldir
            ).to_asciidoc(**kwargs)
        )
        return "\n\n".join(filter(None, output))


class DefineMemberdefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [
            "\n".join(
                (
                    f"[#{sanitize(self.node['id'])}]",
                    title(
                        self.node.find("name", recursive=False).string,
                        5 + kwargs.get("depth", 0),
                    ),
                )
            )
        ]
        macro = [
            f"`#define {escape_text(self.node.find('name', recursive=False).get_text(strip=True))}"
        ]
        if self.node.initializer:
            macro.append(f" {escape_text(self.node.initializer.get_text(strip=True))}`")
        else:
            macro.append("`")
        output.append("".join(macro))
        kwargs["depth"] = 5 + kwargs.get("depth", 0)
        kwargs["documentation"] = True
        briefdescription = Node(
            self.node.briefdescription, xmldir=self.xmldir
        ).to_asciidoc(**kwargs)
        if briefdescription:
            output.append(briefdescription)
        detaileddescription = DetaileddescriptionNode(
            self.node.detaileddescription, xmldir=self.xmldir
        ).to_asciidoc(**kwargs)
        if detaileddescription:
            output.append(detaileddescription)
        return "\n\n".join(output)


class FunctionSectiondefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [title("Functions", 4 + kwargs.get("depth", 0))]
        functions = []
        for memberdef in self.node("memberdef", kind="function"):
            if memberdef["static"] == "yes":
                function = ["`static "]
            else:
                function = ["`"]
            function.append(
                Node(
                    memberdef.find("type", recursive=False), xmldir=self.xmldir
                ).to_asciidoc(**kwargs)
            )
            function.append(
                f" <<{sanitize(memberdef['id'])},{escape_text(memberdef.find('name', recursive=False).get_text(strip=True))}>> "
            )
            function.append(
                f"{escape_text(memberdef.find('argsstring', recursive=False).get_text(strip=True))}`:: "
            )
            briefdescription = Node(
                memberdef.briefdescription, xmldir=self.xmldir
            ).to_asciidoc(**kwargs)
            if briefdescription:
                function.append(briefdescription)
            else:
                function.append("{empty}")
            functions.append("".join(function))
        output.append("\n".join(functions))
        return "\n\n".join(output)


class TypedefSectiondefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [title("Typedefs", 4 + kwargs.get("depth", 0))]
        typedefs = []
        for memberdef in self.node("memberdef", kind="typedef"):
            typedef = [
                f"`typedef {escape_text(memberdef.find('type', recursive=False).get_text(strip=True))} <<{sanitize(memberdef['id'])},{escape_text(memberdef.find('name', recursive=False).get_text(strip=True))}>>{escape_text(memberdef.find('argsstring', recursive=False).get_text(strip=True))}`::"
            ]
            briefdescription = Node(
                memberdef.briefdescription, xmldir=self.xmldir
            ).to_asciidoc(**kwargs)
            if briefdescription:
                typedef.append(briefdescription)
            else:
                typedef.append("{empty}")
            typedefs.append(" ".join(typedef))
        output.append("\n".join(typedefs))
        return "\n\n".join(output)


class EnumSectiondefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [title("Enumerations", 4 + kwargs.get("depth", 0))]
        enums = []
        for memberdef in self.node("memberdef", kind="enum"):
            enum = [
                f"`enum <<{sanitize(memberdef['id'])},{escape_text(memberdef.find('name', recursive=False).get_text(strip=True))}>>",
                " { ",
            ]
            enumvalues = []
            for enumvalue in memberdef("enumvalue", recursive=False):
                if enumvalue.briefdescription.get_text(strip=True):
                    value = [
                        f"<<{sanitize(enumvalue['id'])},{escape_text(enumvalue.find('name', recursive=False).get_text(strip=True))}>>"
                    ]
                else:
                    value = [
                        escape_text(
                            enumvalue.find("name", recursive=False).get_text(strip=True)
                        )
                    ]
                if enumvalue.initializer:
                    value.append(
                        escape_text(enumvalue.initializer.get_text(strip=True))
                    )
                enumvalues.append(" ".join(value))
            enum.append(", ".join(enumvalues))
            enum.append(" }`:: ")
            briefdescription = Node(
                memberdef.find("briefdescription", recursive=False), xmldir=self.xmldir
            ).to_asciidoc(**kwargs)

            if briefdescription:
                enum.append(briefdescription)
            else:
                enum.append("{empty}")
            enums.append("".join(enum))
        output.append("\n".join(enums))
        return "\n\n".join(output)


class DefineSectiondefNode(Node):
    def to_asciidoc(self, **kwargs):
        output = [title("Macros", 4 + kwargs.get("depth", 0))]
        macros = []
        for memberdef in self.node("memberdef", kind="define"):
            macro = [
                f"* `#define <<{sanitize(memberdef['id'])},{escape_text(memberdef.find('name', recursive=False).get_text(strip=True))}>>"
            ]
            if memberdef.initializer:
                macro.append(
                    f" {escape_text(memberdef.find('initializer', recursive=False).get_text(strip=True))}`"
                )
            else:
                macro.append("`")
            macros.append("".join(macro))
        output.append("\n".join(macros))
        return "\n\n".join(output)
