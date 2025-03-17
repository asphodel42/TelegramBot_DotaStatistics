from opendota_api import getLastMatchId, getMatchStats, saveStatsToJSON
import time

PLAYER_ID = 205674998

def main():
    last_match_id = None

    try:
        while True:
            try:   
                match_id = getLastMatchId(PLAYER_ID)

                if last_match_id != match_id:
                    last_match_id = match_id

                    stats = getMatchStats(PLAYER_ID, match_id)
                    saveStatsToJSON(stats)

                    print(f"New match {match_id} was played")
                else:
                    print("No new match yet, checking again...")

            except Exception as e:
                print(f"Error: {e}")
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    return 0

if __name__ == "__main__":
    main()