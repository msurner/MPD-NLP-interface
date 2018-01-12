from enum import Enum

# conversation state is stored in a expiringdict
# note that there an additional state which is also the initial state which is considered if no state is stored
class ConversationStateEnum(Enum):
    Initial = 0 # only for initialization, same as not existing / expired
    AwaitYesOrNo = 1
    AwaitSongArtistOrGenre = 2


class ConversationState:
    """This class defines a simple state type for states and suggested instructions"""
    state = ConversationStateEnum.Initial
    suggestion = ""

    def __init__(self, state, suggestion=None):
        self.state = state
        self.suggestion = suggestion
