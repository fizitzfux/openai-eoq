from openai import OpenAI
import time
import io
from random import randint

# Function to read Minecraft server log for chat messages
def read_minecraft_log():
    with io.open('./logs/latest.log','r', buffering=1) as log_file:
        log_file.seek(0, 2)  # Move cursor to end of file
        while True:
            new_line = log_file.readline()
            if new_line:
                if '[Server thread/INFO]' in new_line and '<' in new_line:
                    # Extract chat message from log line
                    chat_message = new_line.split('> ')[-1].strip()
                    print(chat_message)
                    send_to_chatgpt(chat_message)
            else:
                time.sleep(1)  # Sleep for 1 second before checking for new lines

# Function to send chat message to ChatGPT API
def send_to_chatgpt(message):
    # Send message to ChatGPT API and process response
    # Implement this part based on the API documentation
    openai = OpenAI(
        api_key="qhr3cy383obm", base_url="https://openai.sd42.nl/api/providers/openai/v1"
    )

    prompt = message

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate Minecraft 1.18.1 valid commands to do the following instructions. all positions should be relative to the player. You can specify the player with @s. Use modern item names. DO NOT USE minecraft:bed OR minecraft:door. Use minecraft:air instead of 0. Make sure all block namespaces and commands are valid. After generating the output strip everything but the commands, every command should start with '/'."},
            {"role": "user", "content": prompt},
        ],
    )

    output = response.choices[0].message.content
    print(output)
    write_to_pack(output)

    # Check credit status
    print(openai.models.with_raw_response.list().headers["OpenAiProxy"])


def write_to_pack(commands):
    prompt_id = str(randint(0, 9999999))
    lines = (
        "execute if data storage main {lastid:"+prompt_id+"} run return 0\n"
        "data modify storage main lastid set value "+prompt_id+"\n"
    )
    for c in commands.split('\n'):
        if '/' in c:
            index = c.index('/')
            c = c[index+1:]
            c = c.rstrip('` ')
            lines += "execute as @p at @s run "+c+"\n"
    print('>', lines)
    with open('./saves/1/datapacks/loader/data/loader/functions/load.mcfunction', 'w') as pack:
        pack.write(lines)


# Main function
def main():
    read_minecraft_log()

if __name__ == "__main__":
    main()

