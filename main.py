import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=",")


@bot.event
async def on_ready():
    print("Bot is active.")


class General(commands.Cog):
    @commands.command()
    async def members(self, ctx):
        embed = discord.Embed(
            title='Member Count',
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="Server: ", value=ctx.guild.name, inline=False)
        embed.add_field(name="Members: ", value=ctx.guild.member_count, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx, member: discord.Member):
        _roles = [role.mention for role in member.roles if not role.is_default()]
        _roles.append(str(ctx.guild.default_role))
        member_roles = str.join(', ', _roles)
        embed = discord.Embed(
            title='User Info',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User: ", value=member.mention, inline=False)
        embed.add_field(name="Roles: ", value=member_roles, inline=False)
        embed.add_field(name="Creation date: ", value=member.created_at, inline=False)
        await ctx.send(embed=embed)

    @info.error
    async def info(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please provide a valid user.')
            
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {int(bot.latency)}ms')


class Moderation(commands.Cog):
    @commands.command()
    @commands.has_role('Bot Operator')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.message.delete()
        await member.send(f'You have been kicked from {ctx.guild.name} for reason: {reason}')
        await member.kick(reason=reason)
        embed = discord.Embed(
            title='User Kicked',
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User: ", value=member.mention, inline=False)
        embed.add_field(name="Kicked by: ", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason: ", value=reason, inline=False)
        channel = bot.get_channel(756284124733374494)
        await channel.send(embed=embed)

    @kick.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please provide a valid user.')

    @commands.command()
    @commands.has_role('Bot Operator')
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.message.delete()
        await member.send(f'You have been banned from {ctx.guild.name} for reason: {reason}')
        await member.ban(reason=reason)
        embed = discord.Embed(
            title='User Banned',
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User: ", value=member.mention, inline=False)
        embed.add_field(name="Banned by: ", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason: ", value=reason, inline=False)
        channel = bot.get_channel(756284124733374494)
        await channel.send(embed=embed)

    @ban.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please provide a valid user.')

    @commands.command()
    @commands.has_role('Bot Operator')
    async def unban(self, ctx, member):
        await ctx.message.delete()
        banned_users = await ctx.guild.bans()
        banned_name, banned_discriminator = None, None

        try:
            banned_name, banned_discriminator = member.split("#")
        except ValueError:
            await ctx.send("Please provide a valid username and discriminator.")

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name and user.discriminator) == (banned_name and banned_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title='User Unbanned',
                    color=discord.Color.green(),
                )
                embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name="User: ", value=member, inline=False)
                embed.add_field(name="Unbanned by: ", value=ctx.author.mention, inline=False)
                channel = bot.get_channel(756284124733374494)
                await channel.send(embed=embed)

    @commands.command()
    @commands.has_role('Bot Operator')
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        await ctx.message.delete()
        await member.send(f'You have been muted in {ctx.guild.name} for reason: {reason}')
        await member.add_roles(discord.utils.get(ctx.guild.roles, id=756308928052068502), reason=reason, atomic=True)
        embed = discord.Embed(
            title='User Muted',
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User: ", value=member.mention, inline=False)
        embed.add_field(name="Muted by: ", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason: ", value=reason, inline=False)
        channel = bot.get_channel(756284124733374494)
        await channel.send(embed=embed)

    @mute.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please provide a valid user.')

    @commands.command()
    @commands.has_role('Bot Operator')
    async def unmute(self, ctx, member: discord.Member):
        await ctx.message.delete()
        await member.remove_roles(discord.utils.get(ctx.guild.roles, id=756308928052068502), atomic=True)
        embed = discord.Embed(
            title='User Unmuted',
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User: ", value=member.mention, inline=False)
        embed.add_field(name="Unmuted by: ", value=ctx.author.mention, inline=False)
        channel = bot.get_channel(756284124733374494)
        await channel.send(embed=embed)

    @unmute.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please provide a valid user.')

    @commands.command()
    @commands.has_role('Bot Operator')
    async def purge(self, ctx, num: int):
        await ctx.channel.purge(limit=num, check=None)
        embed = discord.Embed(
            title='Channel Purged',
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="User: ", value=ctx.author.mention, inline=False)
        embed.add_field(name="Purged channel: ", value=ctx.channel.mention, inline=False)
        channel = bot.get_channel(756284124733374494)
        await channel.send(embed=embed)

    @purge.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please provide a valid integer.')


bot.add_cog(General(bot))
bot.add_cog(Moderation(bot))

bot.run(TOKEN)
