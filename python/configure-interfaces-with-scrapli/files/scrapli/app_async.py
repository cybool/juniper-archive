import asyncio

from scrapli_netconf.driver import AsyncNetconfDriver
from scrapli.logging import enable_basic_logging

# Enable logging. Create a log file in the current directory.
enable_basic_logging(file=True, level="debug")

GALVESTON = {
    "host": "192.168.105.137",
    "auth_username": "scrapli",
    "auth_password": "juniper123",
    "auth_strict_key": False,
    "transport": "asyncssh"
}

SANANTONIO = {
    "host": "192.168.105.146",
    "auth_username": "scrapli",
    "auth_password": "juniper123",
    "auth_strict_key": False,
    "transport": "asyncssh"
}

DEVICES = [GALVESTON, SANANTONIO]

CONFIG = """
<config>
    <configuration>
        <interfaces>
            <interface>
                <name>ge-0/0/1</name>
                <unit>
                    <name>0</name>
                    <family>
                        <inet>
                            <address>
                                <name>192.168.110.22/24</name>
                            </address>
                        </inet>
                    </family>
                </unit>
            </interface>
        </interfaces>
    </configuration>
</config>
"""


# async function to open a connection and return the output of our RPC
async def edit_configuration(device):
    conn = AsyncNetconfDriver(**device)
    await conn.open()
    result = await conn.edit_config(config=CONFIG, target="candidate")
    await conn.close()
    return result


# primary function
async def main():
    """Function to gather coroutines, await them and print results"""
    coroutines = [edit_configuration(device) for device in DEVICES]
    results = await asyncio.gather(*coroutines)
    for each in results:
        print(each.host)
        print(each.result)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())