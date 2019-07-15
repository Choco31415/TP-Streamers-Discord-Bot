# Handle imports
from config import config

# Define variables
command_lookup = {}
aliases = {}
command_start = config["command_start"]

# Define methods
def register_command(func, name, category, params, help_message=None,
                     help_func=None, alias_list=None, owner_only=False):
    if not alias_list is None:
        for a in alias_list:
            aliases[a] = name

    command_lookup[name] = Command(
        name=name,
        command=func,
        aliases=alias_list,
        category=category,
        help_message=help_message,
        help_func=help_func,
        params=params,
        owner_only=owner_only
    )

class Command():
    def __init__(self, name, command, aliases, category, help_message, help_func, params, owner_only):
        self.name = name
        self.command = command
        self.aliases = [] if (aliases is None) else aliases
        self.category = category
        self.help_message = help_message
        self.help_func = help_func
        self.params = params
        self.owner_only = owner_only

    async def get_help(self, message, include_params=False):
        '''
        Gets the help message of a command.
        :param message: A message
        :param include_params: Whether or not to include command params.
        :return: A help message.
        '''
        this_aliases = [self.command] + self.aliases

        # Gather parameter info
        param_info = ""
        if include_params:
            for param in self.get_params():
                param_attributes = param["attributes"] if "attributes" in param else []
                attribute_info = "".join(
                    ["(" + a + ")" for a in param_attributes])
                if len(param_attributes) > 0:
                    attribute_info = " " + attribute_info
                param_info += " <" + param["name"] + attribute_info + ">"

        # Gather alias info
        alias_info = ", ".join(self.aliases)

        # Gather context info
        if self.help_message is None:
            context = await self.help_func(message)
        else:
            context = self.help_message
        if self.owner_only:
            context = "(server-owner) " + context

        # Handle formatting
        lstub = "{}{}{}".format(self.name, alias_info, param_info)
        if include_params:
            lstub = lstub.ljust(20)
        else:
            lstub = lstub.ljust(12)

        return command_start + lstub + " :: " + context

    def run(self, message, args):
        return self.command(message, args)

    def get_category(self):
        return self.category

    def get_params(self):
        return self.params

    def is_owner_only(self):
        return self.owner_only