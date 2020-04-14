
import json

class RestAPI():

    """Class for tracking debts between users. Accepts GET requests
    with url '/users' any number of users as data, information on
    specified users, or all users if none are specified. Accepts
    POST requests with url '/iou' and data specifying a transaction
    between two users, returning information on the involved users.
    Also accepts POST requests with url '/add' and data containing
    a name, and adds a new user with no debts or balance, then returns
    information on the new user.
    """
    jsondb = dict()
    gethandlers = dict()
    posthandlers = dict()

    def __init__(self, database=None):
        self.jsondb = database
        self.gethandlers['/users'] = self.users
        self.posthandlers['/add'] = self.add
        self.posthandlers['/iou'] = self.iou

    def get(self, url, payload=None):
        ''' Handler for an http GET to the provided URL.Processes GET requests. '''
        return self.exec_handler(self.gethandlers, url, payload)

    def post(self, url, payload=None):
        ''' Handler for an http POST to the provided URL. Processes POST requests.'''
        return self.exec_handler(self.posthandlers, url, payload)

    @staticmethod
    def exec_handler(handlers, url, payload):
        ''' Looks up and executes the requested handler, or throws '''
        handler = handlers[url]
        if not handler:
            raise Exception(f"No route defined for {url}.")

        return handler(payload)

    def users(self, payload):
        ''' Returns a users dictionary as a JSON string,
            filtering by the provided user list,
            or all if no filter is provided'''
        ret = ""
        if payload:
            ret = self.get_named_users(payload)
        else:
            ret = json.dumps(self.jsondb)

        return ret

    def get_named_users(self, payload):
        ''' Returns a JSON string of all users matching
            the requested names in the provided payload '''

        users = []

        try:
            names = json.loads(payload)['users']
            names.sort()
        except:
            raise Exception(f"Could not parse 'users' key of JSON payload as array: {payload}")

        for name in names:
            for user in self.jsondb['users']:
                if name == user['name']:
                    users.append(user)

        ret = {"users": users}
        return json.dumps(ret)

    def add(self, payload):
        ''' Adds a user to the database.  '''
        try:
            name = json.loads(payload)['user']
        except:
            raise Exception(f"Could not parse 'user' key of JSON payload: {payload}")

        if name in self.jsondb['users']:
            raise Exception(f"User {name} already exists")

        user = self.new_user(name)
        self.jsondb['name'] = user
        return json.dumps(user)

    @staticmethod
    def new_user(name):
        ''' Creates a new user with the given name '''
        user = {"name": name, "owes": {}, "owed_by": {}, "balance": 0.0}
        return user

    def iou(self, payload):
        ''' Adds an IOU from one user to another '''
        try:
            iou = json.loads(payload)
            lname = iou['lender']
            bname = iou['borrower']
            amount = iou['amount']
        except:
            raise Exception(f"Could not parse JSON payload: {payload}")

        for user in self.jsondb['users']:
            if lname == user['name']:
                lender = user
            if bname == user['name']:
                borrower = user

        if not lender:
            raise Exception(f"Could not find user {lname}")
        if not borrower:
            raise Exception(f"Could not find user {bname}")

        self.adjust_balances(lender, True, bname, amount)
        lender['balance'] = lender['balance'] + amount

        self.adjust_balances(borrower, False, lname, amount)
        borrower['balance'] = borrower['balance'] - amount

        users = [lender, borrower] if lname < bname else [borrower, lender]
        ret = {"users": users}
        return json.dumps(ret)

    def adjust_balances(self, user, user_is_lender, name, amount):
        ''' Update the appropriate named balance
            for the user's balances.

            1. Check for a previous
            balance for the named party that should be
            canceled or reduced.

            2. If found, adjust that balance by the
            given amount and compute the difference.

            3. Then apply either the difference
            or the full amount
            to the balance listed in the second key. '''

        reduce_bal = 'owes' if user_is_lender else 'owed_by'
        increase_bal = 'owed_by' if user_is_lender else 'owes'

        if name in user[reduce_bal]:
            prev_bal = user[reduce_bal][name]
            new_bal = prev_bal - amount
            if amount < prev_bal:
                user[reduce_bal][name] = new_bal
            else:
                del user[reduce_bal][name]
                remainder = -1 * new_bal
                self.increase_named_bal(user[increase_bal], name, remainder)
        else:
            self.increase_named_bal(user[increase_bal], name, amount)

    @staticmethod
    def increase_named_bal(balances, name, amount):
        ''' Increase (or create) the balance
            for the named party in the list of balances
            by the given amount '''
        if name in balances:
            new_bal = balances[name] + amount
            if new_bal:
                balances[name] = new_bal
            else:
                del balances[name]
        elif amount:
            balances[name] = amount