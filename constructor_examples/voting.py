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
            'contract_name': "SmartVotes"
        }


    def post_construct(self, fields, abi_array):
        function_titles = {
            'addQuestion': {
                'title': 'Add Question',
                'description': 'Add question',
                'inputs': [{
                    'title': 'your new question',
                }]
            },

            'readQuestion': {
                'title': 'Read question',
                'description': '',
                'inputs': [{
                    'title': 'question number',
                }]
            },

            'userVoting':{
                'title': 'Make your vote',
                'description': '',
                'inputs': [
                    {'title': 'true'},
                    {'title': 'question number'}
                ]

            },

            'closeVote': {
                'title': 'Close vote',
                'description': '',
                'inputs': [{
                    'title': 'question number',
                }]
            },

            'voteResult': {
                'title': 'Get vote result for closed question',
                'description': '',
                'inputs': [{
                    'title': 'question number',
                }]
            },
        }
        return {
            "result": "success",
            'function_specs': merge_function_titles2specs(make_generic_function_spec(abi_array), function_titles),
            'dashboard_functions': ['voteResult']
        }


    # language=Solidity
    _TEMPLATE ="""
pragma solidity ^0.4.0;
contract SmartVotes {
    address dictator;
    bool dictatorVote;
    
    struct Question {
        string info;
        bool voted;
        bool voteResult;
        bool isClosed;
        address[] voters;
        mapping(address => bool) votes;
        mapping(address => bool) ifVotes;
    }
    Question[] public questions;
    
    function addQuestion(string info) public returns (uint _questionNumber){
        _questionNumber = questions.length;
        questions.length += 1;
        address[] memory voters;
        questions[_questionNumber] = Question(info, false, false, false, voters);
    }
    
    function readQuestion(uint questionNumber) public constant
    returns (string _question){
        _question = questions[questionNumber].info;
    }
    
    function userVoting(bool vote, uint questionNumber) public {
        if (questions[questionNumber].voted) return;
        bool ifVote = questions[questionNumber].ifVotes[msg.sender];
        if (!(ifVote)){
          questions[questionNumber].voters.push(msg.sender);  
        } 
        questions[questionNumber].votes[msg.sender] = vote;
        questions[questionNumber].ifVotes[msg.sender] = true;
    }
    
    function closeVote(uint questionNumber) public returns (bool _result) {
        bool isClosed = questions[questionNumber].isClosed;
        if (!isClosed){
            int winningVoteCount = 0;
            for (uint prop = 0; prop < questions[questionNumber].voters.length; prop++)
                address nextVoter = questions[questionNumber].voters[prop];
                if (questions[questionNumber].votes[nextVoter]){
                    winningVoteCount += 1;  
                }else{
                    winningVoteCount -= 1;
                }
            if (winningVoteCount > 0){
                questions[questionNumber].voteResult = true;
            }else{
                questions[questionNumber].voteResult = false;
            }
            questions[questionNumber].isClosed = true;
        }
         _result = questions[questionNumber].voteResult;
        
    }
    
    function voteResult(uint questionNumber) public constant returns (bool _result) {
        _result = questions[questionNumber].voteResult;
    }
    
}
"""