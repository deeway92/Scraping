#On apporte les modules python
import discord
from discord.ext import commands, tasks
import mysql.connector
import random
import asyncio

TOKEN = 'Nzk2MjgwNDA3MDIwNDA0NzM2.X_Vn6w.kGKXiNXrc7JEv2_61wI0pSVWvtc'
data = [] #Création d'une liste vide pour pouvoir stocker les valeurs de la base de données ici nos films

con= mysql.connector.connect(host='127.0.0.1 ',database='discord',user='root',password='') #On se connecte a notre base de données
sql = "SELECT * FROM `film` ORDER BY `id_film` ASC" #Requête SQL
cursor = con.cursor()
cursor.execute(sql)
records = cursor.fetchall()
print("\nNombre total de ligne dans la table: ", cursor.rowcount) #Affiche le nombre de ligne

print("\nVoici les prochaines sorties de films en 2021 !")
for row in records:
	print("Nom des films | ",row[0]) #Affiche une à une les valeurs dans la base de données
	print("----------------------------------------------------------")


	data.append(row[1]) #Ajoute les valeurs une à une dans la liste vide
k = "\n".join(data) #Sauts de lignes dans la liste
print(k)

bot = commands.Bot(command_prefix = '!', description= "Bot de Nolan") #Prefix du bot discord

@bot.command()
async def Films(ctx): #Création d'un embed discord pour afficher les films de notre base de données
	embed=discord.Embed(title="Liste des films de 2021 !", description= k , color=0x12e23c)
	embed.set_author(name="Nolan")
	embed.set_footer(text="Projet python")
	embed.set_thumbnail(url="https://i.pinimg.com/originals/f6/de/49/f6de49d28109609f6067861b777d8e8f.jpg")
	await ctx.send(embed=embed)


status = ["!Films", #Permet d'avoir un statuts qui change sur le profil du bot
		"Projet de Nolan",
		"Classe de NSI", 
		"Créé sur Visual Studio", 
		"Lorsque vous volez, vous ne touchez pas le sol ! ", 
		"Je suis une IA", 
		"Mon créateur est Nolan",]

@bot.event #Fonction pour lancer le statuts
async def on_ready():
	print(" Bot Ready ! @By Nolan")
	changeStatus.start()
	
async def createMutedRole(ctx): #Fonction pour pouvoir créé un rôle mute et mettreles caractéristique du rôles
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx): #Fonction qui attribue le rôle
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command() #Fonction pour mute avec le prefix
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute par ! ")

@bot.command() #Fonction pour démute 
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !" )


@bot.command() #Fonction pour changer le status toute les 5 secondes
async def start(ctx, secondes = 5):
	changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
	game = discord.Game(random.choice(status))
	await bot.change_presence(status = discord.Status.offline, activity = game)


@bot.command #Fonction qui affiche les infos du serveur discord
async def serverInfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
	await ctx.send(message)

@bot.command() #Fonction qui éfface les messages
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()


@bot.command() #Fonction pour kick
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

@bot.command() #Fonction pour ban
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command() #Fonction pour unban
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")




bot.run(TOKEN) #Met en route le bot
