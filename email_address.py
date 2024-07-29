class EmailAddress:
    def __init__(self, address: str):
        self.full = address
        content = address.split('@')
        if len(content) != 2:
            self.local_part = content[0] + '@' + content[1]
            self.domain = content[2]
        else:
            self.local_part = content[0]
            self.domain = content[1]

    def __repr__(self) -> str:
        return self.local_part + " [at] " + self.domain
    