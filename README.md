# A RESTful API for tracking IOUs

Okay, for this one, we would like a RESTful API that tracks Jo's borrowing habits and gives him a warning about how much he owes shylocks. Yeah, we want Jo to be better at managing money. Is that too much to ask? Okay, how about this instead:

Implement a RESTful API for tracking IOUs, simple enough yeah? I thought so too. Let me give you a little background.

Four roommates have a habit of borrowing money from each other frequently, and have trouble remembering who owes whom, and how much.

Your task is to implement a simple RESTful API that receives IOUs as POST requests, and can deliver specified summary information via GET requests.


### API Specification

#### User object
```json
{
  "name": "Adam",
  "owes": {
    "Bob": 12.0,
    "Chuck": 4.0,
    "Dan": 9.5
  },
  "owed_by": {
    "Bob": 6.5,
    "Dan": 2.75,
  },
  "balance": "<(total owed by other users) - (total owed to other users)>"
}
```

#### Methods

| Description | HTTP Method | URL | Payload Format | Response w/o Payload | Response w/ Payload |
| --- | --- | --- | --- | --- | --- |
| List of user information | GET | /users | `{"users":["Adam","Bob"]}` | `{"users":<List of all User objects>}` | `{"users":<List of User objects for <users> (sorted by name)}` |
| Create user | POST | /add | `{"user":<name of new user (unique)>}` | N/A | `<User object for new user>` |
| Create IOU | POST | /iou | `{"lender":<name of lender>,"borrower":<name of borrower>,"amount":5.25}` | N/A | `{"users":<updated User objects for <lender> and <borrower> (sorted by name)>}` |


Ensure you have a data store in place to store these records, they could be in-memory, an actual database or even a very simple JSON based database.

Bonus points if you implement a DELETE HTTP method to delete a user, and all his IOUs. I mean people move out, it is only fair to wipe out his/her ledger.

## Exception messages

No one likes errors, but they happen sometimes. It is necessary to raise an exception in such cases. When you do this, you should include a meaningful error message toindicate what the source of the error is. This makes your code more readable and helps significantly with debugging.

                                                     <<<END OF QUESTION>>>

----------------------------------------------------------------------------------------------------------------------------------------
## Solution 

### Setting Up the Environment

Step1: Install python on your machine depending on the Operating System you are using. https://www.python.org/downloads/
                  --Used Version: 3.7.7 ---

Step2: Install Pytest. https://docs.pytest.org/en/latest/getting-started.html
                   --Used Version: 5.4.1 ---


Step3: Download/clone this repository on your local environment



### Running the tests

To run the tests you need to pass the name of the testsuite file to pytest. In my case, see below. 

To run the tests, run `pytest rest_api_test.py`

Alternatively, you can tell Python to run the pytest module:
`python -m pytest rest_api_test.py`

#### Raise a Message with an Exception

To raise a message with an exception, just write it as an argument to the exception type. For example, instead of
`raise Exception`, you should write:

```python
raise Exception("Meaningful message indicating the source of the error")
```
