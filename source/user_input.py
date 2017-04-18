class UserInput(object):
    def __init__(self):
        self.state = None

    def ask(self):
        answer = raw_input('''
Enter number of operation or name of it
1. Yes (Y/y)
2. No (N/n)
3. Yes to all (allY)
4. No to all (allN)
5. Cancel
''')
        if answer == 'Yes' or answer == 'Y' or answer == 'y' or answer == '1':
            self.state = 'yes'
        elif answer == 'No' or answer == 'N' or answer == 'n' or answer == '2':
            self.state = 'no'
        elif answer == 'Yes to all' or answer == 'allY' or answer == '3':
            self.state = 'yes_to_all'
        elif answer == 'Yes' or answer == 'No to all' or answer == 'allN' or answer == '4':
            self.state = 'no_to_all'
        elif answer == 'Cancel' or answer == 'cancel' or answer == '5':
            self.state = 'cancel'

    def ask_yes_or_no(self):
        answer = raw_input('''
Enter number of operation or name of it
1. Yes (Y/y)
2. No (N/n)
3. Cancel
''')
        if answer == 'Yes' or answer == 'Y' or answer == 'y' or answer == '1':
            self.state = 'yes'
        elif answer == 'No' or answer == 'N' or answer == 'n' or answer == '2':
            self.state = 'no'
        elif answer == 'Cancel' or answer == 'cancel' or answer == '3':
            self.state = 'cancel'