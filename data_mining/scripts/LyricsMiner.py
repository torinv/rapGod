import Lyrics
import filter

# Country lyrics miner
# Lyrics.getLyrics("spotify:user:berardone:playlist:4TC5TMRoosckbFFBl2x3wI", 535, "country_lyrics.txt", "w") # Summer Country playlist
# Lyrics.getLyrics("spotify:user:225maj3hqpdbqhxihtfoyphdy:playlist:6gXgPeZLfob30T6RSoy9nb", 222, "country_lyrics.txt", "a")  # 2000 country music playlist
# Lyrics.getLyrics("spotify:user:mmabxr:playlist:1r2Ej3bxEMFpnLmDTTqrQx", 262, "country_lyrics.txt", "a")  # 90 country playlist
# Lyrics.getLyrics("spotify:user:sambone2:playlist:3Iy6IrE5A54fi8Ngnsrk8Z", 251, "country_lyrics.txt", "a")  # Old country classics and more playlist
# filter.lyrics_filter("country_lyrics.txt", "country_filtered.txt", "w")

# Pop lyrics miner
Lyrics.getLyrics("spotify:user:caaakeeey:playlist:6QAKnenuZoowNqxRzZbeRg", 1860, "pop_lyrics.txt", "w") # Guess that tune.  playlist
filter.lyrics_filter("pop_lyrics.txt", "pop_filtered.txt", "w")
