from datetime import datetime

import os

TIME_FORMAT = "%H:%M:%S"
LEFT_INDICATORS = ["_left", "_l", "ll", "/left"]
RIGHT_INDICATORS = ["_right", "_r", "rr", "/right"]
EXIT_INDICATORS = ["exit()", "exit", "ee", "/exit"]
CLEAR_INDICATORS = ["clear()", "clear", "cls", "/clear"]


def clear_line() -> None:
    """Clears the last printed line from the termnal."""
    print(
        "\033[A                                                                                       \033[A"
    )


def clear_terminal() -> None:
    """Clears the entire terminal of any printouts."""
    os.system("cls" if os.name == "nt" else "clear")


class User:
    """Represents a user in the chat"""

    registered_users: dict[str, "User"] = {}

    def __init__(self, name: str, left: str, right: str):
        self.name = name
        self._left = left
        self._right = right

        self.__class__.register(self)

    @property
    def left(self) -> "User":
        """
        Resolves the user to the 'left' of the current user
        via the registered user dict, caching the value for future calls
        """
        if isinstance(self._left, str):
            self._left = self.__class__.registered_users[self._left]
        return self._left

    @property
    def right(self) -> "User":
        """
        Resolves the user to the 'right' of the current user
        via the registered user dict, caching the value for future calls

        Returns:
            right_user (User): The user to the 'right' of self
        """
        if isinstance(self._right, str):
            self._right = self.__class__.registered_users[self._right]
        return self._right

    @classmethod
    def from_list(cls, user_list: list[str] | None) -> None:
        """
        Registers a list of users from a list of username strings

        Returns:
            left_user (User): The user to the 'left' of self
        """
        user_list = user_list or ["Anonymous"]
        for index, name in enumerate(user_list):
            left_index = index - 1
            right_index = index + 1 if (index + 1) < len(user_list) else 0
            cls(name=name, left=user_list[left_index], right=user_list[right_index])

    @classmethod
    def register(cls, user: "User") -> None:
        """
        Registers a single user object under the user name.
        """
        cls.registered_users.update({user.name: user})

    @classmethod
    def as_list(cls) -> list[str]:
        """
        Retrieves all registered users as a list of strings.

        Returns:
            user_list (list[str]): List of registered user names.
        """
        return list(cls.registered_users.values())

    def __str__(self) -> str:
        """The string representation of a user is their name."""
        return self.name


class ChatLog:
    """
    Keeps track of all messages printed to stdout to be able to
    dump them to an output file for later use.
    """

    def __init__(self, users=list[User]):
        self.users = users
        self.logs = []

    @property
    def filename(self) -> str:
        """
        Creates a unique file name for each chat log file
        including the current date, time, and registered
        users (even if they did not send a message).

        returns:
            filename (str): A unique file name for this chat.
        """
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        for user in self.users:
            filename += f"_{user.name}"
        filename += "_logs.txt"
        return filename

    def add(self, user: User, time: datetime, message: str) -> None:
        """
        Stores a message as they were printed to stdout in the chat log.
        """
        self.logs.append(f"[{time.strftime(TIME_FORMAT)}] {user}: {message}")

    def delete_all(self) -> None:
        """
        Fully clears the chat log to start anew.
        """
        self.logs = []

    def dump(self) -> None:
        """
        Invoked when an 'EXIT_INDICATORS' is typed.
        """
        as_str = ""
        for i in self.logs:
            as_str += i + "\n"
        with open(self.filename, "a") as file:
            file.write(as_str)


def main():
    """
    Clears the terminal and asks the user for two optional inputs:
    1. The time the IRC chat takes place in. This is to evoke the illusion
        that these chats were typed on different times.
        If left empty, it simply takes your current system time stamp. Readers may
        grow suspicious whenn lore dumps that supposedly occurred on different times
        happened right after one another, though.

        The timestamps of the chats are is updated live in real time, to
        also simulate the typing speed of the chat participants in accordance
        with your own typing speed.

    2. The list of users that are present in the chat.
        Chat logs usually concern two or more people, unless you want to write a monologue or a diary.
        During writing, you can change which user is typing by typing one of the indicators.

    The users are registered in the User class, and the chat log begins.
    You can now type chat messages as your user. Should you wish to change users,
    you can type one of the LEFT_INDICATORS or RIGHT_INDICATORS
    and send the message to type as a different user.
    (Imagine that the users are sitting around a circular dinner table,
    hence 'left' and 'right'.)

    Example:
    [23:22:08] DioBrando: Oh? You're approaching me?
    [23:22:14] DioBrando: /left

    becomes:
    [23:22:08] DioBrando: Oh? You're approaching me?
    [23:22:16] JotaroKujo:

    Should you wish to start anew, you can clear the chat by typing a CLEAR_INDICATOR:
    [23:22:08] DioBrando: Oh? You're approaching me?
    [23:22:20] DioBrando: /clear


    Should you wish to stop and save the chat, you may type an EXIT_INDICATOR:
    [23:22:32] DioBrando: /exit
    The chat is then stored in the same folder the python script is located in
    with a unique file name consisting of the datetime you created the chat on,
    and the participating users.

    Alternatives for these commands are documented at the top of this program as the indicator constants.

    Happy typing!
    """
    clear_terminal()
    time_input = input(
        f"Optionally provide a time of day in {TIME_FORMAT} (e.g.: 12:44:37) or press enter for current system time: "
    )
    irc_time = (
        datetime.strptime(time_input, TIME_FORMAT) if time_input else datetime.now()
    )

    users = (
        input(
            "Please provide a list of users that are present in the chat in username, username, username format. \n"
        )
        or "Anonymous"
    )
    cleaned_users = [user.strip() for user in users.split(",")]

    # Register users
    User.from_list(cleaned_users)

    # Retrieve registered users
    user_list = User.as_list()
    current_user = next(iter(user_list))

    clear_terminal()
    start_time = datetime.now()
    logs = ChatLog(users=user_list)
    while True:
        received_input = input(f"[{irc_time.strftime(TIME_FORMAT)}] {current_user}: ")
        parsed_input = received_input.strip().lower()

        if parsed_input in LEFT_INDICATORS:
            current_user = current_user.left
            clear_line()
        elif parsed_input in RIGHT_INDICATORS:
            current_user = current_user.right
            clear_line()
        elif parsed_input in CLEAR_INDICATORS:
            clear_terminal()
            logs.delete_all()
        elif parsed_input in EXIT_INDICATORS:
            clear_line()
            logs.dump()
            exit()
        else:
            logs.add(user=current_user, time=irc_time, message=received_input)

        irc_time = irc_time + (datetime.now() - start_time)
        start_time = datetime.now()


if __name__ == "__main__":
    main()
