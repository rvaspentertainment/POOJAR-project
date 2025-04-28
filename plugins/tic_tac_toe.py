# plugins/tic_tac_toe.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import random
from game import TicTacToe

games = {}

def build_board(board, mode, game_id):
    buttons = []
    for i in range(0, 9, 3):
        row = []
        for j in range(3):
            cell = board[i+j]
            text = cell if cell != " " else "⬜"
            row.append(
                InlineKeyboardButton(text, callback_data=f"move|{mode}|{game_id}|{i+j}")
            )
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

def get_game_id(user_id):
    return str(user_id)

@Client.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "Choose Game Mode:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Single Player (vs Bot)", callback_data="mode|single")],
            [InlineKeyboardButton("2P Same Phone", callback_data="mode|same")],
            [InlineKeyboardButton("2P Different Phones", callback_data="mode|multi|invite")],
        ])
    )

@Client.on_callback_query(filters.regex("^mode\\|"))
async def mode_select(client, callback_query: CallbackQuery):
    data = callback_query.data.split("|")
    mode = data[1]

    if mode == "multi":
        await callback_query.message.reply("Send your partner's user ID to invite (example: 123456789).")
        return

    game_id = get_game_id(callback_query.from_user.id)
    games[game_id] = {
        "game": TicTacToe(),
        "mode": mode,
        "turn": "X",
        "player1": callback_query.from_user.id,
        "player2": None,
    }
    await callback_query.message.reply(
        "Game Started!\nYou are X",
        reply_markup=build_board(games[game_id]["game"].board, mode, game_id)
    )

@Client.on_message(filters.text & filters.reply & filters.regex("^[0-9]+$"))
async def receive_invite(client, message: Message):
    if not message.reply_to_message:
        return
    if "invite" not in message.reply_to_message.text:
        return
    try:
        partner_id = int(message.text)
    except:
        await message.reply("Invalid ID.")
        return
    game_id = f"{message.from_user.id}_{partner_id}"
    games[game_id] = {
        "game": TicTacToe(),
        "mode": "multi",
        "turn": "X",
        "player1": message.from_user.id,
        "player2": partner_id,
    }
    await message.reply(
        f"Game started with {partner_id}!\nYou are X",
        reply_markup=build_board(games[game_id]["game"].board, "multi", game_id)
    )

@Client.on_callback_query(filters.regex("^move\\|"))
async def handle_move(client, callback_query: CallbackQuery):
    _, mode, game_id, pos = callback_query.data.split("|")
    pos = int(pos)

    game = games.get(game_id)
    if not game:
        await callback_query.answer("Game not found.", show_alert=True)
        return

    user_id = callback_query.from_user.id
    if mode == "multi":
        if user_id not in [game["player1"], game["player2"]]:
            await callback_query.answer("Not your game!", show_alert=True)
            return
        if (game["turn"] == "X" and user_id != game["player1"]) or (game["turn"] == "O" and user_id != game["player2"]):
            await callback_query.answer("Wait for your turn!", show_alert=True)
            return

    success = game["game"].make_move(pos, game["turn"])
    if not success:
        await callback_query.answer("Invalid move.", show_alert=True)
        return

    winner = game["game"].check_winner()
    if winner:
        if winner == "Draw":
            text = "It's a Draw!"
        else:
            text = f"{winner} Wins!"
        await callback_query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Play Again", callback_data="restart")],
                [InlineKeyboardButton("Back to Menu", callback_data="back_to_menu")]
            ])
        )
        games.pop(game_id, None)
        return

    # Switch turn
    game["turn"] = "O" if game["turn"] == "X" else "X"

    if mode == "single" and game["turn"] == "O":
        empty = [i for i, cell in enumerate(game["game"].board) if cell == " "]
        if empty:
            bot_move = random.choice(empty)
            game["game"].make_move(bot_move, "O")
            winner = game["game"].check_winner()
            if winner:
                if winner == "Draw":
                    text = "It's a Draw!"
                else:
                    text = f"{winner} Wins!"
                await callback_query.message.edit_text(
                    text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Play Again", callback_data="restart")],
                        [InlineKeyboardButton("Back to Menu", callback_data="back_to_menu")]
                    ])
                )
                games.pop(game_id, None)
                return
            else:
                game["turn"] = "X"

    await callback_query.message.edit_text(
        f"{game['turn']}'s Turn",
        reply_markup=build_board(game["game"].board, mode, game_id)
    )

@Client.on_callback_query(filters.regex("^restart$"))
async def restart_game(client, callback_query: CallbackQuery):
    await start(client, callback_query.message)

@Client.on_callback_query(filters.regex("^back_to_menu$"))
async def back_to_menu(client, callback_query: CallbackQuery):
    await start(client, callback_query.message)
