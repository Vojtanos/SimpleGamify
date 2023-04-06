actionConfigSchema = {
    "type" : "object",
    "additionalProperties": {
        "type" : "object",
        "properties" : {
            "desc" : {"type" : "string"},
            "points" : {"type" : "object"},
            "custom" : {"type" : "object"},
        },
    }
}

challengeConfigSchema = {
    "type" : "object",
    "additionalProperties": {
        "type" : "object",
        "properties" : {
            "title" : {"type" : "string"},
            "desc" : {"type" : "string"},
            "points" : {"type" : "object"},
            "challenges" : {"type" : "array"},
            "custom" : {"type" : "object"},
            "badge" : {"type" : "object"},
        },
    }
}

levelConfigSchema = {
    "type" : "object",
    "additionalProperties": {
        "type" : "object",
        "properties" : {
            "points" : {"type" : "object"},
            "custom" : {"type" : "object"},
        },
    }
}

pointSystemConfigSchema = {
    "type" : "object",
    "additionalProperties": {
        "type" : "object",
        "properties" : {
            "desc" : {"type" : "string"},
            "custom" : {"type" : "object"},
        },
    }
}