# Discord-Reservation-Bot
## What does it do?
Are you too lazy to reserve a library room for yourself at UoP? Well this bot alleviates some of those dreadful clicks.
This discord bot provides a client interface via discord, that allows you to effortessly reserve a library room. All you have to do is confirm reservation. 

## How does it do it?
As stated, the bot acts as the client interface via the discord command, '-reserve'. This prints out the available library times for the current day and prompts you to react to the times. Once reacted, you confirm it by reacting to a check emoji, and it does all the backend stuff to find you a room for those inputted times

However, the first time you run '-reserve', the code has no idea who you are! Therefore, the bot will DM you and ask you for the information needed to create a reservation (i.e. first/last name, university id, and university email). It saves this data ***locally***, and will ***never*** be shared with anyone. If at any time the user does not want their data in the database, all they have to do is run the discord command '-deleteme'

The backend leverages my [Library Reservation Tool V2](https://github.com/RamonAra209/Library-Reservation-Tool-V2) to go in and do all the tedious work for you. If you're interested in the backend, go take a look at that.