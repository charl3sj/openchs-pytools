header = """
const {RuleFactory, FormElementsStatusHelper, StatusBuilderAnnotationFactory, complicationsBuilder} = require('rules-config/rules');
const WithStatusBuilder = StatusBuilderAnnotationFactory('programEncounter', 'formElement');
const RuleHelper = require('../RuleHelper');
const ObservationMatcherAnnotationFactory = require('../ObservationMatcherAnnotationFactory');
const CodedObservationMatcher = ObservationMatcherAnnotationFactory(RuleHelper.Scope.Encounter, 'containsAnyAnswerConceptName')(['programEncounter', 'formElement']);
"""


def declare_rule(filter_name, form_uuid):
    return f"""
const {filter_name}Filter = RuleFactory("{form_uuid}", 'ViewFilter');
"""


def define_class(filter_name, filter_uuid):
    return f"""
@{filter_name}Filter('{filter_uuid}', '<description>', 100.0)
class {filter_name}FilterHandler {{
    static exec(programEncounter, formElementGroup, today) {{
        return FormElementsStatusHelper
            .getFormElementsStatusesWithoutDefaults(
                new {filter_name}FilterHandler(),
                programEncounter,
                formElementGroup,
                today
            );
    }}

"""


def close_class():
    return """
}
"""


def lodash_camel_case(line):
    line = line.strip()
    for char in "`~!@#$%^&*-_+()[]{}:;'\",.<>?|\\/":
        line = line.replace(char, ' ')
    words = line.split(' ')
    return ''.join([words[0].lower(), *[x.capitalize() for x in words[1:]]])


def define_method(method_name):
    return f"""
    @WithStatusBuilder
    @CodedObservationMatcher()
    {lodash_camel_case(method_name)}([programEncounter, formElement], statusBuilder) {{
        statusBuilder.show()
    }}    
"""
