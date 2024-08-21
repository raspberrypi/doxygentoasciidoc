from doxygentoasciidoc.helpers import escape_text, sanitize, title


def test_escape_text_escapes_words_starting_with_double_underscore():
    assert escape_text("foo __bar baz") == "foo ++__bar++ baz"


def test_escape_text_escapes_literal_asterisks():
    assert escape_text("* foo * bar") == "++*++ foo ++*++ bar"


def test_escape_text_strips_line_continuation_characters():
    assert escape_text(" \\\n") == " "


def test_escape_text_accepts_non_strings():
    assert escape_text(123) == "123"


def test_escape_text_escapes_double_parentheses():
    assert escape_text("((hello))") == "\\((hello))"


def test_escape_text_does_not_escape_unbalanced_double_parentheses():
    assert escape_text("((hello)-1)") == "((hello)-1)"


def test_escape_text_escapes_arrows():
    assert escape_text("->") == "\\->"


def test_sanitize_replaces_multiple_leading_underscores():
    assert sanitize("___foo__bar") == "_foo_bar"


def test_title_with_level_0():
    assert title("Level 0 Section Title", 0) == "= Level 0 Section Title"


def test_title_with_level_1():
    assert title("Level 1 Section Title", 1) == "== Level 1 Section Title"


def test_title_with_level_2():
    assert title("Level 2 Section Title", 2) == "=== Level 2 Section Title"


def test_title_with_level_3():
    assert title("Level 3 Section Title", 3) == "==== Level 3 Section Title"


def test_title_with_level_4():
    assert title("Level 4 Section Title", 4) == "===== Level 4 Section Title"


def test_title_with_level_5():
    assert title("Level 5 Section Title", 5) == "====== Level 5 Section Title"


def test_title_with_level_6():
    assert title("Level 6 Section Title", 6) == "[role=h6]\n*Level 6 Section Title*"


def test_title_with_level_7():
    assert title("Level 7 Section Title", 7) == "[role=h6]\n*Level 7 Section Title*"


def test_title_escapes_text():
    assert title("3 * 2 = 6", 1) == "== 3 ++*++ 2 = 6"


def test_title_escapes_text_with_level_6():
    assert title("3 * 2 = 6", 6) == "[role=h6]\n*3 ++*++ 2 = 6*"


def test_title_with_id():
    assert (
        title("Title", 1, attributes={"id": "group__foo"}) == "[#group_foo]\n== Title"
    )


def test_title_with_role():
    assert (
        title("Title", 1, attributes={"role": "contextspecific"})
        == "[role=contextspecific]\n== Title"
    )


def test_title_with_level_6_and_role():
    assert (
        title("Title", 6, attributes={"role": "contextspecific"})
        == "[role=h6 contextspecific]\n*Title*"
    )


def test_title_with_tag_and_type():
    assert (
        title("Title", 1, attributes={"type": "TYPE", "tag": "TAG"})
        == "[tag=TAG,type=TYPE]\n== Title"
    )


def test_title_with_all_attributes():
    assert (
        title(
            "Title",
            1,
            attributes={
                "id": "group__foo",
                "role": "contextspecific",
                "tag": "TAG",
                "type": "TYPE",
            },
        )
        == "[#group_foo,role=contextspecific,tag=TAG,type=TYPE]\n== Title"
    )


def test_title_with_level_6_and_all_attributes():
    assert (
        title(
            "Title",
            6,
            attributes={
                "id": "group__foo",
                "role": "contextspecific",
                "tag": "TAG",
                "type": "TYPE",
            },
        )
        == "[#group_foo,role=h6 contextspecific,tag=TAG,type=TYPE]\n*Title*"
    )


def test_title_with_arbitrary_attributes():
    assert (
        title(
            "Title",
            1,
            attributes={
                "foo": "bar",
                "baz": "quux",
            },
        )
        == '[foo="bar",baz="quux"]\n== Title'
    )


def test_title_with_attribute_with_space():
    assert (
        title(
            "Title",
            1,
            attributes={
                "foo": "bar baz",
            },
        )
        == '[foo="bar baz"]\n== Title'
    )
