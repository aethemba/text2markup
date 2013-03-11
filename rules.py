"""
    Module that holds the rules for the parser to determine the applicability
    of rules for a block.

    A rule must do two things:
    1) Determine if a block fulfills the condition fo the rule
    2) Transform the block by calling the handler object

"""

class Rule(object):
    """ Defines a generic action function. Child objects implement
        their unique rule condition """
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        #Return True to terminate rule processing
        return True

class HeadingRule(Rule):
    """ Implements the condition to detect a headline.
        A heading is defined by:
            1) Not more than 70 chars
            2) Doesn't end with a colon
            3) Is a single line
    """
    type = 'heading' #Used by action method in super class
    def condition(self, block):
        return (not '\n' in block and len(block) <= 70 and not block[-1]==':')

class TitleRule(HeadingRule):
    """ Implements the condition to detect a headline.
        A title is defined by:
            1) The first block in a document, if its a heading
    """
    type = "title"
    first = True

    def condition(self, block):
        if not self.first:
            return False
        #First time around first is True, then set to False
        self.first = False
        #Use heading rule
        return HeadingRule.condition(self, block)

class ListItemRule(Rule):
    """ Implements list item detection
        Conditions:
        1) paragraph that starts with hyphen
    """

    type = 'listitem'

    def condition(self, block):
        return block[0]== '-'

    def action(self, block, handler):
        """ Reimplement superclass and remove the hyphen """
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    """ Detects a list.
        A list begins with a non-list item and follows with a list item. It
        ends when a non-list item is detected.
    """

    type = 'list'
    inside = False

    def condition(self, block):
        #Always returns True to examine all the blocks in a document
        # The action function will determine to apply markup
        return True

    def action(self, block, handler):
        """ Apply list markup for a section of listrule items  """
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False

class ParagraphRule(Rule):
    """ 
        Catch all rule. If its not a title, heading or list, its a paragraph
    """

    type = 'paragraph'

    def condition(self, block):
        return True

    #Use super obj  action
