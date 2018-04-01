from smartz.api.constructor_engine import ConstructorInstance
from smartz.eth.contracts import make_generic_function_spec, merge_function_titles2specs


class Constructor(ConstructorInstance):
    def get_params(self):
        json_schema = {
            "type": "object",
            "additionalProperties": False,
        }

        ui_schema = {}

        return {
            "result": "success",
            "schema": json_schema,
            "ui_schema": ui_schema
        }


    def construct(self, fields):
        source = self.__class__._TEMPLATE
        return {
            "result": "success",
            'source': source,
            'contract_name': "DictatorVoting"
        }


    def post_construct(self, fields, abi_array):
        function_titles = {
            'voteResult': {
                'title': 'Vote result',
                'description': 'Vote of dictator'
            },

            'dictatorVoting': {
                'title': 'Vote',
                'description': 'You are dictator make your vote (true of false)',
                'inputs': [{
                    'title': 'vote',
                }]
            }
        }
        return {
            "result": "success",
            'function_specs': merge_function_titles2specs(make_generic_function_spec(abi_array), function_titles),
            'dashboard_functions': ['voteResult']
        }


    # language=Solidity
    _TEMPLATE = """
pragma solidity ^0.4.0;
contract DictatorVoting {
    address dictator;
    bool dictatorVote;

    function dictatorVoting(bool vote) public {
        dictatorVote = vote;
    }

    function voteResult() public constant returns (bool _voteResult) {
        _voteResult = dictatorVote;
    }

}"""
