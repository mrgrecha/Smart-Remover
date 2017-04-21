import user_input

def interactive(func):
    def func_wrapper(self, *args, **kwargs):
        answer = user_input.UserInput()
        if self.interactive:
            print 'Are you sure?'
            answer.ask_yes_or_no()
            if answer.state == 'yes':
                return func(self, *args, **kwargs)
            else:
                pass
        else:
            return func(self, *args, **kwargs)
    return func_wrapper
