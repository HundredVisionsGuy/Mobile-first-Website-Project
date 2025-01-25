"""
Test CSS Requirements.
"""
import pytest
from webcode_tk import cascade_tools as cascade
from webcode_tk import css_tools as css
from webcode_tk import validator_tools as validator

project_dir = "project/"

css_validation_results = validator.get_project_validation(
    project_dir, "css"
)


style_attributes_in_project = css.no_style_attributes_allowed_report(
    project_dir)
css_validation_results = validator.get_project_validation(
    project_dir, "css"
)

color_contrast_results = []
color_contrast_results = cascade.get_color_contrast_report(project_dir)

applying_styles_results = css.styles_applied_report(project_dir)
font_data = css.fonts_applied_report(project_dir)
header_color_rule_data = css.get_heading_color_report(project_dir)


@pytest.mark.parametrize("results", style_attributes_in_project)
def test_css_for_no_style_attributes(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results", css_validation_results)
def test_css_validation(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results", applying_styles_results)
def test_if_file_applies_styles(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results",
                         color_contrast_results)
def test_color_contrast(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results", font_data)
def test_font_requirements(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results", header_color_rule_data)
def test_for_colors_applied_to_headings(results):
    assert "pass" == results[:4]


@pytest.fixture
def styles_by_files():
    styles = css.get_styles_by_html_files(project_dir)
    return styles


applied_properties_goals = {
        "figure": {
            "properties": ("padding", "border", "background-color"),
        }
    }

applied_properties_report = css.get_properties_applied_report(
    project_dir,
    applied_properties_goals)


@pytest.mark.parametrize("results", applied_properties_report)
def test_figure_styles_applied(results):
    assert "fail:" not in results[:5]


def test_for_breakpoints(styles_by_files):
    # at least one break point per file
    expected_num = len(styles_by_files)
    breakpoints = 0
    for styles in styles_by_files:
        for stylesheet in styles.get("stylesheets"):
            at_rules = css.get_all_at_rules(stylesheet)
            if at_rules:
                for at_rule in at_rules:
                    rule = at_rule[1].get("at_rule")
                    if "@media screen" in rule:
                        breakpoints += 1
    assert expected_num >= breakpoints
