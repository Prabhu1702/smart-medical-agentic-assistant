from autogen_agentchat.agents import UserProxyAgent

def user_proxy():
    return UserProxyAgent(
        name="user_proxy"
    )