from behave import *

@given('we open Tommy Hilfiger Netherlands website')
def step_impl(context):
    pass

@when('we point at the logo')
def step_impl(context):
    assert True

@then('the logo will be displayed')
def step_impl(context):
    assert context.failed is False