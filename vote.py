# referred https://qiita.com/marufura/items/6f7d9ab1369a8f485100
import discord

# 自分のBotのアクセストークン
TOKEN = 'myTOKEN'

# Reaction
list_yesno = ['🙆‍♂️', '🙅‍♂️']
list_vote = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


def emphasize(text):
    return "**" + text + "**"


def underline(text):
    return "__" + text + "__"


def isContainedNoInput(command):
    for i in command:
        if i == "":
            return True
    return False


client = discord.Client()


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # コマンドのセパレータは"."
    command = message.content.split(".")

    # 投票関連のコマンド
    if command[0] == "question":

        # セパレータによる不自然な挙動を防止
        if isContainedNoInput(command):
            await message.channel.send("無効なコマンドです (セパレータが連続もしくは最後に入力されています)")
            return

        try:
            # Yes-No 疑問文
            if command[1] == "yes-no":
                embed = discord.Embed(title=command[2], description="", color=discord.Colour.blue())

                # 質問文を表示してYes,Noを絵文字でリアクション
                voting_msg = await message.channel.send(embed=embed)
                for i in range(len(list_yesno)):
                    await voting_msg.add_reaction(list_yesno[i])
                return

            # 選択肢のある疑問文　
            elif command[1] == "vote":
                embed = discord.Embed(title=command[2], description="", color=discord.Colour.green())

                # 選択肢の数を確認
                select = len(command) - 3
                if select > 10:
                    await message.channel.send("可能な選択肢は最大10個までです")
                    return

                # 選択肢を表示
                vote_candidate = command[3:]
                for i in range(len(vote_candidate)):
                    embed.description = embed.description + list_vote[i] + "   " + vote_candidate[i] + "\n"

                # リアクションによる回答欄を作成
                voting_msg = await message.channel.send(embed=embed)
                for i in range(select):
                    await voting_msg.add_reaction(list_vote[i])
                return

            # 使い方
            elif command[1] == "help":
                embed = discord.Embed(title="使用方法", description="", color=discord.Colour.red())
                embed.description = emphasize("question.[TYPE].[CONTENT] + .[CANDIDATE]\n") + \
                                    "注意 : 質問文や選択肢に\".\"を含めないでください\n" \
                                    "\n" \
                                    + emphasize("[TYPE] : \"yes-no\" or \"vote\"\n") + \
                                    underline("\"yes-no\" : \n") + \
                                    "Yes-No疑問文を作成します\n" \
                                    "[CANDIDATE]は必要ありません\n" \
                                    + underline("\"vote\" : \n") + \
                                    "選択肢が複数ある質問を作成します\n" \
                                    "[CANDIDATE]がない場合は質問文だけ表示されます\n" \
                                    "\n" \
                                    + emphasize("[CONTENT] : \n") + \
                                    "質問文に相当します\n" \
                                    "\n" \
                                    + emphasize("[CANDIDATE] : \n") + \
                                    "質問形式が\"vote\"である場合の選択肢です\n" \
                                    "選択肢として可能な最大個数は10個までです\n"
                await message.channel.send(embed=embed)

            # 以上のどの形式でもないものは形式不備を伝える
            else:
                await message.channel.send("質問形式が異なっています (2つめの引数が正しくありません)")
                return

        except IndexError:
            await message.channel.send("質問の入力形式に間違いがあります (引数が足りません)")
            return


# Botの起動とDiscordへの接続
client.run(TOKEN)