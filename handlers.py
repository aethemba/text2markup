"""
    A handler is responsible for generating the resulting marked-up text. The
    parser will send detailed instructios.
"""

class Handler(object):
    """ Superclass for the handlers of various markup types. Takes
        care of various administrative tasks.
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        return self.callback('start_', name)

    def end(self, name):
        return self.callback('end_', name)

    def sub(self, name):
        """ Returns a new function, used as the replacement function for
            re.sub that returns a match object """
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                match.group(0) #Return the entire string
            return result
        return substitution

class HTMLHandler(Handler):
    """ Renders the appropriate markup for the specified type """

    def start_document(self):
        print '<html><head><title>...</title></head><body>'

    def end_document(self):
        print '</body></html>'

    def start_paragraph(self):
        print '<p>'

    def end_paragraph(self):
        print '</p>'

    def start_heading(self):
        print '<h2>'

    def end_heading(self):
        print '</h2>'

    def start_list(self):
        print '<ul>'

    def end_list(self):
        print '</ul>'

    def start_listitem(self):
        print '<li>'

    def end_listitem(self):
        print '</li>'

    def start_title(self):
        print '<h1>'

    def end_title(self):
        print '</h1>'

    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1) )

    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1) )

    def sub_emphasis(self, match):
        """ Receives the match object from the regex """
        #Subsitutes the first match
        return '<em>%s</em>' % match.group(1)

    def feed(self, data):
        print data
