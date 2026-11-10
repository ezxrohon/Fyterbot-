from telethon import events, utils
import asyncio
import random
import time
import re

from runak.helpers import bot,replyraid,dreplyraid,raidinfo
from runak.plugins.vortex_core import register_cmd

VERSION = "1.0.0"
CATEGORY = "utilities"

active_raids = {
    "users": {},
    "stats": {},
    "start_time": {},
    "language": {}
}

RAID_BANNER = """
🎭 ═══════════════════════════════════════ 🎭
       ʀuɴAkuser𝐁‌σᴛ 𝗥𝗔𝗜𝗗 𝗦𝗬𝗦𝗧𝗘𝗠 
🎭 ═══════════════════════════════════════ 🎭
"""

HINDI_RAIDS = [\ "hi",
               "good morning",
               "happy birthday".
]

ENGLISH_RAIDS = [\ "kese ho ap",
                 "help me",
     
    
    

ACTIVATION_MESSAGE = """
🎭 **ʀuɴAkuser𝐁‌σᴛ RAID ACTIVATED** 🎭

🎯 **Target:** {}
🆔 **Target ID:** `{}`
🗣️ **Language:** {}
⚡ **Deployment:** Instant Reply System
🛡️ **Protection:** Elite Shield Active
✅ **Status:** Operational

🤖 **Powered by ʀuɴAkuser𝐁‌σᴛ**
"""

def init(client_instance):
    commands = [
        ".replyraid [hindi/english] [username/userid] - 🎭 Activate raid (reply or use username/ID)",
        ".dreplyraid - ❌ Deactivate active raid system", 
        ".raidinfo - 📊 Display raid statistics and data"
    ]
    description = "ʀuɴAkuser𝐁‌σᴛ Raid System - Advanced bilingual raiding with flexible targeting"
    add_handler("raid", commands, description)

async def parse_user_target(event, args):
    """Parse and retrieve user entity from reply, username, or ID"""
    user = None
    
    # Check if replying to a message
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user = await event.client.get_entity(reply.sender_id)
        return user
    
    # Extract username or ID from arguments
    # Remove language keywords first
    target_str = args.replace('hindi', '').replace('english', '').strip()
    
    if not target_str:
        return None
    
    try:
        # Check if it's a numeric ID
        if target_str.isdigit():
            user_id = int(target_str)
            user = await event.client.get_entity(user_id)
        # Check if it's a username (with or without @)
        else:
            # Remove @ if present
            username = target_str.lstrip('@')
            user = await event.client.get_entity(username)
            
    except ValueError as e:
        # Entity not found
        raise ValueError(f"Could not find user: {target_str}")
    except Exception as e:
        raise Exception(f"Error getting user entity: {str(e)}")
    
    return user

(events.NewMessage)
async def handle_all_messages(event):
    if event.sender_id in active_raids["users"]:
        try:
            sender = await event.get_sender()
            name = sender.first_name if sender and sender.first_name else "Target"
            
            response = f"[{name}](tg://user?id={event.sender_id}) "
            
            lang = active_raids["language"].get(event.sender_id, "english")
            messages = HINDI_RAIDS if lang == "hindi" else ENGLISH_RAIDS
            
            response += random.choice(messages)
            
            await event.reply(response)
            active_raids["stats"][event.sender_id] += 1
            
        except Exception as e:
            lang = active_raids["language"].get(event.sender_id, "english")
            response = f"[User](tg://user?id={event.sender_id}) "
            response += random.choice(HINDI_RAIDS if lang == "hindi" else ENGLISH_RAIDS)
            await event.reply(response)
            active_raids["stats"][event.sender_id] += 1

async def register_commands():
    on(events.NewMessage(pattern=r".replyraid(?: |$)(.*)"))
    async def activate_raid(event):
        try:
            args = event.pattern_match.group(1).lower()
            lang = "hindi" if "hindi" in args else "english"
            
            # Try to get user from reply or arguments
            user = await parse_user_target(event, args)
            
            if not user:
                await event.reply("🎭 **ʀuɴAkuser𝐁‌σᴛ Raid System**"
                                "❌ **Error:** No target specified!"
                                "💡 **Usage Options:**"
                                "• Reply to user's message: `.replyraid hindi`"
                                "• Use username: `.replyraid hindi @username`"
                                "• Use user ID: `.replyraid english 123456789`"
                                "🗣️ **Languages:** `hindi` or `english` (default: english)")
                return
            
            # Check if target is the bot owner
            if user.id == CIPHER_ELITE_OWNER:
                await event.reply("🎭 **Cipher Elite Security Protocol**"
                                "🛡️ **Access Denied:** You Cannot target my developer Rishabh"
                                "🔒 **Security Level:** Maximum Protection Active"
                                "⚠️ **Status:** Operation Blocked by Elite Shield")
                return
            
            # Check if already raiding this user
            if user.id in active_raids["users"]:
                await event.reply("🎭 **ʀuɴAkuser𝐁‌σᴛ Raid System**"
                                f"⚠️ **Already raiding:** {utils.get_display_name(user)}"
                                f"💡 **Tip:** Use `.dreplyraid` to stop the current raid first")
                return
            
            # Activate raid
            active_raids["users"][user.id] = True
            active_raids["stats"][user.id] = 0
            active_raids["start_time"][user.id] = time.time()
            active_raids["language"][user.id] = lang
            
            user_mention = f"[{utils.get_display_name(user)}](tg://user?id={user.id})"
            
            activation_msg = RAID_BANNER + ACTIVATION_MESSAGE.format(
                user_mention,
                user.id,
                lang.upper()
            )
            
            await event.reply(activation_msg)
            
        except ValueError as e:
            await event.reply(f"🎭 **ʀuɴAkuser𝐁‌σᴛ System Error**"
                            f"❌ **Error:** {str(e)}"
                            f"💡 **Tip:** Make sure the username/ID exists and is accessible")
        except Exception as e:
            await event.reply(f"🎭 **ʀuɴAkuser𝐁‌σᴛ System Error**"
                            f"❌ **Error:** {str(e)}")

    (events.NewMessage(pattern=r".raidinfo"))
    ()
    async def raid_info(event):
        try:
            info = f"{RAID_BANNER}🎭 **ACTIVE RAID STATISTICS**"
            
            if not active_raids["users"]:
                return await event.reply("🎭 **ʀuɴAkuser𝐁‌σᴛ Raid Monitor**"
                                       "❌ **No active raids detected**"
                                       "💡 **Use `.replyraid` to start raiding**"
                                       "📊 **All systems are idle**")
                
            for user_id in active_raids["users"]:
                try:
                    user = await event.client.get_entity(user_id)
                    duration = time.time() - active_raids["start_time"][user_id]
                    hits = active_raids["stats"][user_id]
                    lang = active_raids["language"][user_id]
                    
                    info += f"🎯 **Target:** {utils.get_display_name(user)}"
                    info += f"🗣️ **Language:** {lang.upper()}"
                    info += f"💥 **Hits Delivered:** {hits}"
                    info += f"⏱️ **Duration:** {int(duration)}s"
                    info += f"🆔 **User ID:** `{user_id}`"
                    info += f"🔥 **Status:** Active Raid"
                except Exception:
                    info += f"🎯 **Target ID:** `{user_id}`"
                    info += f"⚠️ **Status:** Entity unavailable"
                
            info += f"🤖 **Powered by CipherElite Raid System**"
            await event.reply(info)
        except Exception as e:
            await event.reply(f"🎭 **Raid Info Error:** {str(e)}")

    (events.NewMessage(pattern=r".dreplyraid(?: |$)(.*)"))
    ()
    async def deactivate_raid(event):
        try:
            args = event.pattern_match.group(1).strip()
            user_id = None
            
            # Check if replying to a message
            if event.reply_to_msg_id:
                reply = await event.get_reply_message()
                user_id = reply.sender_id
            # Check if username/ID provided
            elif args:
                try:
                    if args.isdigit():
                        user_id = int(args)
                    else:
                        username = args.lstrip('@')
                        user = await event.client.get_entity(username)
                        user_id = user.id
                except Exception:
                    await event.reply("🎭 **ʀuɴAkuser𝐁‌σᴛ  Raid System**"
                                    "❌ **Error:** Could not find specified user"
                                    "💡 **Check username/ID and try again**")
                    return
            
            if not user_id:
                await event.reply("🎭 **ʀuɴAkuser𝐁‌σᴛ Raid Deactivation**"
                                "❌ **Error:** No target specified!"
                                "💡 **Usage Options:**"
                                "• Reply to user's message: `.dreplyraid`"
                                "• Use username: `.dreplyraid @username`"
                                "• Use user ID: `.dreplyraid 123456789`")
                return
            
            if user_id in active_raids["users"]:
                final_hits = active_raids["stats"][user_id]
                duration = int(time.time() - active_raids["start_time"][user_id])
                
                del active_raids["users"][user_id]
                del active_raids["stats"][user_id]
                del active_raids["start_time"][user_id]
                del active_raids["language"][user_id]
                
                await event.reply("🎭 **ʀuɴAkuser𝐁‌σᴛ RAID DEACTIVATED** 🎭"
                                f"✅ **Successfully Stopped**"
                                f"💥 **Total Hits:** {final_hits}"
                                f"⏱️ **Duration:** {duration}s"
                                f"🛡️ **Elite Shield:** Restored"
                                f"🤖 **Powered by ʀuɴAkuser𝐁‌σᴛ**")
            else:
                await event.reply("🎭 **ʀuɴAkuser𝐁‌σᴛ Raid System**"
                                "❌ **No active raid found for this user**"
                                "💡 **Target is not currently being raided**")
                                
        except Exception as e:
            await event.reply(f"🎭 **Deactivation Error:** {str(e)}")
