import os


class TestResult(object):
    """
    This class handles test result.
    """
    def __init__(self, score=None, pass_score=None, inspect_only=False):
        self.score = score
        self.passed = pass_score
        self.inspect_only = bool(inspect_only)

    def validate(self):
        try:
            if (self.score is not None) and (self.passed is not None):
                if self.score > self.passed:
                    return "passed"
                else:
                    return "failed"
            else:
                if self.inspect_only:
                    return "inspection"
        except Exception as ex:
            print("arguments : {0}".format(
                [self.score, self.passed, self.inspect_only]))
            print(ex)


class BaseValidationTest(object):

    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def __init__(self, *kwargs):
        pass

    def run(catalog_name, output_dir):
        pass
