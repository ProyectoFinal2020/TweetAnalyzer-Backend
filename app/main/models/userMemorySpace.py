class UserMemorySpace:
    def __init__(self, availableSpace: int, spaceUsed: int, topicsAndSpaceUsed: list):
        self.availableSpace = availableSpace
        self.spaceUsed = spaceUsed
        self.additionalInformation = topicsAndSpaceUsed


class TopicAndSpaceUsed:
    def __init__(self, topic: str, spacedUsed: int, language: str):
        self.topic = topic
        self.spaceUsed = spacedUsed
        self.language = language
