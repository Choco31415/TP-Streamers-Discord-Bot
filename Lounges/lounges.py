# Handle imports
from discord.utils import get
import asyncio
from config import config
from permissions import *
from config import config

# Define variables
lounges = []

# Define classes
class Lounge():
    def __init__(self, vc, tc, creator):
        # Create vars
        self.creator = creator
        self.guild = vc.guild
        self.name = vc.name
        self.vc = vc
        self.tc = tc
        self.vc_blocks = []
        self.admins = [creator]
        self.locked = False
        self.member_count = 0
        self.time_to_delete = config["lounges"]["timeout"] # Seconds
        self.delete_task = None
        self.deleted = False

    async def remove_member(self, member):
        """
        Remove a member from the lounge. Assumes lounge is unlocked.
        :param member:
        :return:
        """
        if not self.deleted:
            await self.tc.set_permissions(member, overwrite=lounge_tc_disallow)
            self.member_count = len(self.vc.members)
            if self.member_count == 0:
                await self.schedule_empty_check()

            if self.locked:
                if not member in self.admins:
                    await self.vc.set_permissions(member,
                                              overwrite=lounge_vc_disallow)

                self.vc_blocks.append(member)

    async def kick_member(self, member, requestor):
        """
        A user requests a user to be kicked
        :param requestor:
        :return:
        """
        if self.is_admin(requestor):
            if not self.is_admin(member):
                await self.tc.send("Removing member {}, please wait.".format(member.name))
                if self.locked:
                    self.vc_blocks.append(member) # Auto block them
                await self.remove_member(member)

                old_vc = self.vc
                self.vc = await self.vc.clone()

                # Transfer members over
                for m in old_vc.members:
                    if m != member:
                        await m.move_to(self.vc)

                await old_vc.delete()

                #Setup permissions on new vc, Discord doesn't always copy them correctly
                for member in self.vc_blocks:
                    await self.vc.set_permissions(member,
                                              overwrite=lounge_vc_disallow)
                for admin in self.admins:
                    await self.vc.set_permissions(admin,
                                                  overwrite=lounge_vc_allow)
                if self.locked:
                    await self.vc.set_permissions(self.guild.default_role,
                                                  overwrite=lounge_vc_disallow)

                self.member_count = len(self.vc.members)

                await self.tc.send("Removed member {}.".format(member.name))
            else:
                await self.tc.send("Cannot kick an admin!")
        else:
            await self.tc.send(
                "{} is not an admin and cannot run admin commands.".format(
                    requestor.name))

    async def add_member(self, member):
        """
        Add a member to the lounge. Assumes lounge is unlocked.
        :param member:
        :return:
        """
        await self.tc.set_permissions(member, overwrite=lounge_tc_allow)
        self.member_count += 1
        await self.interrupt_empty_check()

    async def toggle_admin(self, member, requestor):
        if self.is_admin(requestor):
            if member != self.creator:
                if self.is_admin(member):
                    self.admins.remove(member)

                    await self.tc.send("{} is no loner an admin.".format(member.name))
                else:
                    self.admins.append(member)

                    if self.locked:
                        await self.vc.set_permissions(member,
                                                      overwrite=lounge_vc_allow)

                    await self.tc.send(
                        "{} is now an admin!".format(member.name))
            else:
                await self.tc.send("Lounge creators are always admins.")
        else:
            await self.tc.send(
                "{} is not an admin and cannot run admin commands.".format(
                    requestor.name))

    def get_admins(self):
        return self.admins

    def is_admin(self, member):
        return member in self.admins

    async def toggle_lock(self, requestor):
        """
        Lock a lounge
        :return:
        """
        if self.is_admin(requestor):
            self.locked = not self.locked

            if self.locked:
                await self.vc.set_permissions(self.guild.default_role,
                                              overwrite=lounge_vc_disallow)

                for admin in self.admins:
                    await self.vc.set_permissions(admin,
                                                  overwrite=lounge_vc_allow)

                await self.tc.send("The lounge is locked.")
            else:
                await self.vc.set_permissions(self.guild.default_role,
                                              overwrite=lounge_vc_allow)

                for member in self.vc_blocks:
                    await self.vc.set_permissions(member,
                                                  overwrite=lounge_vc_allow)
                self.vc_blocks = []

                await self.tc.send("The lounge is unlocked.")
        else:
            await self.tc.send(
                "{} is not an admin and cannot run admin commands.".format(
                    requestor.name))

    async def bypass_member(self, member, requestor):
        if self.locked:
            if self.is_admin(requestor):
                if not self.is_admin(member):
                    if member in self.vc.members:
                        await self.vc.set_permissions(member,
                                                      overwrite=lounge_vc_disallow)

                        self.vc_blocks.append(member)

                        await self.tc.send("{} is blocked from entering.".format(member.name))
                    else:
                        await self.vc.set_permissions(member,
                                                      overwrite=lounge_vc_allow)

                        if member in self.vc_blocks:
                            self.vc_blocks.remove(member)

                        await self.tc.send(
                            "{} is allowed to enter.".format(member.name))
                else:
                    await self.tc.send("{} is an admin and cannot be bypassed.".format(member.name))
            else:
                await self.tc.send(
                    "{} is not an admin and cannot run admin commands.".format(
                        requestor.name))
        else:
            await self.tc.send("This channel is not locked and hence can't be bypassed.")

    async def schedule_empty_check(self):
        """
        Start destruct sequence. Is not immediate.
        :return:
        """
        if self.delete_task is None:
            self.delete_task = asyncio.ensure_future(self.empty_check())

    async def interrupt_empty_check(self):
        """
        Stop destruct sequence if occurring
        :return:
        """
        if not self.delete_task is None:
            self.delete_task.cancel()
            try:
                await self.delete_task
            except:
                pass
            self.delete_task = None

    async def empty_check(self):
        """
        Check if lounge is empty, and delete if needed
        :return:
        """
        await asyncio.sleep(self.time_to_delete)
        if self.member_count == 0:
            await self.delete()

    async def request_delete(self, requestor):
        """
        A user requests the lounge deleted.
        :param requestor:
        :return:
        """
        if self.is_admin(requestor):
            await self.delete()
        else:
            await self.tc.send(
                "{} is not an admin and cannot run admin commands.".format(
                    requestor.name))

    async def delete(self):
        if not self.deleted:
            self.deleted = True

            await self.vc.delete()
            await self.tc.delete()

            lounges.remove(self)

# Define methods
async def create_lounge(guild, lounge_name, creator):
    """
    Create a lounge
    :param guild:
    :param lounge_name:
    :param creator:
    :return:
    """
    # Handle setup
    lounge_category = get(guild.categories, name=config["lounges"]["category_name"])

    overwrites = {guild.me: lounge_vc_allow_bot,}

    vc = await guild.create_voice_channel(lounge_name,
                               category=lounge_category,
                               overwrites=overwrites)

    overwrites = {guild.default_role: lounge_tc_disallow,
                  guild.me: lounge_tc_allow}

    tc = await guild.create_text_channel(lounge_name,
                              category=lounge_category,
                              overwrites=overwrites)

    new_lounge = Lounge(vc, tc, creator)

    await new_lounge.schedule_empty_check()

    lounges.append(new_lounge)